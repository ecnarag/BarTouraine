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
    c = Carte()
    L = { "Café": {"px": 0.5, "tot":0},
            "Bière": {"px":0.8,"tot":0},
            "Friandise":{"px":0.8,"tot":0},
            "Soft":{"px":0.8,"tot":0}
        }
    c.cons = L
    c.n = len(L)
    c.saveCarte(fle)

construct(open("cartefile.txt","wb"))
