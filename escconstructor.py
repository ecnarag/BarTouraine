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

from main import *

def construct(fle):
    esc = Escadron()
    L = [{"lst":"Ababou","solde":7.2,"cns":0},
         {"lst": "Algeri", "solde":1.4,"cns":0},
         {"lst":"Aniort", "solde":25.7,"cns":0},
         {"lst":"Bonami","solde":4.4,"cns":0},
         {"lst":"Borrien","solde":114.9,"cns":0},
         {"lst":"Bouchareissas","solde":72.6,"cns":0},
         {"lst":"Boulant","solde":-80.2,"cns":0},
         {"lst":"Burdin", "solde":26.4,"cns":0},
         {"lst":"Chamorel","solde":-51.0,"cns":0},
         {"lst":"Cobo","solde":-1.9,"cns":0},
         {"lst":"Collin","solde":57.2,"cns":0},
         {"lst":"Delattre","solde":0.4,"cns":0},
         {"lst":"Desvignes","solde":-107.2,"cns":0},
         {"lst":"Dufourneau","solde":24.1,"cns":0},
         {"lst":"Duguet","solde":-70.8,"cns":0},
         {"lst":"Duval","solde":29.6,"cns":0},
         {"lst":"Encinas","solde":14.0,"cns":0},
         {"lst":"Favre","solde":44.8,"cns":0},
         {"lst":"Fricard","solde":-17.6,"cns":0},
         {"lst":"Gannier","solde":11.2,"cns":0},
         {"lst":"Gardan","solde":7.6,"cns":0},
         {"lst":"Gein","solde":-145.3,"cns":0},
         {"lst":"Gilot","solde":14.0,"cns":0},
         {"lst":"Girardet","solde":27.2,"cns":0},
         {"lst":"Gomes","solde":-141.2,"cns":0},
         {"lst":"Grand","solde":67.2,"cns":0},
         {"lst":"Gregoire","solde":-119.6,"cns":0},
         {"lst":"Grezes-Besset","solde":-2.7,"cns":0},
         {"lst":"Hebraud","solde":61.0,"cns":0},
         {"lst":"Herbreteau","solde":-140.6,"cns":0},
         {"lst":"Honecker","solde":90.0,"cns":0},
         {"lst":"Jacquiet","solde":53.4,"cns":0},
         {"lst":"Kuhlmann","solde":-74.4,"cns":0},
         {"lst":"Lafaille","solde":57.3,"cns":0},
         {"lst":"Laurent","solde":48.8,"cns":0},
         {"lst":"Leple","solde":-77.9,"cns":0},
         {"lst":"Mantion","solde":52.0,"cns":0},
         {"lst":"Marcelle","solde":24.2,"cns":0},
         {"lst":"Marie","solde":35.2,"cns":0},
         {"lst":"Mayakas","solde":23.0,"cns":0},
         {"lst":"Meillassoux","solde":2.0,"cns":0},
         {"lst":"Missey","solde":13.6,"cns":0},
         {"lst":"Ortet","solde":17.4,"cns":0},
         {"lst":"Paillard","solde":213.2,"cns":0},
         {"lst":"Pallares","solde":-148.0,"cns":0},
         {"lst":"Pelopidas","solde":90.5,"cns":0},
         {"lst":"Pierre","solde":51.8,"cns":0},
         {"lst":"Pineau","solde":-72.7,"cns":0},
         {"lst":"Pinot","solde":-96.8,"cns":0},
         {"lst":"Pourquier","solde":75.4,"cns":0},
         {"lst":"Schaffauser","solde":83.1,"cns":0},
         {"lst":"Segard","solde":91.0,"cns":0},
         {"lst":"Sochet","solde":10.3,"cns":0},
         {"lst":"Soutille","solde":2.7,"cns":0},
         {"lst":"Tatigne","solde":-29.6,"cns":0},
         {"lst":"Thouaille","solde":-49.8,"cns":0},
         {"lst":"Vasseur","solde":6.4,"cns":0},
         {"lst":"Vanzande","solde":96.4,"cns":0},
         {"lst":"Venard","solde":5.0,"cns":0},
         {"lst":"Weber","solde":18.4,"cns":0},
         {"lst":"Bellais","solde":3.6,"cns":0},
         {"lst":"De Chavigny","solde":7.4,"cns":0},
         {"lst":"Lebrun","solde":25.6,"cns":0},
         {"lst":"Lefer","solde":0.0,"cns":0},
         {"lst":"Gontier","solde":42.8,"cns":0},
         {"lst":"Perrot","solde":39.8,"cns":0},
         {"lst":"Dhalleine","solde":0.0,"cns":0},
         {"lst":"Teremate","solde":21.0,"cns":0},
         {"lst":"Auclerc","solde":28.0,"cns":0},
         {"lst":"Barbe","solde":2.8,"cns":0},
         {"lst":"Begoc","solde":4.0,"cns":0},
         {"lst":"Bernard","solde":0.0,"cns":0},
         {"lst":"Coterot","solde":9.0,"cns":0},
         {"lst":"De Boisseson","solde":17.0,"cns":0},
         {"lst":"Evrard","solde":14.4,"cns":0},
         {"lst":"Franzi","solde":0.0,"cns":0},
         {"lst":"Garrault","solde":10.2,"cns":0},
         {"lst":"Glet","solde":4.6,"cns":0},
         {"lst":"Gregoire","solde":13.0,"cns":0},
         {"lst":"Gwinner","solde":15.8,"cns":0},
         {"lst":"Herrier","solde":13.6,"cns":0},
         {"lst":"Jacconi","solde":0.0,"cns":0},
         {"lst":"Kudela","solde":0.0,"cns":0},
         {"lst":"Lefebvre","solde":0.0,"cns":0},
         {"lst":"Millet","solde":-9.0,"cns":0},
         {"lst":"Persico","solde":0.0,"cns":0},
         {"lst":"Philippe","solde":12.5,"cns":0},
         {"lst":"Quervel","solde":6.0,"cns":0},
         {"lst":"Stoeffel","solde":-0.8,"cns":0},
         {"lst":"Tessaro","solde":13.0,"cns":0},
         {"lst":"Thirion","solde":0.0,"cns":0},
         {"lst":"Toulon","solde":0.0,"cns":0},
         {"lst":"Wijas","solde":-8.8,"cns":0},
         {"lst":"Test","solde":0,"cns":0}]
    esc.pers = L
    esc.n = len(L)
    esc.saveEsc(fle)

construct(open("escadronfile.txt","wb"))
