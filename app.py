import kivy
kivy.require('1.10.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.properties import ListProperty
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from math import sqrt

class MyPolygon():
    def __init__(self, points):
        self.points = points[:]
    
    def get_points(self):
        return self.points

    def is_inside(self, point):
        raise NotImplementedError
    
    def change_x_y(self, nx, ny):
        self.x = nx
        self.y = ny
    
    def draw(self,canvas):
        print(canvas)
        with canvas:
            Line(points=self.points, width=2)


class MyCanvas(Widget):
    polygons = []
    def __init__(self, **kwargs):
        super(MyCanvas, self).__init__(**kwargs)
        self.paintColor = (1,1,1)
        print(self.pos)
        print(self.width,self.height)
        # self.bind(size=self.refresh)
        self.adding_poly_mode = False
        self.new_points = []

    def refresh(self, *args):
        width = self.width
        height = self.height
        self.canvas.clear()
        for polygon in self.polygons:
            polygon.draw(self.canvas)
        # print(self)
        print(self.parent)

    def is_close_to_startpoint(self,added_points, point, min_dist = 10):
        if (len(added_points)) < 3:
            return False
        start = added_points[0]
        if ((start[0] - point[0])**2 + (start[1] - point[1])**2) < (min_dist**2):
            return True
        return False
               
    def on_touch_down(self, touch):
        # Rectangle(pos=touch.pos, size=(10,10))
        if self.collide_point(touch.pos[0], touch.pos[1]):
            print("canvas sizem width:{} and height {}".format(self.width, self.height))
            self.refresh()
            if (self.adding_poly_mode):
                if (not self.is_close_to_startpoint(self.new_points,[touch.x, touch.y])):
                    self.new_points.append([touch.x, touch.y])
                else:
                    self.new_points.append(self.new_points[0])
                    self.adding_poly_mode = False
                    self.polygons.append(MyPolygon(self.new_points))
                    self.new_points = []
            with self.canvas:
                Line(points=self.new_points)
                Rectangle(pos=(touch.x - 5, touch.y - 5), size=(10,10))
            print("touched", touch.pos )
            return True
        return super(MyCanvas, self).on_touch_down(touch)


class ButtonsContainer(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonsContainer, self).__init__(**kwargs)
        self.rows = 1
        self.size_hint = (1, None)
        self.height = 50
        self.background_color = [0.7,0.7,0.7,1]
        self.btn1 = Button(on_press=self.btn1_press, text="Save")
        self.btn2 = Button(on_press=self.btn2_add_press,text="Add Polygon")
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
    
    def btn1_press(self, arg):
        print("pressed button 1", arg)
    
    def btn2_add_press(self, arg):
        if not self.parent.mc.adding_poly_mode:
            self.parent.mc.adding_poly_mode = True

class AppScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AppScreen, self).__init__(**kwargs)
        self.rows = 2
        self.buttons = ButtonsContainer()
        self.add_widget(self.buttons)
        self.mc = MyCanvas()
        self.add_widget(self.mc)


class MyApp(App):

    def build(self):
        return AppScreen()


if __name__ == '__main__':
    MyApp().run()