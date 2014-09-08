import scipy
import numpy
import matplotlib.pyplot as pyplot

class Derotator( object ):
    def __init__(self):
        self.Z = 10.0   # mm
        self.Y = 17.3   # mm
        self.origin = Point(0.0, 0.0, 0.0)
        self.theta = numpy.arctan2(self.Z, self.Y)
        self.beta = numpy.pi/4.0 + self.theta/2.0
        #print numpy.rad2deg(self.beta)

        self.m1Point = Point(0.0, 0.0, self.Z)
        self.m2Point = Point(0.0, self.Y, 0.0)
        self.m3Point = Point(0.0, 0.0, -self.Z)

        self.m1Normal = numpy.array([0.0, numpy.sin(self.beta), numpy.cos(self.beta)])
        self.m2Normal = numpy.array([0.0, -1.0, 0.0])
        self.m3Normal = numpy.array([0.0, numpy.sin(self.beta), -numpy.cos(self.beta)])

        self.makeMirrors()

    def makeMirrors(self):
        self.mirror1 = Plane(self.m1Point, self.m1Normal)
        self.mirror2 = Plane(self.m2Point, self.m2Normal)
        self.mirror3 = Plane(self.m3Point, self.m3Normal)

    def rotate(self, angle):
        self.mirror1.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))
        self.mirror2.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))
        self.mirror3.rotate(self.origin, angle, numpy.array([0.0, 0.0, 1.0]))

    def propogate(self, line):
        r1 = self.mirror1.reflection(line)
        r2 = self.mirror2.reflection(r1)
        r3 = self.mirror3.reflection(r2)
        return r3

    def translate(self, dx, dy, dz):
        shift = Point(dx, dy, dz)
        self.origin = self.origin+shift
        self.m1Point = self.m1Point+shift
        self.m2Point = self.m2Point+shift
        self.m3Point = self.m3Point+shift
        self.makeMirrors()

    def tiptilt(self, angle, axis):
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
        v1 = self.origin- self.m1Point
        v1 = numpy.array([v1.x, v1.y, v1.z])
        new_vector = numpy.dot(rotation_matrix, v1)
        self.m1Normal = numpy.dot(rotation_matrix, self.m1Normal)
        v1 = Point(new_vector[0], new_vector[1], new_vector[2])
        self.m1Point = self.origin + v1
        v2 = self.origin- self.m2Point
        v2 = numpy.array([v2.x, v2.y, v2.z])
        new_vector = numpy.dot(rotation_matrix, v2)
        self.m2Normal = numpy.dot(rotation_matrix, self.m2Normal)
        v2 = Point(new_vector[0], new_vector[1], new_vector[2])
        self.m2Point = self.origin + v2
        v3 = self.origin- self.m3Point
        v3 = numpy.array([v3.x, v3.y, v3.z])
        new_vector = numpy.dot(rotation_matrix, v3)
        self.m3Normal = numpy.dot(rotation_matrix, self.m3Normal)
        v3 = Point(new_vector[0], new_vector[1], new_vector[2])
        self.m3Point = self.origin + v3

        self.makeMirrors()


class Point( object ):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y, self.z-other.z)

    def __repr__(self):
        return "x: "+str(self.x)+" y: "+str(self.y)+" z: "+str(self.z)
    def __str__(self):
        return "x: "+str(self.x)+" y: "+str(self.y)+" z: "+str(self.z)

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
        if (numpy.abs(Ax) < 1e-5) & (numpy.abs(Ay) < 1e-5):
            self.coeffs = numpy.array([0.0, 0.0, 1.0/self.p.z])
        elif (numpy.abs(Ax) < 1e-5) & (numpy.abs(Az) < 1e-5 ):
            self.coeffs = numpy.array([0.0, 1.0/self.p.y, 0.0])
        elif (numpy.abs(Ay) < 1e-5) & (numpy.abs(Az) < 1e-5):
            self.coeffs = numpy.array([1.0/self.p.x, 0.0, 0.0])
        elif (numpy.abs(Ax) < 1e-5):
            p2 = Point(self.p.x, self.p.y+1.0, self.p.z-Ay/Az)
            X = numpy.array([
                [self.p.y, self.p.z],
                [p2.y, p2.z]])
            Y = numpy.array([1.0, 1.0])
            BC = numpy.linalg.solve(X, Y)
            self.coeffs = numpy.array([0.0, BC[0], BC[1]])
        elif (numpy.abs(Ay) < 1e-5):
            p2 = Point(self.p.x+1.0, self.p.y, self.p.z-Ax/Az)
            X = numpy.array([
                [self.p.x, self.p.z],
                [p2.x, p2.z]])
            Y = numpy.array([1.0, 1.0])
            AC = numpy.linalg.solve(X, Y)
            self.coeffs = numpy.array([AC[0], 0.0, AC[1]])
        elif (numpy.abs(Az) < 1e-5):
            p2 = Point(self.p.x-Ay/Ax, self.p.y+1.0, self.p.z)
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
p1 = Point(-0.002, 0.0, 0.0)
p2 = Point(0.00, 0.5, 0.0)
p3 = Point(1.0, 1.0, 0.0)

derot = Derotator()

l0 = Line(origin, [0.0, 0.0, -1.0])
l1 = Line(p1, [0.0, 0.0, -1.0])
l2 = Line(p3, [0.0, 0.0, -1.0])

l3 = Line(p3, [0.0, 0.00028, -1.0])
l4 = Line(origin, [0.00028, 0.0, -1.0])

detectorPlane = Plane(Point(0.0, 0.0, -1000.0), numpy.array([0.0, 0.0, 1.0]))

nsteps = 51
dangle = 2.0*numpy.pi/nsteps

angle = []
a = []
b = []
c = []
d = []
e = []

theta = 0.0

derot.tiptilt(0.000278, numpy.array([0.0, 1.0, 0.0]))

#derot.rotate(numpy.deg2rad(45.0))
#spot = detectorPlane.intersection(derot.propogate(l2))
#print asdf

for i in range(nsteps):
    angle.append(theta)
    spot = detectorPlane.intersection(derot.propogate(l0))
    a.append([spot.x, spot.y])
    spot = detectorPlane.intersection(derot.propogate(l1))
    b.append([spot.x, spot.y])
    spot = detectorPlane.intersection(derot.propogate(l2))
    c.append([spot.x, spot.y])
    spot = detectorPlane.intersection(derot.propogate(l3))
    d.append([spot.x, spot.y])
    spot = detectorPlane.intersection(derot.propogate(l4))
    e.append([spot.x, spot.y])

    derot.rotate(dangle)
    theta += dangle

    

a = numpy.array(a)
b = numpy.array(b)
c = numpy.array(c)
d = numpy.array(d)
e = numpy.array(e)

pyplot.ion()
fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
fig.show()

#for image in zip(angle, a, b, c):
#    print("Angle : %.2f" % numpy.rad2deg(image[0]))
#    line = numpy.array(image[1:])
#    ax.plot(line[:,0], line[:,1], marker= 'x')
#    pyplot.draw()
#    raw_input()
    
ax.plot(a[:,0], a[:,1], c='r', marker='o')
ax.plot(b[:,0], b[:,1], c='b', marker='x')
#ax.plot(c[:,0], c[:,1], c='g', marker='+')
#ax.plot(d[:,0], d[:,1], c='k', marker='.')
#ax.plot(e[:,0], e[:,1], c='m', marker='x')

