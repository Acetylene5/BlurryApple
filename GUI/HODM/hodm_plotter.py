import scipy
import numpy
import matplotlib.pyplot as pyplot
import pyfits

def ring1(x, y):
    global nx
    radius = nx/10.0
    return (x**2.0 + y**2.0)**(0.5) < radius

def ring2(x, y):
    global nx
    radius = nx/5.0
    return (x**2.0 + y**2.0)**(0.5) < radius

def ring3(x, y):
    global nx
    radius = 3*nx/10.0
    return (x**2.0 + y**2.0)**(0.5) < radius

def ring4(x, y):
    global nx
    radius = 4*nx/10.0
    return (x**2.0 + y**2.0)**(0.5) < radius

def ring5(x, y):
    global nx
    radius = nx/2.0
    return (x**2.0 + y**2.0)**(0.5) < radius

def measure_angle(x, y):
    return numpy.rad2deg(numpy.arctan2(y, x))

class actuator( object ):
    def __init__(self, number, ring, angle_start, angle_stop, value = 0.0):
        self.number = number
        self.ring = ring
        self.angle_start = angle_start
        self.angle_stop= angle_stop
        self.value = value
        self.pixels = []

    def included(self, x, y, angle):

        if (self.angle_start <= angle) and (self.angle_stop >= angle):
            pass
        else:
            return False
        if self.ring == 1:
            if ring1(x, y):
                pass
            else:
                return False
        elif self.ring == 2:
            if (ring2(x, y) and not(ring1(x,y))):
                pass
            else:
                return False
        elif self.ring == 3:
            if (ring3(x, y) and not(ring2(x,y))):
                pass
            else:
                return False
        elif self.ring == 4:
            if (ring4(x, y) and not(ring3(x, y))):
                pass
            else:
                return False
        else:
            if (ring5(x, y) and not(ring4(x, y))):
                pass
            else:
                return False

        return True

    def addPixel(self, x, y):
        self.pixels.append([x, y])

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def calcCentroid(self):
        self.pixels = numpy.array(self.pixels)
        self.xTextAnchor = numpy.average(self.pixels[:,0])
        self.yTextAnchor = numpy.average(self.pixels[:,1])



fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

nact = 60
nx = 200
ny = 200

actuators = []

#xpts = numpy.arange(nx)
#ypts = numpy.arange(ny)
grid = numpy.zeros((nx, ny), dtype ='int16')
#grid = numpy.meshgrid(nx, ny)

#Populate actuators

act_num = 0

n_ring1 = 4
n_ring2 = 8
n_ring3 = 12
n_ring4 = 16
n_ring5 = 20

#Create ring 1
ringn = 1
for nact in [n_ring1, n_ring2, n_ring3, n_ring4, n_ring5]:
    for i in range(nact):
        angle_start = 360.0/nact * i
        angle_stop = 360.0/nact * (i+1)
        if angle_start >= 180.0:
            angle_start -= 360.0
        if angle_stop > 180.0:
            angle_stop -= 360.0

        value = 2.0*numpy.random.random_sample() - 1.0
        value = act_num
        actuators.append(actuator(act_num, ringn, angle_start,
            angle_stop, value))
        act_num += 1
    ringn += 1

for x in range(nx):
    xpix = x-nx/2.0
    for y in range(ny):
        ypix = y - ny/2.0
        angle = measure_angle(xpix, ypix)
        for act in actuators:
            if act.included(xpix, ypix, angle):
                grid[x][y] = act.getValue()
                act.addPixel(x, y)


hdu = pyfits.PrimaryHDU(grid.T)
hdu.writeto("HODM_SUBAP_MAP.fits", clobber=True)
#for act, value in zip(actuators, flatpattern):

ax.matshow(grid.T, origin='lower')
for act in actuators:
    act.calcCentroid()
    ax.text(act.xTextAnchor, act.yTextAnchor, str(act.number))

#a = actuators[2]
#a.setValue(50.0)
#pixels = numpy.array(a.pixels)
#grid[pixels[:,0],pixels[:,1]] = a.getValue()
#ax.imshow(grid, origin='lower')

fig.show()

