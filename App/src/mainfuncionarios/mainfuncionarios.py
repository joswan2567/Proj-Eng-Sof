DB_HOST ="ec2-3-227-149-67.compute-1.amazonaws.com"  
DB_NAME ="d3gdajkts88rvi"
DB_USER = "gdujgklsirqyxl"
DB_PASS = "587450b087c81af774131650ffa95e0b47793242ab89bb2adac05d4b8b46491e"
import psycopg2
import psycopg2.extras
conn = psycopg2.connect(host = DB_HOST, database = DB_NAME, user = DB_USER, password = DB_PASS, port = "5432")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel


class LayoutFuncionarios(TabbedPanel):  
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
    def deletarBD(self):
        id_excluir = self.id_excluir.text
        print(id_excluir)
        with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("DELETE FROM funcionario WHERE id_funcionario = %s",(id_excluir,))                
          conn.close
        pass
    def atualizacaoBD(self):
        id_update = self.id_update.text
        nome_update = self.nome_update.text
        telefone_update = self.telefone_update.text
        email_update = self.email_update.text
        funcao_update = self.funcao_update.text
        turno_update = self.turno_update.text
        print(id_update+" "+nome_update+" "+telefone_update+" "+funcao_update+" "+turno_update+" "+email_update)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("UPDATE funcionario SET (nome,telefone,funcao,turno,email) = (%s,%s,%s,%s,%s) WHERE id_funcionario = ( %s)", (nome_update,telefone_update,funcao_update,turno_update,email_update,id_update) )
            conn.close 

class FuncionariosApp(App):
    def build(self):
        return LayoutFuncionarios()

if __name__ == '__main__' :
    FuncionariosApp().run()