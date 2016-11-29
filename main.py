from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class Bar(Widget):

    pass

class Conso:

    def __init__(self, px):
        self.prix = px

class Personnel(Widget):

    grade = StringProperty("")
    first_name = StringProperty("")
    last_name = StringProperty("")
    solde = NumericProperty(0)

    def addMoney(self, money):
        self.solde += money

    def payCons(self, cons):
        self.solde -= cons.prix

    def eatConso(self):
        #Pour mettre plusieurs contenus dans une popup, utiliser une BoxLayout.
        box = BoxLayout()
        buttcaf = Button(text = 'Cafe')
        buttcons = Button(text = 'Conso')
        box.add_widget(buttcaf)
        box.add_widget(buttcons)
        popup = Popup(title = "Choisis ta conso",
                    size_hint = (0.2,0.2),
                    content = box)
        def action(cons):
            self.payCons(cons)
            popup.dismiss()
        #Pour une raison quelconque la touche cafe paye les deux consos, d'ou le 0.3
        buttcons.bind(on_touch_down = lambda x,y : action(Conso(0.8)))
        buttcaf.bind(on_touch_down = lambda x,y : action(Conso(-0.3)))
        popup.open()

class Escadron:

    def __init__(self):
        self.pers = []

    def addPerso(self,pers):
        self.pers.append(pers)

class BarApp(App):

    def build(self):
        return Bar()

if __name__ == '__main__':
    BarApp().run()
