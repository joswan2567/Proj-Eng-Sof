DB_HOST ="ec2-3-227-149-67.compute-1.amazonaws.com"  
DB_NAME ="d3gdajkts88rvi"
DB_USER = "gdujgklsirqyxl"
DB_PASS = "587450b087c81af774131650ffa95e0b47793242ab89bb2adac05d4b8b46491e"

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(host = DB_HOST, database = DB_NAME, user = DB_USER, password = DB_PASS, port = "5432")

Builder.load_file('funcionarios.kv')
#teste

class MyLayout(TabbedPanel):  
  nome = ObjectProperty(None)
  telefone = ObjectProperty(None)
  funcao = ObjectProperty(None)
  turno = ObjectProperty(None)
  email = ObjectProperty(None)       

  def inserirDB(self):
    nome = self.nome.text
    telefone = self.telefone.text
    funcao = self.funcao.text
    turno = self.turno.text
    email = self.email.text

    print(nome,telefone,funcao,turno,email)
    if nome != "":
      print ("entrou")
      with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
              cur.execute("INSERT INTO funcionario (nome,telefone,funcao,turno,email) VALUES (%s,%s,%s,%s,%s)",(nome,telefone,funcao,turno,email) )
          conn.close
    pass

  def editarDB(self):
      id_fucionario = self.id_fucionario.int
      nome = self.nome.text
      telefone = self.telefone.text
      funcao = self.funcao.text
      turno = self.turno.text
      email = self.email.text
      print(nome)
      with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
          cur.execute("UPDATE funcionario SET (nome,telefone,funcao,turno,email) = (%s,%s,%s,%s,%s) WHERE id_funcionario = 5", (nome,telefone,funcao,turno,email) )
        conn.close
      pass 
  def deletarDB(self):
    id_fucionario = self.id_fucionario.int
    with conn:
      with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("DELETE FROM funcionario WHERE id_fucionario = %d", (id_fucionario,) )
      conn.close
    pass




class FuncionariosApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__' :
    FuncionariosApp().run()