DB_HOST ="ec2-3-227-149-67.compute-1.amazonaws.com"  
DB_NAME ="d3gdajkts88rvi"
DB_USER = "gdujgklsirqyxl"
DB_PASS = "587450b087c81af774131650ffa95e0b47793242ab89bb2adac05d4b8b46491e"

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.lang import Builder
import psycopg2
import psycopg2.extras

from kivy.uix.screenmanager import ScreenManager, Screen 

conn = psycopg2.connect(host = DB_HOST, database = DB_NAME, user = DB_USER, password = DB_PASS, port = "5432")
GUI = Builder.load_file('cliente-list.kv')

# class ScreenClienteList(Screen):
#     def build(self):
#         return ClienteListApp()

# class ScreenClienteApp(Screen):
#     def build(self):
#         return ClienteApp()

# class TelaManager(ScreenManager):
#     pass

class CadastrarApp(TabbedPanel):     

  def inserirDB(self, dados):
    nome = dados.nome.text
    telefone = dados.telefone.text
    email = dados.email.text
    cpf = dados.cpf.text
    tipo = 1 if dados.tipo.text == "Normal" else 2
    dados.nome.text = "coe"

    print(nome, telefone, email, cpf, tipo)
    if nome != "":
      print ("entrou")
      with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
              cur.execute("INSERT INTO public.cliente (nome,telefone,email,cpf,id_tipo_cliente) VALUES (%s,%s,%s,%s,%s)",(nome,telefone,email,cpf,tipo) )
          conn.close
    pass
  # def editarDB(self):
  #     id_fucionario = self.id_fucionario.int
  #     nome = self.nome.text
  #     telefone = self.telefone.text
  #     funcao = self.funcao.text
  #     turno = self.turno.text
  #     email = self.email.text
  #     print(nome)
  #     with conn:
  #       with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
  #         cur.execute("UPDATE cliente SET (nome,telefone,funcao,turno,email) = (%s,%s,%s,%s,%s) WHERE id_funcionario = 5", (nome,telefone,funcao,turno,email) )
  #       conn.close
  #     pass 

  # def deletarDB(self):
  #   id_fucionario = self.id_fucionario.int
  #   with conn:
  #     with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
  #       cur.execute("DELETE FROM cliente WHERE id_fucionario = %d", (id_fucionario,) )
  #     conn.close
  #   pass


  def back(self, root):
      root.clear_widgets()
      #Builder.unload_file('cliente.kv')
      #Builder.load_file('cliente-list.kv')
      ClienteListApp().run(); 

  # def setFuncao(self, value):
  #     self.ids.funcao.text = value

class ClienteApp(App):
  def build(self):
    return CadastrarApp()

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt

class RV(BoxLayout):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_users()

    def get_users(self):
        connection = conn
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM public.cliente ORDER BY id_cliente ASC")
        rows = cursor.fetchall()
        print(rows)
        # create data_items
        for row in rows:
            for col in row:
                self.data_items.append(col)

    def cd(self):  
        self.clear_widgets()
        Builder.load_file('cliente.kv')
        ClienteApp().run()

    def buscar(self, value):
        connection = conn
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.cliente WHERE nome LIKE '%" + value + "%'")
        rows = cursor.fetchall()
        self.data_items = []
        if len(rows) > 1:
            for row in rows:
                for col in row:
                    self.data_items.append(col)
        else:
            self.data_items.append("Não há dados compatíveis")
        print(self.data_items)

class ClienteListApp(App):
    title = "Clientes"

    def build(self):
        return RV()

if __name__ == "__main__":
    ClienteListApp().run()

