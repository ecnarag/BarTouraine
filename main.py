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
J'ai essayé de commenter au maximum (un peu en franglais ...) et d'avoir des conventions assez réglo : saut de ligne après les définitions des classes et entre deux blocs, noms des fonctions avec des majusculesAuDébutDeChaqueMot, noms de variables explicites, donc ça devrait être compréhensible. N'hésitez pas à commenter au maximum et à faire le code le plus propre possible (factorisation de code et jolies conventions). Bonne chance !"""

"""Ordre des classes: Carte - Conso - Stats - Escadron - Personnel - BarApp.
La Carte contient les données générales sur les consos et la sérialization.
La Conso contient les attributs d'une conso (nom, prix, total d'utilisation).
Les Stats contiennent l'inventaire, les plus gros consommateurs, les plus mauvais payeurs, le total du bar et la fonction de remise à zéro.
L'Escadron contient la sérialisation et les fonctions générales sur les utilisateurs.
La classe Personnel contient les attributs d'un consommateur (nom, solde, nombre de consos ...) et les fonctions de consommation.
La classe BarApp est la classe "principale" qui contient les fonctions de démarrage et de fermeture de l'application."""

class Carte(GridLayout): #L'équivalent de Escadron -> Personnel pour les Consos

    g = ObjectProperty(GridLayout())
    cons = {}
    cons_widg = {}
    n = 0

    def saveCarte(self, fle): #Enregistrer la carte dans un fichier
       pickle.dump({"n":self.n, "cons":self.cons},fle)

    def loadCarte(self,fle): #Télécharger la carte depuis un fichier
        x = pickle.load(fle)
        self.n = x["n"]
        self.cons = x["cons"]

    def addConso(self,conso): #Ajouter un type de conso à la carte (inutilisé)
        n += 1
        cons[conso.name] = {"px":conso.prix, "tot":conso.total}

    def grid(self, perso): #Créer la grille de choix
        self.g = BoxLayout(orientation = 'horizontal')
        for i in self.cons.iteritems():
            butt = Conso(perso, i[1]["px"],i[0],i[1]["tot"], size_hint = (1.0/self.n, 1))
            self.cons_widg[i[0]] = butt
            self.g.add_widget(butt)
        return self.g

class Conso(Button):
#Everything is in the title

    def __init__(self, perso, px, nm, tot, **kwargs):

        self.prix = px
        self.perso = perso
        self.name = nm
        self.total = tot
        super(Conso,self).__init__(**kwargs)

class Stats(BoxLayout):
#Classe qui contient les statistiques de l'escadron (pour le moment plus gros consommateur, plus mauvais payeur. Autres idées?)

    def __init__(self,esc,carte,**kwargs):
        self.escadron = esc
        self.carte = carte
        super(Stats,self).__init__(**kwargs)

    def plusGrosConso(self): #Returns a list with the number of "consos" and names of the top 3 consumers (since the launching of the app)
        L = [(k["cns"],k["lst"]) for k in self.escadron.pers]
        L = list(reversed(sorted(L)))
        return L[:3]

    def plusMauvaisPayeur(self): #Returns a list with the "solde" and names of the top 3 most in debt (lower "soldes")
        L = [(k["solde"],k["lst"]) for k in self.escadron.pers]
        L = sorted(L)
        return L[:3]

    def totalBar(self):
        return sum([k["solde"] for k in self.escadron.pers])

    def inventaire(self):
        result = "\nConsommations :\n"
        for k in self.carte.cons.iteritems():
            result += k[0] + " : " + str(k[1]["tot"]) + "\n"
        return result

    def inventaireToZero(self):
        for k in self.carte.cons.iteritems():
            k[1]["tot"] = 0

    def press(self): #Function called when the Stats button is pressed
        a = self.plusGrosConso()
        b = self.plusMauvaisPayeur()
        pop = Popup(title = "Statistiques",
                    size_hint = (0.7,0.7),
                    content = Label(text = "Total du bar\n" + str(self.totalBar()) + "\n\n" + "Les trois plus gros consommateurs du bar sont :\n" + a[0][1] + "\n" + a[1][1] + "\n" + a[2][1] + "\n"
                            + "Les trois plus mauvais payeurs sont : \n" + b[0][1] + "\n" + b[1][1] + "\n" + b[2][1] + "\n"
                            + self.inventaire()))
        pop.open()

class Escadron(GridLayout):
#Pour afficher tout le monde dans une grille + enregistrer dans un fichier

    #Initialisation
    g = ObjectProperty(GridLayout())
    n = 0
    pers = []
    pers_widg = []

    def addPerso(self,perso): #Add someone to the Escadron
        self.n += 1
        self.pers.append({"lst":perso.last_name, "solde":perso.solde, "cns": perso.consos})
        self.pers_widg.append(perso)

    def removePerso(self, name):
        self.pers = list(filter(lambda x : x["lst"] != name.text, self.pers))
        self.pers_widg = list(filter(lambda x : x.last_name != name.text, self.pers_widg))
        self.n = len(self.pers)

    def removeButton(self):
        name = TextInput(multiline = False,
                        focus = True,
                        text = "")
        popup = Popup(title = "Supprimer un personnel",
                    size_hint = (0.2,0.2),
                    content = name)
        name.bind(on_text_validate = popup.dismiss)
        popup.bind(on_dismiss = lambda x : self.removePerso(name))
        popup.open()
        return name.text

    def addButton(self):
        name = TextInput(multiline = False,
                    focus = True,
                    text = "")
        popup = Popup(title = "Nouveau personnel",
                        size_hint = (0.2,0.2),
                        content = name)
        name.bind(on_text_validate = popup.dismiss)
        popup.bind(on_dismiss = lambda x: self.addPerso(Personnel(lst = name.text)))
        popup.open()
        return name.text

    def saveEsc(self,fle): #Save Escadron in a file
        for i in range(self.n): #Conversion Widgets -> Dicts to be pickable/unpickable
            k = self.pers_widg[i]
            self.pers[i] = {"lst":k.last_name, "solde":k.solde, "cns":k.consos} #Update values to make sure any changes are recorded
            #(We probably use the saveEsc function when closing the app)
        pickle.dump({"pers":self.pers, "n":self.n}, fle)

    def loadEsc(self,fle): #Load Escadron from a file
        x = pickle.load(fle)
        self.n = x["n"]
        self.pers = x["pers"]

    def grid(self): #Build grid
        self.g = GridLayout(cols = int(math.sqrt(self.n)))
        color = [(0,0,1,0.5),(0,0,1,0.6)]
        for i in range(len(self.pers)): #Add everyone in the grid
            k = self.pers[i]
            perso = Personnel(lst = k["lst"], sld = k["solde"], cns = k["cns"], background_color = color[(i%2)])
            self.pers_widg.append(perso)
            self.g.add_widget(self.pers_widg[i])
        return self.g

class Personnel(Button):
#Instance represents one user of the Bar app.

    global app
    solde = NumericProperty()

    def __init__(self, lst = "", sld = 0, cns = 0, **kwargs):
        self.last_name = lst
        self.consos = cns
        self.solde = sld
        super(Personnel,self).__init__(**kwargs) #Init of the "Button" instance

    def addMoney(self, money):
        assert money >= 0 #Don't fuck your friends
        self.solde += money

    def payCons(self, cons):
        app.card.cons[cons.name]["tot"] += 1
        self.solde -= cons.prix
        self.consos += 1

    def multipleCons(self,n,cons): #Payer plusieurs consos
        for k in range(n):
            self.payCons(cons)

    def action(self, cons): #Action des boutons buttcaf et buttcons: consommation et fermeture de la popup
        textinput = TextInput(multiline = False,
                                focus = True,
                                text = "0")
        popup2 = Popup(title = "Quantité de " + cons.name,
                        size_hint = (0.2,0.2),
                        content = textinput)
        textinput.bind(on_text_validate = popup2.dismiss)
        popup2.bind(on_dismiss = lambda x : self.multipleCons(int(textinput.text),cons))
        popup2.open()
        return textinput.text

    def actionask(self): #Action du bouton buttadd pour ajouter de l'argent: fermeture de popup et ouverture de popup2 avec un input utilisateur...
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

    def click(self): #Fonction appelée quand on clique sur son bouton
        carte = app.card.grid(self)
        content = BoxLayout(orientation = 'vertical', spacing = 10)
        if abs(self.solde) < 10**(-6): #Avant que j'ajoute ce test, les erreurs de calcul de python mettaient un "1.8E-14" au lieu de 0 (par exemple)
            self.solde = 0
        content.add_widget(Label(text = "Vous avez " + str(self.solde) + "€"))
        content.add_widget(carte)
        content.add_widget(Button(text = "Add\nmoney", on_press = lambda x : self.actionask()))
        popup = Popup(title = "Choisis ta conso, mon cher " + self.last_name,
                        size_hint = (0.3,0.5),
                        content = content)
        popup.open()

class BarApp(App):

    esc = ObjectProperty(Escadron())
    card = ObjectProperty(Carte())

    def build(self): #Ce que l'application fait quand elle démarre
        global app
        app = self
        self.esc = Escadron() #Construire un escadron
        self.esc.loadEsc(open("escadronfile.txt","rb"))
        self.root = root = self.esc.grid() #Construire une grille
        self.card = Carte()
        self.card.loadCarte(open("cartefile.txt","rb"))
        root.add_widget(Label()) #Une case vide pour séparer les noms du reste -- si on pouvait ajouter depuis la fin ça serait mieux
        #mais j'ai cru comprendre dans la doc de kivy que c'était impossible ...
        stat = Stats(self.esc, self.card) #Construire les statistiques
        root.add_widget(stat)
        box = BoxLayout(orientation = "horizontal")
        box.add_widget(Button(text = "Add", on_press = lambda x: self.esc.addButton()))
        box.add_widget(Button(text = "Remove", on_press = lambda x : self.esc.removeButton()))
        root.add_widget(box)
        return root

    def on_stop(self): #Ce que l'application fait quand on la ferme (sauvegarde des données)
        self.esc.saveEsc(open("escadronfile.txt","wb")) #Escadronfile est le fichier dans lequel toutes les données sont écrites (en binaire)
        self.card.saveCarte(open("cartefile.txt","wb"))

if __name__ == '__main__':
    BarApp().run()

"""COMMENTAIRES POUR MOI-MÊME:
Ce qui fonctionne :
- les boutons de consommation, quand on les définissait avec kivy
- le save/load de l'escadron dans un fichier avec pickle
- le changement de solde en appuyant sur un bouton
- les boutons sont bien définis
- le solde est mis à jour
- il y a un fichier loadé pour l'escadron
- les données sont sauvegardées quand l'app est fermée
- il y a un bouton statistiques
- l'appli est transférée sous android !!!
- gestion des stocks
- remise à zéro des stocks
- affichage en rouge des personnes en négatif
- ajouter/supprimer quelqu'un
- couleurs alternées
Ce qui ne fonctionne pas / ce qui reste à faire :
- important ? actualiser les nouvelles personnes
- faire autre chose que planter quand il y a un nombre négatif entré dans "add money"
- l'affichage est pas du tout optimisé pour mon téléphone, il faut voir ce que ça donne sur tablette
"""
