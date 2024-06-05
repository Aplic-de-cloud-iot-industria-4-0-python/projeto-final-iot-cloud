from .modulos import *

root = Tk()

load_dotenv()
login = os.getenv('LOGIN')
powershell = os.getenv('MAPEAMENTO')
virtual = os.getenv('AMBIENTE_VIRTUAL')
virtual_linux = os.getenv('AMBIENTE_VIRTUAL_LINUX')
database = os.getenv('DATABASE')
nasArquivosRede = os.getenv('DIRETORIO_RAIZ')
search_bool = False

def maximize_window(event=None):
    if platform == "win32":  # Para Windows
        root.state('zoomed')
    else:  # Para Unix-like (Linux, MacOS)
        root.attributes('-zoomed', True)


class Relatorios():
    def mostrar(self):
        webbrowser.open('relatorioMapeamento'+self.namerel+'.pdf')

    def Gerar_Ficha(self):
        self.codigorel = self.entry_codigo.get()
        self.namerel = self.entry_name.get()
        self.origemrel = self.entry_origem.get()
        self.destinorel = self.entry_destino.get()
        self.sridrel = self.entry_srid.get()
        self.ficha_cliente = canvas.Canvas('relatorioMapeamento'+self.namerel+'.pdf')
        self.ficha_cliente.setFont("Helvetica-Bold",20)
        self.ficha_cliente.drawString(200,780,'FICHA DO CLIENTE')
        self.ficha_cliente.setFont("Helvetica-Bold",20)
        self.ficha_cliente.drawString(50,680,'Código: '+self.codigorel)
        self.ficha_cliente.drawString(50, 650, 'name: ' + self.namerel)
        self.ficha_cliente.drawString(50, 620, 'origem: ' + self.origemrel)
        self.ficha_cliente.drawString(50, 590, 'destino: ' + self.destinorel)
        self.ficha_cliente.drawString(50, 590, 'srid: ' + self.sridrel)
        self.ficha_cliente.rect(20,430,550,400, fill=False,stroke=True)
        self.ficha_cliente.showPage()
        self.ficha_cliente.save()
        self.mostrar()


class Funcoes():
    def limpar_campos(self):
        self.entry_codigo.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_origem.delete(0, END)
        self.entry_destino.delete(0, END)
        self.entry_srid.delete(0, END)

    def db_conect(self):
        self.conexao = sqlite3.connect(database)
        # self.conexao = sqlite3.connect('db.sqlite')
        self.cursor = self.conexao.cursor()
        print("conectando ao banco de dados")

    def db_conectUsuarios(self):
        self.conexao = sqlite3.connect(login)
        # self.conexao = sqlite3.connect('db.sqlite')
        self.cursor = self.conexao.cursor()
        print("conectando ao banco de dados")

    def db_desconect(self):
        self.conexao.close()
        print("Desconectando ao banco de dados sqlite3")

    def criar_tabela(self):
        self.db_conect()
        #Criando uma tabela se ela não existir
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rota(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            origem INTEGER(11) NOT NULL,
            destino VARCHAR(40) NOT NULL,
            srid INTEGER(11));""")
        self.conexao.commit(); print("banco de dados criado")
        self.db_desconect()

    def capturar_campos(self):
        self.codigo = self.entry_codigo.get()
        self.name = self.entry_name.get()
        self.origem = self.entry_origem.get()
        self.destino = self.entry_destino.get()
        self.srid = self.entry_srid.get()

    def add_cliente(self):
        #obter dados dos campos
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""INSERT INTO rota (name,origem,destino,srid) 
        VALUES(?,?,?,?)""",(self.name,self.origem,self.destino,self.srid))
        self.conexao.commit()
        self.db_desconect()
        self.select_lista()
        self.limpar_campos()

    def select_lista(self):
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.db_conect()
        lista = self.cursor.execute("""SELECT id , name,origem,destino,srid
         FROM rota ORDER BY name ASC;""")
        for l in lista:
            self.lista_grid.insert("",END,values=l)
        self.db_desconect()

    def OnDubleClick(self,event):
        self.limpar_campos()
        self.lista_grid.selection()
        for x in self.lista_grid.selection():
            col1,col2,col3,col4,col5 = self.lista_grid.item(x,'values')
            self.entry_codigo.insert(END, col1)
            self.entry_name.insert(END, col2)
            self.entry_origem.insert(END, col3)
            self.entry_destino.insert(END, col4)
            self.entry_srid.insert(END, col5)

    def deleta_cliente(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""DELETE FROM rota WHERE id = ?""", (self.codigo,))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def alterar_cliente(self):
        self.capturar_campos()
        self.db_conect()
        self.cursor.execute("""UPDATE rota SET name = ?, origem = ?, destino = ?, srid = ?
        WHERE id = ?;
        """,(self.name,self.origem,self.destino,self.srid,self.codigo))
        self.conexao.commit()
        self.db_desconect()
        self.limpar_campos()
        self.select_lista()

    def Buscar_Rota(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.entry_name.insert(END,'%')
        name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM rota WHERE name LIKE '%s' COLLATE NOCASE ORDER BY name ASC"""%name)
        Resultado_busca = self.cursor.fetchall()
        for cliente in Resultado_busca:
            self.lista_grid.insert("",END,values=cliente)
        self.db_desconect()
        self.limpar_campos()
        self.db_desconect()

    def Buscar_spatial_ref_sys(self):
        self.db_conect()
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.entry_name.insert(END,'%')
        # name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM spatial_ref_sys """)
        Resultado_busca = self.cursor.fetchall()
        for cliente in Resultado_busca:
            self.lista_grid.insert("",END,values=cliente)
        self.db_desconect()
        self.limpar_campos()
        self.db_desconect()

    def Buscar_usuarios(self):
        self.db_conectUsuarios()
        self.lista_grid.delete(*self.lista_grid.get_children())
        self.entry_name.insert(END,'%')
        # name = '%'+self.entry_name.get()
        self.cursor.execute("""SELECT * FROM users """)
        Resultado_busca = self.cursor.fetchall()
        for cliente in Resultado_busca:
            self.lista_grid.insert("",END,values=cliente)
        self.db_desconect()
        self.limpar_campos()
        self.db_desconect()


class Aplication(Funcoes,Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_tela()
        self.grid_cliente()
        self.widgets_frame1()
        self.Menus()
        self.criar_tabela()
        self.select_lista()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Intercepta o fechamento
        self.root.bind("<Map>", self.on_desiconify)  # Vincula o evento de restauração da janela
        root.mainloop()

    def tela(self):
        self.root.title("Mapeamento de arquivos Shapefile")
        self.root.configure(background='#6a50c9')
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=850, height=700)
        self.root.minsize(width=400, height=300)
        self.root.bind("<Map>", self.on_desiconify)  # Vincula o evento de desiconificação

    def frames_tela(self):
        self.frame1 = Frame(self.root, bd=4, bg="#fff",
                            highlightbackground="#b471f8", highlightthickness=3)
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2 = Frame(self.root, bd=4, bg="#fff",
                            highlightbackground="#b471f8", highlightthickness=3)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def on_close(self):
        self.root.destroy()

    def on_desiconify(self, event=None):
        # Verifica se a janela foi minimizada e então maximiza novamente
        if self.root.state() == 'iconic':
            self.root.deiconify()  # Restaura a janela se ela estiver minimizada
            self.root.geometry("1920x108")  # Define o tamanho desejado ou maximiza conforme necessário

    def widgets_frame1(self):
       # Estilo comum para os botões
        estilo_botao = {
            'bg': '#583bbf',
            'fg': 'white',
            'font': ('verdana', 8, 'bold')
        }
        
        # Espaçamento e tamanho dos botões
        largura_botao = 0.1
        espacamento_inicial = 0.05
        incremento = largura_botao + 0.01  # Ajuste o espaçamento conforme necessário
        # Botão Mapeamento
        self.bt_mapeamento = Button(self.frame1, text="Mapear", command=self.mapeamento, **estilo_botao)
        self.bt_mapeamento.place(relx=espacamento_inicial, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Inserir
        self.bt_inserir = Button(self.frame1, text="Inserir", command=self.insercao, **estilo_botao)
        self.bt_inserir.place(relx=espacamento_inicial + incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Limpar
        self.bt_limpar = Button(self.frame1, text="Limpar", command=self.limpar_campos, **estilo_botao)
        self.bt_limpar.place(relx=espacamento_inicial + 2*incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Buscar
        self.bt_buscar = Button(self.frame1, text="Buscar", command=self.Buscar_Rota, **estilo_botao)
        self.bt_buscar.place(relx=espacamento_inicial + 3*incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Novo
        self.bt_novo = Button(self.frame1, text="Novo", command=self.add_cliente, **estilo_botao)
        self.bt_novo.place(relx=espacamento_inicial + 4*incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Atualizar
        self.bt_alterar = Button(self.frame1, text="Atualizar", command=self.alterar_cliente, **estilo_botao)
        self.bt_alterar.place(relx=espacamento_inicial + 5*incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # Botão Apagar
        self.bt_apagar = Button(self.frame1, text="Apagar", command=self.deleta_cliente, **estilo_botao)
        self.bt_apagar.place(relx=espacamento_inicial + 6*incremento, rely=0.07, relwidth=largura_botao, relheight=0.15)
        # label e entry - codigo
        self.lb_codigo = Label(self.frame1, text="Codigo", bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.lb_codigo.place(relx=0.05, rely=0.3)
        self.entry_codigo = Entry(self.frame1, bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.entry_codigo.place(relx=0.2, rely=0.3, relwidth=0.2)
        # label e entry - name
        self.lb_name = Label(self.frame1, text="name", bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.lb_name.place(relx=0.5, rely=0.3)
        self.entry_name = Entry(self.frame1, bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.entry_name.place(relx=0.65, rely=0.3, relwidth=0.2)
        # label e entry - origem
        self.lb_origem = Label(self.frame1, text="origem", bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.lb_origem.place(relx=0.05, rely=0.5)
        self.entry_origem = Entry(self.frame1, bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.entry_origem.place(relx=0.2, rely=0.5, relwidth=0.2)
        # label e entry - destino
        self.lb_destino = Label(self.frame1, text="destino", bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.lb_destino.place(relx=0.5, rely=0.5)
        self.entry_destino = Entry(self.frame1, bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.entry_destino.place(relx=0.65, rely=0.5, relwidth=0.2)
        # label e entry - srid
        self.lb_srid = Label(self.frame1, text="srid", bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.lb_srid.place(relx=0.05, rely=0.7)
        self.entry_srid = Entry(self.frame1, bg="white", fg="#583bbf", font=('verdana', 10, 'bold'))
        self.entry_srid.place(relx=0.2, rely=0.7, relwidth=0.2)
        # Botão para mostrar dados da tabela Rota
        self.bt_mostrar_rota = Button(self.frame1, text="Mostrar Rota", command=self.Buscar_Rota, **estilo_botao)
        self.bt_mostrar_rota.place(relx=0.05, rely=0.85, relwidth=largura_botao, relheight=0.15)
        # Botão para mostrar dados da tabela spatial_ref_sys
        self.bt_mostrar_spatial_ref_sys = Button(self.frame1, text="Mostrar Spatial Ref Sys", command=self.Buscar_spatial_ref_sys, **estilo_botao)
        self.bt_mostrar_spatial_ref_sys.place(relx=0.16, rely=0.85, relwidth=largura_botao, relheight=0.15)
        self.bt_mostrar_spatial_ref_sys = Button(self.frame1, text="Mostrar Usuários", command=self.Buscar_usuarios, **estilo_botao)
        self.bt_mostrar_spatial_ref_sys.place(relx=0.27, rely=0.85, relwidth=largura_botao, relheight=0.15)

    def grid_cliente(self):
        self.lista_grid = ttk.Treeview(self.frame2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.lista_grid.heading("#0", text='')
        self.lista_grid.heading("#1", text='CODIGO')
        self.lista_grid.heading("#2", text='name')
        self.lista_grid.heading("#3", text='origem')
        self.lista_grid.heading("#4", text='destino')
        self.lista_grid.heading("#5", text='srid')
        self.lista_grid.column("#0", width=1)
        self.lista_grid.column("#1", width=25)
        self.lista_grid.column("#2", width=200)
        self.lista_grid.column("#3", width=125)
        self.lista_grid.column("#4", width=125)
        self.lista_grid.column("#5", width=125)
        self.lista_grid.place(relx=0.005, rely=0.1, relwidth=0.95, relheight=0.86)
        self.scrol_lista = Scrollbar(self.frame2, orient='vertical')
        self.lista_grid.configure(yscroll=self.scrol_lista.set)
        self.scrol_lista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.88)
        self.lista_grid.bind("<Double-1>",self.OnDubleClick)

    def insercao(self):
        messagebox.showinfo("Sucesso", "Começando a inserir os dados no banco!")  # Feito
        shape_processor = Shapefile(database)
        shape_processor.process_shapefiles()
        self.mapeamento_monitor()

    def mapeamento_monitor(self):
        class DownloadMonitorHandler(FileSystemEventHandler):
            def __init__(self, app):
                self.app = app

            def on_created(self, event):
                # Este método é chamado quando um arquivo ou pasta é criado
                self.app.update_display(f"Novo arquivo ou pasta criado: {event.src_path}")

            def on_modified(self, event):
                # Este método é chamado quando um arquivo é modificado
                self.app.update_display(f"Arquivo modificado: {event.src_path}")

    # TODO: Adicionar as funcionalidades do menu de acordo com a necessidade
    def mapeamento(self):
        messagebox.showinfo("Sucesso", "Começando a mapear!")  # Feito
        executor = PowerShellScriptExecutor(powershell)
        try:
            executor.execute_script()
            self.mapeamento_monitor()
        except Exception as e:
            pass
        
        class App:
            def __init__(self, root, path_to_watch):
                self.root = root
                self.path_to_watch = path_to_watch
                self.root.title("Monitor de Downloads")

                self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
                self.text_area.pack(padx=10, pady=10)
                self.text_area.config(state='disabled')

            def update_display(self, message):
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, message + "\n")
                self.text_area.config(state='disabled')
                self.text_area.yview(tk.END)

            def on_close(self):
                self.observer.stop()
                self.observer.join()
                self.root.destroy()

        path_to_watch = nasArquivosRede
        root = tk.Tk()
        app = App(root, path_to_watch)
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        root.mainloop()


    def sqlite_monitor(self):
        class DatabaseMonitor:
            def __init__(self, db_path, app, check_interval=5):
                self.db_path = db_path
                self.app = app
                self.check_interval = check_interval
                # Atualize "sua_tabela" pelo nome real da tabela que você quer monitorar
                self.table_name = "rota"  # Substitua pelo nome real da sua tabela
                self.last_row_id = self.get_last_row_id()

            def get_last_row_id(self):
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT MAX(id) FROM {self.table_name}")
                    last_id = cursor.fetchone()[0]
                    conn.close()
                    return last_id if last_id is not None else 0
                except Exception as e:
                    print(f"Erro ao acessar o banco de dados: {e}")
                    return 0

            def check_for_updates(self):
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {self.table_name} WHERE id > {self.last_row_id}")
                    rows = cursor.fetchall()
                    conn.close()
                    for row in rows:
                        self.app.update_display(f"Nova inserção: {row}")
                        self.last_row_id = row[0]
                except Exception as e:
                    print(f"Erro ao acessar o banco de dados: {e}")

        class App:
            def __init__(self, root, db_path):
                self.root = root
                self.db_path = db_path
                self.root.title("Monitor de Banco de Dados")

                self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
                self.text_area.pack(padx=10, pady=10)
                self.text_area.config(state='disabled')

                # self.start_monitoring()

            def update_display(self, message):
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, message + "\n")
                self.text_area.config(state='disabled')
                self.text_area.yview(tk.END)

            def on_close(self):
                self.root.destroy()

        db_path = database
        root = tk.Tk()
        app = App(root, db_path)
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        root.mainloop()


    # TODO: Adicionar as funcionalidades do menu de acordo com a necessidade
    def Ambiente_VirtualAtivarWindows(self):
        messagebox.showinfo("Sucesso", "Ambiente Virtual ativado no Windows!")
        print("==================================================================")
        print("==================== Ambiente virtual ATIVADO ====================")
        print("==================================================================")
        # activator = VirtualEnvActivator(virtual)
        # activator.get_activation_command()

    def Ambiente_VirtualDesativarWindows(self):
        messagebox.showinfo("Sucesso", "Ambiente Virtual desativado no Windows!")
        print("==================================================================")
        print("=================== Ambiente virtual DESATIVADO ==================")
        print("==================================================================")
        # manager = VirtualEnvManager(virtual)
        # manager.create_virtualenv()

    def Ambiente_VirtualAtivarLinux(self):
        messagebox.showinfo("Sucesso", "Ambiente Virtual ativado no Linux!")
        print("==================================================================")
        print("==================== Ambiente virtual ATIVADO ====================")
        print("==================================================================")
        # activate_script = virtual_linux
        # subprocess.call(['cmd', '/c', activate_script])
        # site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
        # if site_packages_path not in sys.path:
        #     sys.path.insert(0, site_packages_path)

    def Ambiente_VirtualDesativarLinux(self):
        messagebox.showinfo("Sucesso", "Ambiente Virtual desativado no Linux!")
        print("==================================================================")
        print("=================== Ambiente virtual DESATIVADO ==================")
        print("==================================================================")
        # env_manager = VirtualEnvManager(virtual_linux)
        # env_manager.deactivate()

    def salvar_info_texto(self): # Feito
        messagebox.showinfo("Salvar", "Salvar informações em arquivo de texto")
        arquivo_destino = input("Digite o nome do arquivo de texto para salvar os dados: ")
        shape = ShapeProject()
        shape.salvar_dados_em_arquivo(arquivo_destino)
        messagebox.showinfo("Sucesso", "Ambiente Virtual desativado no Linux!")
        # print("Dados salvos em:", arquivo_destino)

    def baixar_pacotes(self):
        messagebox.showinfo("Sucesso", "Baixar Pacotes")

    def atualizar_dependencias(self):
        messagebox.showinfo("Sucesso", "Atualização de dependências")

    def gerar_relatorio_estatistico(self):
        messagebox.showinfo("Sucesso", "Geração de relatório estatístico")

    def deploy_github(self):
        messagebox.showinfo("Sucesso", "Deploy ao Github")

    def remover_pasta_rede(self):
        shapefileRedearquivos = RedeArquivos()
        shapefileRedearquivos.remover_pasta(nasArquivosRede)
        messagebox.showinfo("Sucesso", "Removendo pastas da Rede")

    def resolver_conflitos(self):
        messagebox.showinfo("Sucesso", "Resolvendo conflitos de dependências")

    def remover_dependencias(self):
        messagebox.showinfo("Sucesso", "Removendo dependências")

    def verificar_versao(self):
        messagebox.showinfo("Sucesso", "Verificando a versão do projeto")

    def consultar_documentacao(self):
        messagebox.showinfo("Sucesso", "Consultando a documentação do projeto")

    def deletar_documentacao(self):
        messagebox.showinfo("Sucesso", "Deletando a documentação do projeto")

    def gerar_executavel(self):
        messagebox.showinfo("Sucesso", "Gerando um arquivo executável do projeto")

    def executar_frontend(self):
        messagebox.showinfo("Sucesso", "Executando o frontend da aplicação")

    def verificar_atualizacoes(self):
        messagebox.showinfo("Sucesso", "Verificando se há atualizações a serem feitas")

    def remover_pacotes(self):
        messagebox.showinfo("Sucesso", "Removendo pacotes ou dependências")

    def faq(self):
        messagebox.showinfo("Sucesso", "Exibindo FAQs")

    def verificar_logs_seguranca(self):
        messagebox.showinfo("Sucesso", "Verificando logs de segurança")

    def agendar_tarefas(self):
        messagebox.showinfo("Sucesso", "Agendando tarefas automatizadas")

    def gerar_relatorios_estatisticos(self):
        messagebox.showinfo("Sucesso", "Gerando relatórios estatísticos")

    def apagar_projeto(self):
        messagebox.showinfo("Sucesso", "Apagando o projeto")

    def streamlit(self):
        messagebox.showinfo("Sucesso", "Abrindo o navegador!")

    def flask_api(self):
        messagebox.showinfo("Sucesso", "Acessando a API com Flask!")

    def clear_widgets(self):
        for widget in root.winfo_children():
            widget.destroy()

    def Menus(self):
        Menubar = Menu(self.root)
        self.root.config(menu=Menubar)
        filemenu = Menu(Menubar)
        filemenu0 = Menu(Menubar)
        filemenu1 = Menu(Menubar)
        filemenu2 = Menu(Menubar)
        filemenu3 = Menu(Menubar)
        filemenu4 = Menu(Menubar)

        def Quit():
            self.clear_widgets()  # Limpa a interface atual
            main()  # Reinicia a interface de login
        
        Menubar.add_cascade(label="Deslogar",command=Quit)
        Menubar.add_cascade(label="Monitoramento",menu=filemenu)
        # filemenu.add_command(label="Mapeamento sendo realizado",command=self.mapeamento_monitor)
        # filemenu.add_command(label="tabela Rota: Dados sendo inserindo no banco",command=self.sqlite_monitor)
        # filemenu.add_command(label="tabela spatial_ref_sys: Dados sendo inserindo no banco",command=self.sqlite_monitor)
        Menubar.add_cascade(label="Consultar", menu=filemenu0)
        filemenu0.add_command(label="Cultar os dados CSV do mapeamento por completo", command=self.sqlite_monitor)
        Menubar.add_cascade(label="Ambiente virtual", menu=filemenu3)
        filemenu3.add_command(label="Ativar windows", command=self.Ambiente_VirtualAtivarWindows)
        filemenu3.add_command(label="Desativar windows", command=self.Ambiente_VirtualDesativarWindows)
        filemenu3.add_command(label="Ativar linux", command=self.Ambiente_VirtualAtivarLinux)
        filemenu3.add_command(label="Desativar linux", command=self.Ambiente_VirtualDesativarLinux)
        Menubar.add_cascade(label="Funções", menu=filemenu2)
        filemenu2.add_command(label="Limpar campos", command=self.limpar_campos)
        filemenu2.add_command(label="Gerar Relatório", command=self.Gerar_Ficha)
        filemenu2.add_command(label="Salvar informações em arquivo de texto", command=self.salvar_info_texto)
        filemenu2.add_command(label="Download de pacotes", command=self.baixar_pacotes)
        filemenu2.add_command(label="Atualização de dependências", command=self.atualizar_dependencias)
        filemenu2.add_command(label="Geração de relatório estatístico", command=self.gerar_relatorio_estatistico)
        filemenu2.add_command(label="Deploy ao Github", command=self.deploy_github)
        filemenu2.add_command(label="Remover pastas da Rede", command=self.remover_pasta_rede)
        filemenu2.add_command(label="Resolver conflitos de dependências", command=self.resolver_conflitos)
        filemenu2.add_command(label="Remover dependências", command=self.remover_dependencias)
        filemenu2.add_command(label="Verificar a versão do projeto", command=self.verificar_versao)
        filemenu2.add_command(label="Consultar a documentação do projeto", command=self.consultar_documentacao)
        filemenu2.add_command(label="Deletar a documentação do projeto", command=self.deletar_documentacao)
        filemenu2.add_command(label="Gerar um arquivo executável do projeto", command=self.gerar_executavel)
        filemenu2.add_command(label="Executar o frontend da aplicação", command=self.executar_frontend)
        filemenu2.add_command(label="Verificar se há atualizações a serem feitas", command=self.verificar_atualizacoes)
        filemenu2.add_command(label="Remover pacotes ou dependências", command=self.remover_pacotes)
        filemenu2.add_command(label="FAQs", command=self.faq)
        filemenu2.add_command(label="Verificar logs de segurança", command=self.verificar_logs_seguranca)
        filemenu2.add_command(label="Agendar tarefas automatizadas", command=self.agendar_tarefas)
        filemenu2.add_command(label="Gerar relatórios estatísticos", command=self.gerar_relatorios_estatisticos)
        filemenu2.add_command(label="Apagar o projeto", command=self.apagar_projeto)
        Menubar.add_cascade(label="Avançado", menu=filemenu4)
        filemenu4.add_command(label="Acessar a API com o flask", command=self.flask_api)
        filemenu4.add_command(label="Abrir o dashboard no frontend com o streamlit", command=self.streamlit)
        
    
class Login:
    def __init__(self, root):
        self.root = root
        self.username = StringVar()
        self.password = StringVar()
        # Background Color
        self.root.config(bg="#5856a0")
        self.rightFrame = Frame(root, bg="#5856a0")
        self.rightFrame.pack(side=RIGHT)
        # Call the tkinter frame to the window
        self.loginControlFrame()
        # Database connection
        self.conn = sqlite3.connect(login)
        self.cursor = self.conn.cursor()

    """CTA Methods"""
    # login method to redirect to the next frames
    def loginFunc(self):
        username = self.txtUsername.get()
        password = self.txtPassword.get()

        # Query to fetch credentials from database
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()

        if result:
            self.loginFrame.destroy()
            self.rightFrame.destroy()
            Aplication()
        else:
            messagebox.showerror("Error!", "Check your credentials or Please Contact System Admin!")
            self.username.set("")
            self.password.set("")

    """Login Frame"""
    def loginControlFrame(self):
        # Login Frame Configurations
        self.loginFrame = Frame(self.root, bg="white")
        self.loginFrame.pack(side=LEFT, fill=X, padx=60)
        self.login_frame_title = Label(self.loginFrame, text="Login Here", font=("Impact", 35), bg="white", fg="#5856a0")
        self.login_frame_title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")
        # Username
        self.labelUsername = Label(self.loginFrame, text="Username", font=("Times New Roman", 16, "bold"), bg="white", fg="#5856a0")
        self.labelUsername.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.txtUsername = Entry(self.loginFrame, textvariable=self.username, font=("Times New Roman", 15), width=30, bd=5)
        self.txtUsername.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        # Password
        self.labelPassword = Label(self.loginFrame, text="Password", font=("Times New Roman", 16, "bold"), bg="white", fg="#5856a0")
        self.labelPassword.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.txtPassword = Entry(self.loginFrame, textvariable=self.password, font=("Times New Roman", 15), width=30, bd=5, show="*")
        self.txtPassword.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        # Login Button
        self.btnLogin = Button(self.loginFrame, command=self.loginFunc, text="Login", bd=0, cursor="hand2", fg="white", bg="#5856a0", width=10, font=("Impact", 15))
        self.btnLogin.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        # Exit Button
        self.btnExit = Button(self.loginFrame, text="Sair", command=self.root.destroy, bd=0, cursor="hand2", fg="white", bg="#5856a0", width=10, font=("Impact", 15))
        self.btnExit.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        """
        # Carregar a imagem
        self.image = Image.open("ibge.jpg")
        # Redimensionar a imagem usando o filtro LANCZOS
        self.image_resized = self.image.resize((200, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image_resized)
        # Adicionar a imagem redimensionada no frame
        self.labelImage = Label(self.rightFrame, image=self.photo, bg="#5856a0")
        self.labelImage.grid(row=0, column=2, columnspan=2, padx=10)
        """

        # Adicionar o nome "Mapeamento Shapefile" abaixo da imagem
        self.labelCompanyName = Label(self.rightFrame, text="Mapeamento Shapefile", font=("Goudy Old Style", 55), bg="#5856a0", fg="white")
        self.labelCompanyName.grid(row=1, column=2, columnspan=2, padx=10)
        self.labelDesc = Label(self.rightFrame, text="Mapeamento 1.0.0", font=("Times New Roman", 25, "italic"), bg="#5856a0", fg="white")
        self.labelDesc.grid(row=2, column=2, columnspan=2, padx=10, pady=6)


def main():
    global root
    root.title("Mapeamento Shapefile")
    # Maximiza a janela na inicialização
    maximize_window()
    # Vincula o evento de desiconizar a janela à função de maximização
    root.bind('<Map>', maximize_window)
    # Supondo que a classe Login esteja definida em outra parte do seu código
    Login(root)  # Parsing the root window to the Login class
    root.mainloop()


if __name__ == '__main__':
    main()