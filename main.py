import math
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class Bar(Widget):

    pass

class Conso:

    def __init__(self, px):
        self.prix = px

class Personnel(Widget):

    grade = StringProperty("ASP")
    first_name = StringProperty("Garance")
    last_name = StringProperty("Cordonnier")
    solde = NumericProperty(0)

    def addMoney(self, money):
        self.solde += money

    def payCons(self, cons):
        self.solde -= cons.prix

    def eatConso(self): #Fonction qui s'ouvre quand on clique sur son icone.
        #Pour mettre plusieurs contenus dans une popup, utiliser une BoxLayout.

        box = BoxLayout(orientation = 'horizontal', spacing = 10)
        buttcaf = Button(text = 'Cafe', size_hint = (0.3,1))
        buttcons = Button(text = 'Conso', size_hint = (0.3,1))
        buttadd = Button(text = 'Add mny', size_hint = (0.3,1))
        box.add_widget(buttcaf)
        box.add_widget(buttcons)
        box.add_widget(buttadd)

        popup = Popup(title = "Choisis ta conso",
                    size_hint = (0.2,0.2),
                    content = box)

        def action(cons): #Action des boutons buttcaf et buttcons: consommation et fermeture de la popup
            self.payCons(cons)
            popup.dismiss()

        def actionask(): #Action du bouton buttadd : fermeture de popup et ouverture de popup2 avec un input utilisateur...
            popup.dismiss()
            textinput = TextInput(multiline = False,
                                    focus = True,
                                    text = "0")
            popup2 = Popup(title = "Montant",
                            size_hint = (0.2,0.2),
                            content = textinput)
            textinput.bind(on_text_validate = popup2.dismiss)
            popup2.bind(on_dismiss = lambda x : self.addMoney(float(textinput.text)))
            popup2.open()
            return textinput.text

        buttadd.bind(on_press = lambda x : actionask())
        buttcons.bind(on_press = lambda x : action(Conso(0.8)))
        buttcaf.bind(on_press = lambda x : action(Conso(0.5)))
        popup.open()

class Escadron(Widget): #Pour permettre des trucs un peu globaux et surtout ajouter/retirer du personnel. (a completer pour le moment)

    n = NumericProperty(0)
    grid = ObjectProperty(None)
    pers = ListProperty([])

    def fillGrid(self):
        grid = GridLayout(cols = int(math.sqrt(len(self.pers))))
        for k in pers:
            self.grid.add_widget(perso)

    def addPerso(self,perso):
        self.pers.append(perso)
        grid.add_widget(perso)

class BarApp(App):

    def build(self):
        return Bar()

if __name__ == '__main__':
    BarApp().run()
