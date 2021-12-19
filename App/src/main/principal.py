DB_HOST ="ec2-3-227-149-67.compute-1.amazonaws.com"  
DB_NAME ="d3gdajkts88rvi"
DB_USER = "gdujgklsirqyxl"
DB_PASS = "587450b087c81af774131650ffa95e0b47793242ab89bb2adac05d4b8b46491e"
from kivy.app import App
import psycopg2
import psycopg2.extras
conn = psycopg2.connect(host = DB_HOST, database = DB_NAME, user = DB_USER, password = DB_PASS, port = "5432")

from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


dt_items=[]

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton, self).__init__(**kwargs)
        # print(self.text)
        # if self.text is "Editar":
        #     self.text = ""
        #     img = Image(source="ListaPNG.png")
        #     self.append(img)
        pass

    # def _do_release(self, *args):
    #     print(self.text)
    #     if self.text is "Editar":
    #         self.text = ""
    #         img = Image(source="ListaPNG.png")
    #         self.append(img)
    #     return super()._do_release(*args)
        
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

    # def on_press(self):
    #     # popup = TextInputPopup(self)
    #     # popup.open()

    def update_changes(self, txt):
        self.text = txt

class Gerenciador(ScreenManager):
    def autenticarLogin(self,p,login,senha):
        
        # p.dismiss()
        # self.current = "telag"
        print(login+senha)
        cs = conn.cursor()
        cs.execute("SELECT * FROM Login l WHERE  l.login LIKE \'" + str(login) + "\' AND l.senha like \'" + str(senha) + "\' ORDER BY l.id_login ASC")
        senha_bd = cs.fetchall()        

        if len(senha_bd) > 0:

            print(senha_bd)
            self.current = "telag"
            p.dismiss()
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

class PopupBoleto(Popup):
    obj = ObjectProperty(None)
    total = StringProperty("")
    nmr_vg = StringProperty("")
    entrada = StringProperty("")
    saida = StringProperty("")

    def __init__(self, obj, **kw):
        super(PopupBoleto, self).__init__(**kw)
        self.obj = obj
        self.nmr_vg = str(obj[0])
        self.entrada = str(obj[2])
        self.saida = str(obj[3])
        self.total = str(obj[4])

class TelaPagamento(Screen):

    dt_it = []

    def __init__(self, **kw):
        super().__init__(**kw)
        self.get_vgs_ocup()
        pass

    def get_vgs_ocup(self):
        connection = conn
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT vc.id_vaga, v.numero, c.placa, cl.nome, vc.entrada, vc.saida "
                "FROM vaga_cliente vc "
                "INNER JOIN vaga v ON v.id_vaga = vc.id_vaga_cliente "
                "INNER JOIN carro c ON c.id_carro = vc.id_carro_cliente "
                "INNER JOIN carro_cliente cc ON cc.id_carro_cliente = c.id_carro "
                "INNER JOIN cliente cl ON cl.id_cliente = cc.id_cliente "
                "WHERE vc.status LIKE 'Aberta' "
                "ORDER BY vc.id_vaga ASC");
            connection.commit()
            rows = cursor.fetchall()
            print(rows)
            for row in rows:
                for col in row:
                    self.dt_it.append(col)
            print(self.dt_it)
        except :
            print('Error Req')

    def gerar_valor(self, id_vaga, tabela):
        connection = conn
        cursor = connection.cursor()
        # try:
        cursor.execute(
            "SELECT * from calc_bol(%s)", str(id_vaga));
        connection.commit()
        rows = cursor.fetchall()
        print(list(rows[0]))
        popup = PopupBoleto(list(rows[0]))
        popup.open()
        self.get_vgs_ocup()
        tabela.refresh_from_data()

        # except:
        #     print('Error Req')

class TelaFuncCadastro(Screen):
    def enviarBD(self):
        nome_inserir = self.nome_inserir.text
        telefone_inserir= self.telefone_inserir.text
        email_inserir= self.email_inserir.text
        funcao_inserir= self.funcao_inserir.text
        turno_inserir= self.turno_inserir.text
        # acesso_inserir =  self.checkbox.text
        # print(nome_inserir + telefone_inserir + email_inserir + funcao_inserir + turno_inserir+acesso_inserir)
        print(nome_inserir + telefone_inserir + email_inserir + funcao_inserir + turno_inserir)
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                # cur.execute("INSERT INTO funcionario (nome,telefone,funcao,turno,email,acesso) VALUES (%s,%s,%s,%s,%s,%s)",(nome_inserir,telefone_inserir,funcao_inserir,turno_inserir,email_inserir,acesso_inserir) )
                cur.execute("INSERT INTO funcionario (nome,telefone,funcao,turno,email,acesso) VALUES (%s,%s,%s,%s,%s)",(nome_inserir,telefone_inserir,funcao_inserir,turno_inserir,email_inserir) )

            conn.close
        pass
    pass

class TelaFuncExcluir(Screen):
    def deletarBD(self):
        id_excluir = self.id_excluir.text
        print(id_excluir)
        with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("DELETE FROM funcionario WHERE id_funcionario = %s",(id_excluir))                
          conn.close
        pass
    pass

class TelaFuncListar(Screen):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TelaFuncListar, self).__init__(**kwargs)
        self.get_users()
        pass

    def get_users(self):
        connection = conn
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM public.funcionario ORDER BY id_funcionario ASC")
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            for col in row:
                self.data_items.append(col)
            self.data_items.append("Editar")
        pass

    def cd(self):  
        self.clear_widgets()
        TelaFuncListar().run()

    title = "Funcionarios"
    def build(self):
        pass    

class TelaCli(Screen):
    pass

class TelaCliCadastro(Screen):
    def enviarBDcli(self):
        print("funcao enviarBDcliente")
        nome_inserir = self.nome_inserir.text
        telefone_inserir= self.telefone_inserir.text
        email_inserir= self.email_inserir.text
        cpf_inserir= self.cpf_inserir.text
        tipo_inserir= 1 if self.tipo_inserir.text == "Normal" else 2
        print(nome_inserir + telefone_inserir + email_inserir + cpf_inserir)
        if ((nome_inserir != "") and (telefone_inserir != "") and (email_inserir != "") and (cpf_inserir != "") and (tipo_inserir != "")):   
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute("INSERT INTO public.cliente (nome,telefone,email,cpf,id_tipo_cliente) VALUES (%s,%s,%s,%s,%s)",(nome_inserir,telefone_inserir,email_inserir,cpf_inserir,tipo_inserir) )
                conn.close
            
        else:
            print("Campo Invalido!")
    pass

class TelaCliExcluir(Screen):
    def deletarBDcli(self):
        id_excluir = self.id_excluir.text
        print(id_excluir)
        with conn:
          with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("DELETE FROM public.cliente WHERE id_cliente = %s",(id_excluir,))                
          conn.close
        pass
    pass
    pass

class TelaCliListar(Screen):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(TelaCliListar, self).__init__(**kwargs)
        self.get_users()

    def get_users(self):
        dt_items.clear()
        connection = conn
        cursor = connection.cursor()

        cursor.execute("SELECT c.id_cliente, c.id_tipo_cliente, c.nome, c.cpf, c.telefone, c.email FROM public.cliente c WHERE c.deletado = false ORDER BY id_cliente ASC")
        rows = cursor.fetchall()
        # print(rows)
        # create data_items
        for row in rows:
            for col in row:
                dt_items.append(col)
        self.data_items = dt_items

    def cd(self):  
        self.clear_widgets()
        TelaCliListar().run()

    title = "Funcionarios"
    def build(self):
        pass    
    pass

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    id = StringProperty("")
    id_cliente = StringProperty("")
    nome = StringProperty("")
    telefone = StringProperty("")
    cpf = StringProperty("")
    email = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        # print(obj.data)
        self.obj = obj
        self.id = str(obj.data[0])
        self.id_cliente = str(obj.data[1])
        self.nome = str(obj.data[2])
        self.telefone = str(obj.data[3])
        self.cpf = str(obj.data[4])
        self.email = str(obj.data[5])
    
    def save(self, lt):
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                print(self.id)
                print(self.id_cliente)
                print(self.nome)
                print(self.telefone)
                print(self.cpf)
                print(self.email)
                cur.execute(
                    "UPDATE cliente c " 
                    "SET (nome,telefone,cpf,email) = (%s,%s,%s,%s) " 
                    "WHERE c.id_cliente = %s", 
                    (self.nome, self.telefone, self.cpf, self.email, self.id));
                conn.commit()
            conn.close
            lt.get_users()
            lt.ids.lt_cliente.refresh_from_data()
            lt.ids.bt_act_cliente.refresh_from_data()
        except psycopg2.Error as e:
            print('Error banco :' + str(e))
        # print(lt)
        self.dismiss()
  
class ButtonActions(BoxLayout):
    data = []
    def edit(self, init):
        self.data = list(dt_items[init:init+6])
        popup = TextInputPopup(self)
        popup.open()

    def delete(self, lt):
        id = str(lt.ids.telaclilistar.data_items[self.id * 6])
        print(id)
        print(lt.ids.telaclilistar.data_items)
        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    print(id)
                    cur.execute("UPDATE cliente c SET deletado = true WHERE c.id_cliente =" + str(id))
                    # cur.commit()
                    # cur.execute("SELECT * FROM calc_bol(1)")
            conn.close
            lt.ids.telaclilistar.get_users()
            print(lt)
            print(lt.ids.telaclilistar.ids)
            lt.ids.telaclilistar.ids.lt_cliente.refresh_from_data()
            lt.ids.telaclilistar.ids.bt_act_cliente.refresh_from_data()
        except psycopg2.Error as e:
            print('Erro banco: ' + str(e))
  
class ButtonActionsFunc(BoxLayout):
    data = []
    def edit(self, init):
        self.data = list(dt_items[init:init+6])
        popup = TextInputPopup(self)
        popup.open()

    def delete(self, lt):
        print(self.id+1)
        id = str(self.id+1)
        # with conn:
        #     with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        #         # cur.execute("DELETE FROM cliente WHERE id_cliente = %s", (id))
        #         # cur.execute("SELECT * FROM calc_bol(1)")
        # conn.close
        lt.get_users()
        lt.ids.lt.refresh_from_data()
        lt.ids.bt_act.refresh_from_data()

class principalApp(App): 
    def build(self):
        return Gerenciador()
principalApp().run()
