DB_HOST ="ec2-3-227-149-67.compute-1.amazonaws.com"  
DB_NAME ="d3gdajkts88rvi"
DB_USER = "gdujgklsirqyxl"
DB_PASS = "587450b087c81af774131650ffa95e0b47793242ab89bb2adac05d4b8b46491e"
import psycopg2
import psycopg2.extras
conn = psycopg2.connect(host = DB_HOST, database = DB_NAME, user = DB_USER, password = DB_PASS, port = "5432")

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior

from kivy.uix.boxlayout import BoxLayout



class Gerenciador(ScreenManager):
    def autenticarLogin(self,p,login,senha):
        #login = self.login.text
        #senha = self.senha.text
        print(login+senha)
        cs = conn.cursor()
        cs.execute("SELECT * FROM Login l WHERE  l.login LIKE \'" + str(login) + "\' AND l.senha like \'" + str(senha) + "\' ORDER BY l.id_login ASC")
        senha_bd = cs.fetchall()
        
        if len(senha_bd) > 0:

            print(senha_bd)
            self.current = "telag"
            p.dismiss()

            #print(p.ids)
            #self.ids.login_pop.dismiss()
        else:
            
            p.ids.usuario.text = ""
            p.ids.senha.text = ""
            
        
    pass

class TelaPrincipal(Screen): 
    pass

class TelaLogin(Screen):
    

    pass

class TelaGerenciamento(Screen):
    pass

class TelaFunc(Screen):
    pass

class TelaFuncCadastro(Screen):
    def enviarBD(self):
        nome_inserir = self.nome_inserir.text
        telefone_inserir= self.telefone_inserir.text
        email_inserir= self.email_inserir.text
        funcao_inserir= self.funcao_inserir.text
        turno_inserir= self.turno_inserir.text
        print(nome_inserir + telefone_inserir + email_inserir + funcao_inserir + turno_inserir)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("INSERT INTO funcionario (nome,telefone,funcao,turno,email) VALUES (%s,%s,%s,%s,%s)",(nome_inserir,telefone_inserir,funcao_inserir,turno_inserir,email_inserir) )
            conn.close
        pass
    pass

class TelaFuncExcluir(Screen):
    def deletarBD(self):
        id_excluir = self.id_excluir.text
        print(id_excluir)
        with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("DELETE FROM funcionario WHERE id_funcionario = %s",(id_excluir,))                
          conn.close
        pass
    pass



    # def buscar(self, value):
    #     connection = conn
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM public.cliente WHERE nome LIKE '%" + value + "%'")
    #     rows = cursor.fetchall()
    #     self.data_items = []
    #     if len(rows) > 1:
    #         for row in rows:
    #             for col in row:
    #                 self.data_items.append(col)
    #     else:
    #         self.data_items.append("Não há dados compatíveis")
    #     print(self.data_items)

class TelaFuncListar(Screen):
    # data_items = ListProperty([])

    # def __init__(self, **kwargs):
    #     super(TelaFuncListar, self).__init__(**kwargs)
    #     self.get_users()
    #     pass

    # def get_users(self):
    #     connection = conn
    #     cursor = connection.cursor()

    #     cursor.execute("SELECT * FROM public.funcionario ORDER BY id_funcionario ASC")
    #     rows = cursor.fetchall()
    #     print(rows)
    #     for row in rows:
    #         for col in row:
    #             self.data_items.append(col)
    #     pass

    # def cd(self):  
    #     self.clear_widgets()
    #     TelaFuncListar().run()

    # title = "Funcionarios"
    # def build(self):
    pass    

class TelaCli(Screen):
    pass
class TelaCliCadastro(Screen):
    def enviarBDcli(self):
        nome_inserir = self.nome_inserir.text
        telefone_inserir= self.telefone_inserir.text
        email_inserir= self.email_inserir.text
        cpf_inserir= self.cpf_inserir.text
        tipo_inserir= 1 if self.tipo_inserir.text == "Normal" else 2
        print(nome_inserir + telefone_inserir + email_inserir + cpf_inserir + tipo_inserir)
        if nome_inserir != "":   
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute("INSERT INTO public.cliente (nome,telefone,email,cpf,id_tipo_cliente) VALUES (%s,%s,%s,%s,%s)",(nome_inserir,telefone_inserir,email_inserir,cpf_inserir,tipo_inserir) )
                conn.close
        pass
    pass
class TelaCliExcluir(Screen):
    pass
class TelaCliListar(Screen):
    pass

class principalApp(App): 
    def build(self):
        return Gerenciador()
principalApp().run()
