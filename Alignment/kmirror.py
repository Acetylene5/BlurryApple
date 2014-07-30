import scipy
import numpy
import matplotlib.pyplot as pyplot

class Derotator( object ):
    def __init__(self):
        self.Z = 15.0   # mm
        self.Y = 30.0   # mm
        self.origin = Point(0.0, 0.0, 0.0)
        self.theta = numpy.arctan2(self.Z, self.Y)
        self.beta = numpy.pi/4.0 + self.theta/2.0
        self.mirror1 = Plane(Point(0.0, 0.0, self.Z), numpy.array([0.0,
            numpy.sin(self.beta), numpy.cos(self.beta)]))
        self.mirror2 = Plane(Point(0.0, self.Y, 0.0), numpy.array([0.0, -1.0,
            0.0]))
        self.mirror3 = Plane(Point(0.0, 0.0, -self.Z), numpy.array([0.0,
            numpy.sin(self.beta), -numpy.cos(self.beta)]))

    def rotate(self, angle):
        self.mirror1.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))
        self.mirror2.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))
        self.mirror3.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))

    def propogate(self, line):
        r1 = self.mirror1.reflection(line)
        r2 = self.mirror2.reflection(r1)
        r3 = self.mirror3.reflection(r2)
        return r3

class Point( object ):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Line( object):
    def __init__(self, p, slope):
        norm = numpy.sqrt(slope[0]**2.0 + slope[1]**2.0 + slope[2]**2.0)
        self.slope = slope/norm
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
        self.normal = normal/numpy.sqrt(numpy.sum(numpy.square(normal)))
        self.calculatePlaneEqn()

    def rotate(self, p, angle, axis):
        vector = numpy.array([p.x-self.p.x, p.y-self.p.y, p.z-self.p.z])
        ux = axis[0]
        uy = axis[1]
        uz = axis[2]
        rotation_matrix = numpy.array([
            [numpy.cos(angle) + ux**2*(1.0-numpy.cos(angle)), 
                ux*uy*(1.0-numpy.cos(angle)) - uz*numpy.sin(angle),
                ux*uz*(1.0-numpy.cos(angle)) + uy*numpy.sin(angle)],
            [ux*uy*(1.0-numpy.cos(angle))+uz*numpy.sin(angle),
                numpy.cos(angle)+uy**2*(1.0-numpy.cos(angle)),
                uy*uz*(1.0-numpy.cos(angle))-ux*numpy.sin(angle)],
            [uz*ux*(1.0-numpy.cos(angle))-uy*numpy.sin(angle),
                uz*uy*(1.0-numpy.cos(angle))+ux*numpy.sin(angle),
                numpy.cos(angle)+uz**2*(1.0-numpy.cos(angle))]])
        new_vector = numpy.dot(rotation_matrix, vector)
        self.p = Point(p.x-new_vector[0], p.y-new_vector[1], p.z-new_vector[2])
        self.normal = numpy.dot(rotation_matrix, self.normal)
        self.calculatePlaneEqn()

    def calculatePlaneEqn(self):
        Ax = self.normal[0]
        Ay = self.normal[1]
        Az = self.normal[2]
        if (Ax == Ay == 0.0):
            self.coeffs = numpy.array([0.0, 0.0, 1.0/self.p.z])
        elif (Ax == Az == 0.0):
            self.coeffs = numpy.array([0.0, 1.0/self.p.y, 0.0])
        elif (Ay == Az == 0.0):
            self.coeffs = numpy.array([1.0/self.p.x, 0.0, 0.0])
        elif (Ax == 0):
            p2 = Point(self.p.x, self.p.y+1.0, self.p.z-Ay/Az)
            X = numpy.array([
                [self.p.y, self.p.z],
                [p2.y, p2.z]])
            Y = numpy.array([1.0, 1.0])
            BC = numpy.linalg.solve(X, Y)
            self.coeffs = numpy.array([0.0, BC[0], BC[1]])
        elif (Ay == 0):
            p2 = Point(self.p.x+1.0, self.p.y, self.p.z-Ax/Az)
            X = numpy.array([
                [self.p.x, self.p.z],
                [p2.x, p2.z]])
            Y = numpy.array([1.0, 1.0])
            AC = numpy.linalg.solve(X, Y)
            self.coeffs = numpy.array([AC[0], 0.0, AC[1]])
        elif (Az == 0):
            p2 = Point(self.p.x-Ay/Ax, self.p.y-1.0, self.p.z)
            X = numpy.array([
                [self.p.x, self.p.y],
                [p2.x, p2.y]])
            Y = numpy.array([1.0, 1.0])
            AB = numpy.linalg.solve(X,Y)
            self.coeffs = numpy.array([AB[0], AB[1], 0.0])
        else:
            p2 = Point(self.p.x, self.p.y+1.0, self.p.z-Ay/Az)
            p3 = Point(self.p.x+1.0, self.p.y, self.p.z-Ax/Az)
            p4 = Point(self.p.x-Ay/Ax, self.p.y+1.0, self.p.z)
            X = numpy.array([
                [p2.x, p2.y, p2.z],
                [p3.x, p3.y, p3.z],
                [p4.x, p4.y, p4.z]])
            Y = numpy.array([1.0, 1.0, 1.0])
            self.coeffs = numpy.linalg.solve(X, Y)

    def intersection(self, line):
        dotproduct = numpy.dot(self.normal, line.slope)
        if dotproduct == 0.0:
            return False
        else:
            D = (self.coeffs[0]*line.p.x + self.coeffs[1]*line.p.y +
                    self.coeffs[2]*line.p.z)
            t = (1.0-D)/(self.coeffs[0]*line.a + self.coeffs[1]*line.b +
                    self.coeffs[2]*line.c)
            return line.traverse(t)

    def reflection(self, line):
        reflection = self.intersection(line)
        if reflection:
            dot = numpy.dot(self.normal, line.slope)
            newx = line.a - 2*dot*self.normal[0]
            newy = line.b - 2*dot*self.normal[1]
            newz = line.c - 2*dot*self.normal[2]
            newLine = Line(reflection, [newx, newy, newz])
            return newLine
        else:
            print "Error! Line does not intersect plane!"
            return False

        

origin = Point(0.0, 0.0, 0.0)
p1 = Point(0.01, 0.0, 0.0)
p2 = Point(0.00, 0.01, 0.0)

derot = Derotator()

l0 = Line(origin, [0.0, 0.0, -1.0])
l1 = Line(p1, [0.0, 0.0, -1.0])
l2 = Line(p2, [0.0, 0.0, -1.0])

l3 = Line(origin, [0.0, 0.00028, -1.0])
l4 = Line(origin, [0.00028, 0.0, -1.0])

detectorPlane = Plane(Point(0.0, 0.0, -1000.0), numpy.array([0.0, 0.0, 1.0]))

nsteps = 100.0
dangle = 2.0*numpy.pi/nsteps

angle = []
a = []
b = []
c = []
d = []
e = []

theta = 0.0
for i in range(nsteps):
    angle.append(theta)
    a.append(detectorPlane.intersection(derot.propogate(l0))
    b.append(detectorPlane.intersection(derot.propogate(l1))
    c.append(detectorPlane.intersection(derot.propogate(l2))
    d.append(detectorPlane.intersection(derot.propogate(l3))
    e.append(detectorPlane.intersection(derot.propogate(l4))

    derot.rotate(dangle)
    theta += dangle


a_end = detectorPlane.intersection(a)
b_end = detectorPlane.intersection(b)
c_end = detectorPlane.intersection(c)

print a_end.x, a_end.y
print b_end.x, b_end.y
print c_end.x, c_end.y

derot.rotate(0.01)

d = derot.propogate(l0)
e = derot.propogate(l1)
f = derot.propogate(l2)

d_end = detectorPlane.intersection(d)
e_end = detectorPlane.intersection(e)
f_end = detectorPlane.intersection(f)

print d_end.x, d_end.y
print e_end.x, e_end.y
print f_end.x, f_end.y
