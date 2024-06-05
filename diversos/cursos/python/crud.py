Base = declarative_base()
load_dotenv()
database = os.getenv('DATABASE')


class SpatialRefSys(Base):
    __tablename__ = 'spatial_ref_sys'
    srid = Column(Integer, primary_key=True)  # SRID como chave primária, inteiro
    auth_name = Column(String(256))  # Nome da autoridade do SRID, como 'EPSG'
    auth_srid = Column(Integer)  # O identificador numérico do SRID fornecido pela autoridade
    srtext = Column(String(2048))  # Texto WKT do SRID
    proj4text = Column(String(2048))  # Texto PROJ4 do SRID
    rotas = relationship("Rota", back_populates="spatial_ref")

class Rota(Base):
    __tablename__ = 'rota'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    origem = Column(String)
    destino = Column(String)
    srid = Column(Integer, ForeignKey('spatial_ref_sys.srid'))
    spatial_ref = relationship("SpatialRefSys", back_populates="rotas")

class DatabaseManager:
    def __init__(self, database_path=os.getenv('DATABASE')):
        self.database_path = database_path
        self.engine = create_engine(f'sqlite:///{self.database_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def _create_or_connect_db(self):
        return sqlite3.connect(self.database_path)

    def insert_data(self, srid_info, rota_info):
        session = self.Session()
        spatial_ref = session.query(SpatialRefSys).filter_by(auth_srid=srid_info['auth_srid']).first()
        if not spatial_ref:
            spatial_ref = SpatialRefSys(**srid_info)
            session.add(spatial_ref)
            session.commit()
        rota_info['srid'] = spatial_ref.srid
        rota = Rota(**rota_info)
        session.add(rota)
        session.commit()
        session.close()

    def get_srid_from_prj(self, prj_file_path):
        if not os.path.exists(prj_file_path):
            raise FileNotFoundError(f"Arquivo PRJ não encontrado: {prj_file_path}")
        
        srs = osr.SpatialReference()
        
        try:
            with open(prj_file_path, 'r') as prj_file:
                srs.ImportFromWkt(prj_file.read())
        except OSError as e:
            raise OSError(f"Erro ao ler arquivo PRJ: {prj_file_path} - {str(e)}")
        
        return {
            'auth_name': srs.GetAttrValue('AUTHORITY', 0),
            'auth_srid': int(srs.GetAttrValue('AUTHORITY', 1)) if srs.GetAttrValue('AUTHORITY', 1) else 0,
            'srtext': srs.ExportToWkt(),
            'proj4text': srs.ExportToProj4()
        }

    def retrieve_data_for_json(self):
        session = self.Session()
        spatial_refs = session.query(SpatialRefSys).all()
        rotas = session.query(Rota).all()

        data = {
            "SpatialRefSys": [
                {
                    "srid": spatial.srid,
                    "auth_name": spatial.auth_name,
                    "auth_srid": spatial.auth_srid,
                    "srtext": spatial.srtext,
                    "proj4text": spatial.proj4text
                } for spatial in spatial_refs
            ],
            "Rota": [
                {
                    "id": rota.id,
                    "name": rota.name,
                    "origem": rota.origem,
                    "destino": rota.destino,
                    "srid": rota.srid
                } for rota in rotas
            ]
        }
        session.close()
        return data
    
    def update_data(self, rota_id, update_info):
        """
        Atualiza os dados de uma rota específica.

        :param rota_id: O ID da rota a ser atualizada.
        :param update_info: Dicionário contendo as informações para atualização.
        """
        session = self.Session()
        try:
            rota = session.query(Rota).filter_by(id=rota_id).first()
            if not rota:
                print(f"Rota com ID {rota_id} não encontrada.")
                return

            # Atualiza os campos da rota com as novas informações
            for key, value in update_info.items():
                if hasattr(rota, key):
                    setattr(rota, key, value)
                else:
                    print(f"Aviso: A chave '{key}' não é um atributo válido de Rota e foi ignorada.")

            session.commit()
            print(f"Rota com ID {rota_id} atualizada com sucesso.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar rota com ID {rota_id}: {e}")
        finally:
            session.close()

    def backup_dados(self, backup_path):
        """Cria uma cópia de backup do banco de dados."""
        try:
            shutil.copy(self.database_path, backup_path)
            print(f"Backup realizado com sucesso em: {backup_path}")
        except Exception as e:
            print(f"Erro ao realizar backup: {e}")

    def recuperar_dados(self, backup_path):
        """Restaura o banco de dados a partir de um backup."""
        try:
            shutil.copy(backup_path, self.database_path)
            print(f"Dados recuperados com sucesso do backup: {backup_path}")
        except Exception as e:
            print(f"Erro ao recuperar dados: {e}")

    def criar_indice(self, table_name, column_name):
        """Cria um índice para uma coluna específica em uma tabela."""
        session = self.Session()
        try:
            session.execute(f"CREATE INDEX IF NOT EXISTS idx_{column_name} ON {table_name} ({column_name});")
            session.commit()
            print(f"Índice criado com sucesso para a coluna {column_name} na tabela {table_name}.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar índice: {e}")
        finally:
            session.close()

    def consultar_dados(self, table_name, conditions=None):
        """
        Realiza uma consulta em uma tabela específica com condições opcionais.

        :param table_name: Nome da tabela a ser consultada.
        :param conditions: Dicionário de condições para filtrar os resultados, onde a chave é o nome da coluna.
        """
        session = self.Session()
        try:
            # Encontrar a classe da tabela baseada no nome da tabela
            table_class = Base.metadata.tables.get(table_name)
            if table_class is None:
                print(f"A tabela {table_name} não foi encontrada.")
                return

            query = session.query(table_class)
            
            if conditions:
                for column, value in conditions.items():
                    # Aplica as condições de filtragem
                    query = query.filter(getattr(table_class.c, column) == value)

            results = query.all()
            if not results:
                print(f"Nenhum dado encontrado para a tabela {table_name} com as condições especificadas.")
                return

            for result in results:
                print(result)
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
        finally:
            session.close()


    def deletar_dados(self, table_name, condition):
        """Deleta registros de uma tabela baseado em uma condição."""
        session = self.Session()
        try:
            session.execute(f"DELETE FROM {table_name} WHERE {condition};")
            session.commit()
            print(f"Dados deletados com sucesso da tabela {table_name} onde {condition}.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar dados: {e}")
        finally:
            session.close()

    def deletar_banco(self):
        """Deleta o arquivo do banco de dados."""
        try:
            os.remove(self.database_path)
            print(f"Banco de dados {self.database_path} deletado com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar o banco de dados: {e}")