from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class Gerenciador(ScreenManager):
    pass
    #classe que ira gerenciar as telas.

class TelaPrincipal(Screen): 
    pass

class TelaLogin(Screen):
    pass

class TelaFunc(Screen):
    pass

class TelaCli(Screen):
    pass


class telas(App):
    def build(self):
        return Gerenciador()
telas().run()
