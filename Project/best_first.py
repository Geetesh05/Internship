import pandas as pd
from matplotlib import *
import matplotlib.pyplot as plt
from functools import partial
from scipy import stats
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import numpy as np
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from scipy.spatial import ConvexHull
from shapely.geometry import Point, Polygon
import time
from sklearn.neighbors import NearestNeighbors
from kivy.properties import StringProperty
from matplotlib.path import Path
from matplotlib.patches import Polygon as pol
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from sklearn.preprocessing import normalize
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, NavigationToolbar2Kivy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from matplotlib import use as mpl_use
from scipy.special import comb

#import mplcursors

mpl_use('module://kivy.garden.matplotlib.backend_kivy')
class Node:
    def __init__(self, name):
        self.parent = name
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


def Combination(a, combi, n, r, depth, index, val, parent):
    global dic, run
    if index == r:
        x = []
        x = x + combi
        if str(x[0]) == str(parent):
            if len(x) == 3:
                T, m, n, o, p = scoring(x, val)
                if T < run[len(x)]:
                    pval(m, n, o, p, x)
                    dic[len(x)] = x[len(x) - 1]
                    run[len(x)] = T

            else:
                if str(x[len(x) - 2]) == str(dic[len(x) - 1]):
                    T, m, n, o, p = scoring(x, val)
                    if T < run[len(x)]:
                        pval(m, n, o, p, x)
                        dic[len(x)] = x[len(x) - 1]
                        run[len(x)] = T

        return

    for i in range(depth, n):
        combi[index] = a[i]
        Combination(a, combi, n, r, i + 1, index + 1, val, parent)


def bottom_up(root, val):
    t = []
    t.append(root.parent)
    for i in root.children:
        t.append(i)
    for i in range(len(t) + 1):
        combi = [0] * i
        if len(combi) > 2:
            Combination(t, combi, len(t), i, 0, 0, val, root.parent)


def scoring(a, b):
    global file1,file2
    xv = []
    yv = []
    hull = ConvexHull(a)
    for i in hull.vertices:
        xv.append(a[i])

    poly = Polygon(xv)
    pathe = Path([(i[0], i[1]) for i in poly.exterior.coords], closed=True)
    score = 0  # points inside
    scoree = 0  # pathway inside #score_s
    for i in file1[b]:
        if poly.contains(Point(i)) == True:
            scoree = scoree + 1

    z = pathe.contains_points(file2)
    for i in z:
        if i == True:
            score = score + 1
    large_n = len(file2)
    small_n = len(file1[b])
    scoree_out = abs(len(file1[b]) - len(a) - scoree)
    score = abs(score - scoree)
    score_out = len(file2) - score - scoree - scoree_out
    score_limit = comb(scoree + score + small_n, small_n) / comb(large_n, small_n)
    return score_limit, scoree, scoree_out, score, score_out


def pval(a, b, c, d, e):
    global tempp, minarr
    x, p = stats.fisher_exact([[a, b], [c, d]])
    if p < tempp:
        tempp = p
        minarr=e

class Nn(App):

    def build(self):
        global huling, dur
        self.box = RelativeLayout()
        fig, ax = plt.subplots()
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.plot(file2[:, 0], file2[:, 1], "o")
        for i, k in zip(range(len(huling)), range(len(dur))):
            for simplex in huling[i]:
                ax.plot(np.array(dur[k])[simplex, 0], np.array(dur[k])[simplex, 1], marker='o', linestyle='-',
                        markerfacecolor="blue", color='red')

        self.win = fig.canvas
        # FigureCanvasKivyAgg(fig.canvas, size_hint=(1, 0.9), pos_hint={"top": 1})
        self.box.add_widget(self.win)
        self.one = NavigationToolbar2Kivy(self.win)
        self.box1 = BoxLayout(orientation="horizontal")
        self.box1.add_widget(self.one.actionbar)
        self.box2 = BoxLayout(orientation="horizontal")
        # self.box2=GridLayout()
        self.bt3 = Button(text="scores plot", size_hint=(0.15, 0.06), pos=(0, 0))
        self.bt4 = Button(text="pathway list", size_hint=(0.15, 0.06), pos=(1, 0))
        self.box2.add_widget(self.bt3)
        self.bt3.bind(on_press=self.pop1)
        self.bt4.bind(on_press=self.pop)
        self.box2.add_widget(self.bt4)
        self.box.add_widget(self.box1)
        self.box.add_widget(self.box2)
        self.pop_up1 = Popup(title="Visvualization", content=self.box)
        self.pop_up1.open()

    def pop(self, button):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        title = "List of pathways"
        b = []
        for i in range(len(file3)):
            b.append(Button(text=str(i + 1) + ". " + file3[i], size_hint_y=None))
            layout.add_widget(b[i])
            b[i].bind(on_press=partial(self.specific, i))

        # for i in range(len(file3)):
        # layout.add_widget(Button(text=str(i+1)+". "+file3[i],size_hint_y=None))
        closeButton = Button(text="Close the pop-up", size_hint_y=None)
        layout.add_widget(closeButton)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(layout)
        self.pop_up = Popup(title=title, content=root, size_hint=(1, 1))
        self.pop_up.open()
        closeButton.bind(on_press=self.pop_up.dismiss)

    def pop1(self, button):
        self.boxp1 = RelativeLayout()
        fig1, ax1 = plt.subplots()
        ax1.set_xlabel("PC1")
        ax1.set_ylabel("PC2")
        for k in range(len(file4)):
            ax1.plot(file4[k][0], file4[k][1], marker="o", color="blue")
        self.win1 = fig1.canvas
        # FigureCanvasKivyAgg(ax1.gcf(), size_hint=(1, 0.9), pos_hint={"top": 1})
        self.boxp1.add_widget(self.win1)
        closeButton1 = Button(text="Close the pop-up", size_hint=(0.15, 0.06), pos=(0, 0))
        self.one1 = NavigationToolbar2Kivy(self.win1)
        self.boxp1.add_widget(self.one1.actionbar)
        self.boxp1.add_widget(closeButton1)
        self.pop_upp = Popup(title="Visualization", content=self.boxp1)
        self.pop_upp.open()
        closeButton1.bind(on_press=self.pop_upp.dismiss)

    def specific(self, index, unused):
        self.boxp2 = RelativeLayout()
        fig2, ax2 = plt.subplots()
        ax2.set_xlabel("PC1")
        ax2.set_ylabel("PC2")
        ax2.plot(file2[:, 0], file2[:, 1], "o")
        for j in huling[index]:
            ax2.plot(np.array(dur[index])[j, 0], np.array(dur[index])[j, 1], marker='o', linestyle='-',
                     markerfacecolor="blue", color='red')
        self.win2 = fig2.canvas
        # FigureCanvasKivyAgg(ax1.gcf(), size_hint=(1, 0.9), pos_hint={"top": 1})
        self.boxp2.add_widget(self.win2)
        closeButton2 = Button(text="Close the pop-up", size_hint=(0.3, 0.1), pos=(0, 0))
        self.one2 = NavigationToolbar2Kivy(self.win2)
        self.boxp2.add_widget(self.one2.actionbar)
        self.boxp2.add_widget(closeButton2)
        self.pop_up2 = Popup(title="Visualization", content=self.boxp2)
        self.pop_up2.open()
        closeButton2.bind(on_press=self.pop_up2.dismiss)


def bfs(a,b,c,d):
    global file1, file2, huling, tempp, run, dic,minarr, support, file3,file4,dur
    file1 = a
    file2 = b
    file3=c
    file4=d
    huling=[]
    dur=[]
    for l in range(len(a)):
        X = a[l]
        dic = {}
        tempp=999
        minarr=[]
        hulk=[]
        element={}
        for i in range(len(X)):
            element[i] = 0
        for i in range(len(X)):
            run = {}
            for k in range(len(X) + 1):
                run[k] = 1
                dic[k] = 0

            root = Node(X[i])
            for j in range(len(X)):
                if i != j and element[j] == 0:
                    root.add_child(X[j])
            element[i] = 1
            bottom_up(root, l)
        print("complete", l)
        if len(minarr)>2:
            hull1=ConvexHull(minarr)
            for i in hull1.simplices:
                hulk.append(i)

        huling.append(hulk)
        dur.append(minarr)


    Nn().run()
