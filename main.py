#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle #Serializer
import math #Math functions

#Every module we need from kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


from kivy.core.window import Window

""" Informations pour toi, cher lecteur/modificateur de mon code.
Cette application a été développée par Garance Cordonnier, X2016, pour le bar du Touraine.
Il faut installer le module python KIVY (pip install kivy), le code est écrit pour Python 2 (oui, je sais, c'est sale,mais python3 ne fonctionnait pas avec kivy).
Conseils pour le code : utilisez un gestionnaire de versions (j'ai utilisé GIT, niquel pour Linux et MacOS, existe aussi sous Windows) pour enregistrer vos modifications et garder un historique des versions précédentes, la doc kivy est en ligne à https://kivy.org/docs/ avec beaucoup d'exemples, beaucoup de réponses à vos questions sont sur le forum StackOverflow, la doc du module pickle est en ligne à https://docs.python.org/2/library/pickle.html et la plupart des modules écrits pour python ont leur doc sur https://anaconda.org.
J'ai essayé de commenter au maximum (un peu en franglais ...) et d'avoir des conventions assez réglo : saut de ligne après les définitions des classes et entre deux blocs, noms des fonctions avec des majusculesAuDébutDeChaqueMot, noms de variables explicites, donc ça devrait être compréhensible. Bonne chance !"""


class Conso: #Everything is in the title

    def __init__(self, px):
        self.prix = px

class Escadron(GridLayout): #Pour permettre des trucs un peu globaux et surtout ajouter/retirer du personnel. (a completer pour le moment)

    #Initialisation
    g = ObjectProperty(GridLayout())
    n = 4
    pers = [{"grade":"ASP", "fst":"Garance", "lst":"Cordonnier","solde":0},
            {"grade":"ASP","fst":"Vincent","lst":"Ren","solde":0},
            {"grade":"ASP", "fst":"Lala", "lst":"Toto", "solde":15},
            {"grade":"", "fst":"","lst":"Blu", "solde":0}]
    pers_widg = []

    def addPerso(self,perso): #Add someone to the Escadron
        print(self.n, perso.last_name)
        self.n += 1
        self.pers.append(perso.dic)

    def saveEsc(self,fle): #Save Escadron in a file
        for i in range(len(self.pers_widg)): #Conversion Widgets -> Dicts to be pickable/unpickable
            k = self.pers_widg[i]
            self.pers[i] = {"grade": k.grade, "lst":k.last_name, "fst":k.first_name, "solde":k.solde} #Update values to make sure any changes are recorded
            #(We probably use the saveEsc function when closing the app)
        x = {"n": self.n, "pers": self.pers}
        pickle.dump({"pers":self.pers, "n":self.n}, fle)

    def loadEsc(self,fle): #Load Escadron from a file
        x = pickle.load(fle)
        self.n = x["n"]
        self.pers = x["pers"]

    def grid(self): #Build grid
        self.g = GridLayout(cols = int(math.sqrt(self.n)))
        for i in range(len(self.pers)): #Add everyone in the grid
            k = self.pers[i]
            perso = Personnel(gde = k["grade"], lst = k["lst"], fst = k["fst"], sld = k["solde"])
            self.pers_widg.append(perso)

            def update_solde(instance, value): #To make sure that the apparent "solde" is equal to the actual "solde". (Bind the two values)
                perso.children[0].text = str(perso.solde)
            perso.bind(solde = update_solde)

            self.g.add_widget(self.pers_widg[i])
        return self.g

class Personnel(Button): #Instance represents one user of the Bar app.

    solde = NumericProperty()

    def __init__(self, gde = "", fst = "", lst = "Toto", sld = 0, **kwargs):
        self.grade = gde
        self.first_name = fst
        self.last_name = lst
        self.solde = sld
        super(Personnel,self).__init__(**kwargs)

    def addMoney(self, money):
        assert money >= 0 #Don't fuck your friends
        self.solde += money

    def payCons(self, cons):
        self.solde -= cons.prix

    def eatConso(self): #Fonction qui s'ouvre quand on clique sur son icone.
        #Pour mettre plusieurs contenus dans une même popup, utiliser une BoxLayout.
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

        def actionask(): #Action du bouton buttadd pour ajouter de l'argent: fermeture de popup et ouverture de popup2 avec un input utilisateur...
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

class BarApp(App):

    esc = ObjectProperty(Escadron())

    def build(self):
        self.esc = Escadron()
        self.esc.loadEsc(open("escadronfile.txt","rb"))
        g = self.esc.grid()
        g.add_widget(Label(text = "Bienvenue au bar du Touraine !"))
        return g

    def on_stop(self):
       self.esc.saveEsc(open("escadronfile.txt","wb"))

if __name__ == '__main__':
    BarApp().run()

"""COMMENTAIRES POUR MOI-MÊME:
Aujourd'hui, j'ai transformé le truc pour ajouter perso par perso en un truc qui ajoute un escadron direct, sous forme de GridLayout, mais ça marche moyennement : les boutons ne se réfèrent pas à la personne et je ne sais pas comment actualiser la string affichée (elle affiche toujours le solde 0€ contrairement à ce que fait le .kv, cf https://kivy.org/docs/guide/lang.html ce qu'ils disent sur les GridLayout, mais je ne sais pas quoi mettre comme setter où).
Résultat : rien ne marche, mais on avance quand même, en théorie.
Ce qui fonctionne :
- les boutons de consommation, quand on les définissait avec kivy
- le save/load de l'escadron dans un fichier avec pickle
- le changement de solde en appuyant sur un bouton
- les boutons sont bien définis
- le solde est mis à jour
- il y a un fichier loadé pour l'escadron
- les données sont sauvegardées quand l'app est fermée
Ce qui ne fonctionne pas / ce qui reste à faire :
- le dernier bouton a un comportement bizarre quand on l'utilise (le nom et le "€" disparaissent mais le solde est bien actualisé)
- faire autre chose que planter quand il y a un nombre négatif entré dans "add money"
- l'appli n'est pas transférée sous android !!!!!
- il reste toute la déco à gérer"""
