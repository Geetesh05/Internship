from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty,NumericProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import os
import pandas as pd
from ap import process
import sys 
#sys.path.append(os.path.abspath("/Users/geeteshgupta/Desktop/Project"))
class First(Screen):
    def store(self):
        global gc
        gc=self.thresh_hold.text
class Third(Screen):
    pass
class Fth(Screen):
    pass
class MainWindow(ScreenManager):
    gc = 0
    def file_load(self, path, filename):
        self.input_text1 = os.path.join(path, filename[0])

    def path_load(self, path, filename):
        self.input_text2 = os.path.join(path, filename[0])

    def method(self, instance, value, number):
        if value is True:
            self.val = number

    def printing(self):
            global gc
            process(self.input_text1 , self.input_text2 , self.val,gc)
            #process("/Users/geeteshgupta/Desktop/1.csv", "/Users/geeteshgupta/Desktop/1.txt" , self.val,gc)

k = Builder.load_file("main.kv")
class MainApp(App):


    def build(self):
        Window.clearcolor=(1,1,1,1)
        return k

if __name__ == '__main__':
    MainApp().run()




