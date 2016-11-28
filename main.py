from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty

class Bar(Widget):
    pass

class Conso(Widget):
    prix = NumericProperty(0)
    def setPrice(self,px):
        self.prix = px

class Personnel(Widget):
    grade = StringProperty("")
    name = StringProperty("Cordonnier")
    solde = NumericProperty(0)
    admin = BooleanProperty(False)

    def addMoney(self, money):
        self.solde += money

class BarApp(App):
    def build(self):
        return Bar()

if __name__ == '__main__':
    BarApp().run()
