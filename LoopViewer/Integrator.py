import scipy
import pyfits
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy

fig = pyplot.figure(0)

refposfile = '/home/deen/Data/GRAVITY/LoopClosure/test_1/HOCtr.ACT_POS_REF_MAP.fits'
ref = pyfits.getdata(refposfile)

datadir = '/home/deen/Data/GRAVITY/LoopClosure/'
CMfile = '/home/deen/Data/GRAVITY/LoopClosure/test_1/HODM_CM0.fits'
CM = scipy.matrix(pyfits.getdata(CMfile))
CM = CM[0:60]

opendf = 'openloop/openloop.fits'
closed = 'test_2/test_data_2/test_data.fits'
logfile = 'test_2/test_data_2/test_data.log'

# starting and ending frames of the open/closed loops
open_start = [43804]
open_stop = [44229]
close_start = [43306]
close_stop = [43803]

# Extraction of the data from the .fits file
loop = pyfits.getdata(datadir+closed)
frame = loop.field(0)
grad = loop.field(4)
hodm = loop.field(5)
ttm = loop.field(6)

# xdm is the index of the DM Actuators
#xdm = numpy.arange(len(hodm[0])+len(ttm[0]))
xdm = numpy.arange(len(hodm[0]))
# xrs is the index of the reference slopes
xrs = numpy.arange(len(grad[0]))

# OL are frames in open loop, CL are frames in closed loop
OL = scipy.where( (frame >= open_start[0]) & (frame <= open_stop[0]))[0]
CL = scipy.where( (frame >= close_start[0]) & (frame <= close_stop[0]))[0]

fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

diff, = ax.plot([], [], 'o-', lw=2,label='Difference')
ax.set_ybound(-1.0, 1.0)
ax.set_xbound(0, len(hodm[0])+len(ttm[0]))
label1 = ax.text(0.05, 0.2, 'DM positions', transform=ax.transAxes)
ax.legend(frameon=False)


#delta = numpy.array(CM.dot(grad[CL][0]).tolist()[0])
#expected = hodm[CL[0]-1] - delta*0.1
#difference = hodm[CL][0] - expected

def init():
    diff.set_data([], [])
    return diff,

def animate(i):
    # Calculates the product of the CM and the gradients
    delta = numpy.array(CM.dot(grad[CL][i]).tolist()[0])
    expected = hodm[CL[i]-1] - delta*0.1
    unsaturated = numpy.array((numpy.abs(expected) < 1.0).tolist()[0])
    difference = hodm[CL][i] - expected
    diff.set_data(xdm, difference)
    print numpy.max(numpy.abs(numpy.array(difference.tolist()[0])[unsaturated]))
    return diff,

ani = animation.FuncAnimation(fig, animate, numpy.arange(0, len(CL)),
        interval=105, blit=True, init_func=init)

#ani.save('Integrator_test.mp4', dpi=320)

#print "done"

fig.show()

