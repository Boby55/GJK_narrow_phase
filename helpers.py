#!/bin/env python3
# from math import sqrt
from point import Point

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
        known as "jarvis march"
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

def dotproduct(a,b):
    ''' returns a dot product(scalar) of vectors a,b'''
    return sum(i*j for i,j in zip(a,b))

def index_of_furthest_point(vertices, direction):
    '''get index of furthest point from vertices along direction'''
    return max(range(len(vertices)), key=lambda x:dotproduct(direction,vertices[x]))

def neg_vec(vect):
    return list(map(lambda x:-x,vect))

def support(shape1, shape2, vec_d):
    ''' gets 2 shapes in real space, direction vector. Returns support point in Minkowsky space'''
    ip1 = index_of_furthest_point(shape1,vec_d)
    negvec = list(map(lambda x:-x,vec_d))
    ip2 = index_of_furthest_point(shape2,negvec)
    supp = [i + j for i,j in zip(shape1[ip1], neg_vec(shape2[ip2]))]
    return supp

def supportHC(shape1, direc, w):
    ''' w - initial support vertex
    should use hillClimbing from previous known supp vertex'''
    raise NotImplementedError

def best_simplex(simplex, npoint_cso):
    ''' In: simplex and new point on CSO surface
        Out: New smallest simplex W containing npoint_cso and the closest point to the origin
    '''
    if len(simplex) == 0:
        return [npoint_cso]
    if len(simplex) == 1:
        #point simplex, will be an edge
        w1 = simplex[0]
        w1 = Point(w1[0],w1[1]) # w1 = original simplex
        w = Point(npoint_cso[0], npoint_cso[1]) # new vertex
        d = -w
        e1 = w1 - w
        # print ("best simplex d, e1:", d,e1)
        if d * e1 < 0:
            return [w]
        if d * e1 > 0:
            return [w1,w]
    if len(simplex) == 2:
        #in this case simplex will become triangle.
        #edge simplex, will be a triangle
        w = Point(npoint_cso[0], npoint_cso[1])
        w1 = simplex[0]
        w1, w2 = Point(w1[0],w1[1]), Point(simplex[1][0], simplex[1][1])
        d = -w
        e1, e2 = w1 - w, w2 - w
        # print (d,e1,e2)
        # find normals of e1, e2 which point outside of a triangle
        u1 = Point(-e1.y,e1.x)
        if u1 * e2 > 0:
            u1 = Point(e1.y, -e1.x)
        v1 = Point(-e2.y,e2.x)
        if v1 * e1 > 0:
            v1 = Point(e2.y, -e2.x)
        #now do a bunch of tests, in which region the origin lies
        if ( (d*e1 < 0) and (d*e2 < 0)):
            return [w]
        if ((d*e1 > 0) and (d*u1 > 0)):
            # 0,0 nad hranou w1,w
            return [w1,w]
        if ((d*e2 > 0) and (d*v1 > 0)):
            return [w2,w]
        if ((d*v1 < 0) and (d*u1 < 0)):
            #0,0 lezi vnutri trojuholnika - mame koliziu(v 2d)
            return [w1,w2,w]
        print(d,e1,e2,u1,v1)
    
    print("Old simplex", simplex, "not changed!New point identical?")
    return (simplex)

def closest_point(simplex):
    '''returns closest point on simplex in respect to origin [0,0], 2d case
    works only if origin lies in edge voronoi region''' 
    n = len(simplex)
    if n == 0:
        return 0 # ak nie je simplex, nie je na nom ani bod
    if n == 1:
        return simplex[0] # pripad pre jeden vrchol
    if n == 2: #dva vrcholy,teda usecka
        w1,w2 = simplex[0],  simplex[1]
        d = [w2[0] - w1[0],w2[1] - w1[1]]
        proj = dotproduct(d,w1)/dotproduct(d,d)
        dn = [d[0]*proj,d[1]*proj]
        return [w1[0] - dn[0], w1[1]-dn[1]]
   
    print("three part or more simplex occured")
    return None

def proximity_GJK(A, B, isimplex):
    '''In: convex objects A,B and initial simplex W
        Out: touching vector w 
    '''
    v = [1,1]
    omega = 0 # is actually squared whole time
    tolerance = 0.2
    simplex = isimplex
    while (((v[0]*v[0] + v[1]*v[1]) - omega) > tolerance):
        v = closest_point(simplex)
        print("Closest point on simplex {} to origin:{}".format(simplex,v))
        if v == 0:
            v = [A[0][0] - B[0][0], A[0][1] - B[0][1]]
        v0 = [-v[0],-v[1]] # mam ist smerom k 0,0 ???
        w = support(A, B, v0)
        print("using support point{} along direction {}".format(w,v0))
        simplex = best_simplex(simplex, w)
        print("simplex with that support point:", simplex)
        if len(simplex) == 3:
            print("shapes overlap, collision")
            return v # posleny najblizsi bod na simplexe?
        vw = dotproduct(v,w)
        print("v.w",vw, "dotproduct from",v,w)
        if (vw > 0):
            omega = max(omega, (vw*vw)/(v[0]*v[0] + v[1]*v[1]))
            print("omega: {}".format(omega))
    return v # posledny jablizsi bod na simplexe, je zaroven aj dotykovy vektor

        

def test_proximity():
    A = [[4,11],[9,9],[4,5]]
    B = [[8,6],[15,6],[10,2],[13,1]]
    
    touch_vect = proximity_GJK(A,B, [])
    print(touch_vect)
    print(Point(touch_vect).magnitude())

def test_proximity2():
    # A = [[1,1],[1,4],[3,1],[3,4]] # stvorec 1
    # B = [[6,1],[6,4],[9,1],[9,4]] # stvorec 2

    A = [[1,1],[3,1],[1,3],[3,3]] # stvorec 1
    B = [[5,1],[6,1],[5,3],[6,3]] # stvorec 2
    touch_vect = proximity_GJK(A,B, [])
    print(touch_vect)
    print(Point(touch_vect).magnitude())


if __name__ == "__main__":
    print ("main")
# #test point creation and operation
#     p1, p2, p3 = Point(1,1), Point(2, 2), Point(3,1)
#     assert (p1 * p2 == 4)
# #test convex hull 
#     points = [[0,3], [2,3], [-2,1], [2,1], [3,1], [6,0], [3,3],[0,3]]
#     # print(orientation(p1,p3,p2))
#     print(CH_jarvis(points))

#test support function - find point
    # shape1 = [[4,11], [9,9],[4,5]]
    # shape2 = [[5,7],[7,3],[10,2],[12,7]]
    # direc = [0,1]
    # w = support(shape1, shape2, direc)
    # print(w)
    # print(shape1[index_of_furthest_point(shape1, direc)])

#test closest point on simplex
    # print(-Point(1,2) - Point(10,10))
    # simp = best_simplex([[1,3],[-1,7]],[-4,-1])
    # clsp = closest_point(simp)
    # print(Point(clsp).magnitude())
    simp = best_simplex([[-4,0]],[-1,0])
    print("Best simplex:", simp)
    clsp = closest_point(simp)
    print("Closes point", clsp)
    print(Point(clsp).magnitude())

#test simlex refinement () 
    # w1,w2 = [-1,-1], [1,-1]
    # simplex = [w1, w2]
    # wn = [1,2]
    # print(best_simplex(simplex,wn))
    ###
# test gjk proximity
    print("prox test 1***********")
    test_proximity()
    print("prox test 2**************")
    test_proximity2()
