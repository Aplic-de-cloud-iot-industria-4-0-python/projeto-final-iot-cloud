import os
import re
import sys
import abc
import time
import json
import fiona
import msvcrt
import shutil
import logging
import sqlite3
import requests
import importlib
import subprocess
from osgeo import ogr
from pyproj import CRS
import geopandas as gpd
from pathlib import Path
from ..features.doc import *
from ..features.rede import *
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ..features.build import *
from ...backend.crud.crud import DatabaseManager
from ..features.version import *
from ..features.tamPasta import *
from ..features.cacheApp import *
from ..features.animacoes import *
from abc import ABC, abstractmethod
from ..features.dependencias import *
from ..features.backupProjeto import *
from ..features.localizacaoPC import *
from ..features.rede import RedeArquivos
from ..features.ambienteVirtual import *
from ..features.arquivoExecutavel import *
from ..arquivosRede.folders.shape import ShapeProject
from ..features.localizacaoPC import _determinar_local_pc
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float


load_dotenv()
database = os.getenv('DATABASE')
powershell = os.getenv('MAPEAMENTO')
virtual = os.getenv('AMBIENTE_VIRTUAL')
virtual_linux = os.getenv('AMBIENTE_VIRTUAL_LINUX')
documentacao = os.getenv('DOC')
nasArquivosRede = os.getenv('DIRETORIO_RAIZ')
nas = os.getenv('NAS')
Base = declarative_base()

def log_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f'Executing: {func.__name__}')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f'Error occurred: {str(e)}')
            raise
    return wrapper


def add_method(cls):
    def inner_func(self):
        print("This is a dynamically added method")
    cls.dynamic_method = inner_func
    return cls


class ScriptExecutor(ABC):
    @abstractmethod
    def execute_script(self):
        pass


@add_method
class PowerShellScriptExecutor(ScriptExecutor):
    def __init__(self, script_path):
        self.script_path = script_path

    @log_decorator
    def execute_script(self):
        try:
            subprocess.run(["powershell.exe", self.script_path], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'Script execution failed: {e}')
            raise

    def __str__(self):
        return f'PowerShellScriptExecutor: {self.script_path}'


class Shapefile:
    class Rota(Base):
        __tablename__ = 'rota'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        origem = Column(String)
        destino = Column(String)
        srid = Column(String)
        
    def __init__(self, database_path=database):
        self.database_path = database_path
        self.engine = create_engine(f'sqlite:///{self.database_path}')
        Base.metadata.create_all(self.engine)
        self.conn = DatabaseManager()._create_or_connect_db()
        self.diretorio_destino = nasArquivosRede
        # DatabaseManager()._add_columns_if_not_exist()

    def get_srid_from_shapefile(self, shapefile_path):
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = driver.Open(shapefile_path, 0)  # 0 means read-only
        layer = dataSource.GetLayer()
        spatial_ref = layer.GetSpatialRef()
        
        # SRID é extraído do SpatialReference
        srid = spatial_ref.GetAuthorityCode(None)
        return srid

    def process_shapefiles(self):
        diretorio_raiz = r"\\nas.ibge.gov.br\DGC-ACERVO-CCAR2\CONVERSAO_DIGITAL\CCAR_PRODUTOS_VETOR\Arquivos_Shape\CCAR_PRODUTOS_VETOR"
        destino_pc = "D:/projetoIBGE/mapeamentoapp/src/backend/server/nas/arquivosRede"
        db_manager = DatabaseManager()

        id_atual = 1
        mensagem_anterior = ''
        for root, _, files in os.walk(diretorio_raiz):
            for file in files:
                if file.endswith(".prj"):
                    caminho_completo = Path(root) / file
                    srid_info = db_manager.get_srid_from_prj(str(caminho_completo))
                    nome_sem_extensao = caminho_completo.stem

                    origem = str(Path(root)).replace('\\', '/').split('CCAR_PRODUTOS_VETOR/', 1)[1]
                    destino = Path(destino_pc, nome_sem_extensao).as_posix()

                    rota_info = {
                        'name': nome_sem_extensao,
                        'origem': origem,
                        'destino': destino
                    }

                    db_manager.insert_data(srid_info, rota_info)

                    mensagem = f"{id_atual}: {nome_sem_extensao}"
                    print(f"\r{mensagem}" + " " * (len(mensagem_anterior) - len(mensagem)), end='', flush=True)
                    mensagem_anterior = mensagem
                    
                    id_atual += 1
                    
        data = db_manager.retrieve_data_for_json()
        with open('D:/projetoIBGE/mapeamento/app/src/backend/server/nas/data/exported_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        # Para garantir que a última linha seja "apagada":
        print("\r" + " " * len(mensagem_anterior) + "\r", end='', flush=True)