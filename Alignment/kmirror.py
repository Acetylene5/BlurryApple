import scipy
import numpy
import matplotlib.pyplot as pyplot

class Point( object ):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Line( object):
    def __init__(self, p, slope):
        norm = numpy.sqrt(slope[0]**2.0 + slope[1]**2.0 + slope[2]**2.0)
        self.a = slope[0]/norm
        self.b = slope[1]/norm
        self.c = slope[2]/norm
        self.p = p

    def traverse(self, t):
        newx = self.p.x + self.a*t
        newy = self.p.y + self.b*t
        newz = self.p.z + self.c*t
        newpoint = Point(newx, newy, newz)
        return newpoint

class Plane( object ):
    def __init__(self, p, normal):
        self.p = p
        self.normal = normal

    def intersection(self, line):
        dotproduct = numpy.dot(self.normal, line.slope)
        if dotproduct = 0.0:
            return False
        

origin = Point(0.0, 0.0, 0.0)

l1 = Line(origin, [1.0, 0.0, 0.0])

np = l1.traverse(2.0)
