#!/bin/env python3
from math import sqrt

class Point(object):
    def __init__(self, x, y=None):
        if y==None:
            self.x = x[0]
            self.y= x[1]
        else:
            self.x = x
            self.y = y

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __neg__(self):
        # self.x = -self.x
        # self.y = -self.y
        return Point(-self.x,-self.y)

    def __str__(self):
        return f"[{str(self.x)},{str(self.y)}]"
    
    def __mul__(self, other):
        '''implemented as dot product in this case, returns scalar'''
        return sum([self.x*other.x,self.y*other.y])

    def __repr__(self):
        return f"[{str(self.x)},{str(self.y)}]"

    def __getitem__(self, key):
        if key > 1:
            raise KeyError
        if key == 0:
            return self.x
        if key == 1:
            return self.y

    def __setitem__(self, key, val):
        if key > 1:
            raise KeyError
        if key == 0:
            self.x = val
        if key == 1:
            self.y = val