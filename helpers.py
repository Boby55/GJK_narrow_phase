#!/bin/env python3

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"[{str(self.x)},{str(self.y)}]"
    
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


def leftmost(pointset):
    ''' returnsindex of  the leftmost point of a set , in 2d its x value is minimal'''
    l = min(pointset, key = lambda a : a[0])
    return pointset.index(l)

def orientation(p, q, r):
    '''for finding an orientation of ordered point triplet (p,q,r)
    returns:
    0 --> colinear
    1 --> clockwise
    2 --> counter-clockwise
    '''
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    if val > 0:
        return 1
    return 2

def CH_jarvis(set_of_points):
    '''this function gets a set of at least 3 points and returns their convex hull
        knows as "jarvis march
    '''
    if len(set_of_points) < 3:
        return set_of_points
    leftm = leftmost(set_of_points)
    hull = []
    p = leftm
    while(1):
        hull.append(set_of_points[p])
        q = (p+1) % len(set_of_points)
        for i in range(len(set_of_points)):
            if (orientation(set_of_points[p], set_of_points[i], set_of_points[q]) == 2):
                q = i
        p = q
        if p == leftm:
            break
    if hull[0] != hull[len(hull)-1]:
        hull.append(hull[0])
    return hull


if __name__ == "__main__":
    print ("main")
    p1 = Point(1,1)
    p2 = Point(2, 2)
    p3 = Point(3,1)
    points = [[0,3], [2,3], [1,1], [2,1], [3,0], [0,0], [3,3],[0,3]]
    left = leftmost([p2,p1])
    print(orientation(p1,p3,p2))
    print(CH_jarvis(points))