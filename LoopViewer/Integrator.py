import scipy
import pyfits
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy

fig = pyplot.figure(0)

datadir = '/home/deen/Data/GRAVITY/LoopClosure/'
CMfile = '/home/deen/Data/GRAVITY/LoopClosure/test_1/HODM_CM0.fits'
CM = scipy.matrix(pyfits.getdata(CMfile))

opendf = 'openloop/openloop.fits'
closed = 'test_2/test_data_2/test_data.fits'
logfile = 'test_2/test_data_2/test_data.log'

# starting and ending frames of the open/closed loops
open_start = [43804]
open_stop = [44229]
close_start = [44230]
close_stop = [44626]

# Extraction of the data from the .fits file
loop = pyfits.getdata(datadir+closed)
frame = loop.field(0)
grad = loop.field(4)
hodm = loop.field(5)
ttm = loop.field(6)

# xdm is the index of the DM Actuators
xdm = numpy.arange(len(hodm[0])+len(ttm[0]))
# xrs is the index of the reference slopes
xrs = numpy.arange(len(grad[0]))

# OL are frames in open loop, CL are frames in closed loop
OL = scipy.where( (frame > open_start[0]) & (frame < open_stop[0]))[0]
CL = scipy.where( (frame > close_start[0]) & (frame < close_stop[0]))[0]

# Determines the initial actuator position by looking at the last frame of
# the open-loop data
initial_act_pos = numpy.append(hodm[OL][-1], ttm[OL][-1])

fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

dmposOL, = ax.plot([], [], 'o-', lw=2, label='Open')
dmposCL, = ax.plot([], [], 'o-', lw=2, label='Commanded')
newdmpos, = ax.plot([], [], 'o-', lw=2, label='Calculated')
ax.set_ybound(-5.0, 7.0)
ax.set_xbound(0, len(hodm[0])+len(ttm[0]))
label1 = ax.text(0.05, 0.2, 'DM positions', transform=ax.transAxes)
ax.legend(ncol=3, frameon=False)

def init():
    dmposOL.set_data(xdm, initial_act_pos)
    dmposCL.set_data([], [])
    newdmpos.set_data([], [])
    return dmposOL, dmposCL

# Sets integrand initially to zero
integrand = numpy.zeros(len(xdm))

def animate(i):
    global integrand
    # Calculates the product of the CM and the gradients
    delta = numpy.array(CM.dot(grad[CL][i]).tolist()[0])
    # Adds to the integrand, multiplying by the gain (-0.1)
    integrand -= delta*0.1
    dmposCL.set_data(xdm, numpy.append(hodm[CL][i], ttm[0]))
    newdmpos.set_data(xdm, initial_act_pos + integrand)

    return dmposCL, newdmpos

ani = animation.FuncAnimation(fig, animate, numpy.arange(0, len(CL)),
        interval=15, blit=True, init_func=init)

ani.save('Integrator_test.mp4', dpi=320)

#print "done"

fig.show()

