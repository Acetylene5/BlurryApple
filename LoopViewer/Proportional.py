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
closed = 'test_1/test_data_1/test_data_1.fits'
logfile = 'test_1/test_data_1/test_data_1.log'

open_start = [2269]
open_stop = [2734]
close_start = [2735]
close_stop = [3175]

#for line in open(logfile, 'r'):
#    l = line.split()
#    if l[2] = 'STATE_CHANGE_CLOSE_LOOP':

loop = pyfits.getdata(datadir+closed)
frame = loop.field(0)
grad = loop.field(4)
hodm = loop.field(5)
ttm = loop.field(6)

xdm = numpy.arange(len(hodm[0])+len(ttm[0]))
xrs = numpy.arange(len(grad[0]))

OL = scipy.where( (frame > open_start[0]) & (frame < open_stop[0]))[0]
CL = scipy.where( (frame > close_start[0]) & (frame < close_stop[0]))[0]

delta = []

for g in grad:
    delta.append(CM.dot(g))

initial_act_pos = numpy.append(hodm[0], ttm[0])
delta = numpy.array(delta).swapaxes(0,1)[0]
avg_delt = delta.mean(0)
new_dm_pos = initial_act_pos - avg_delt

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

def animate(i):
    dmposCL.set_data(xdm, numpy.append(hodm[CL][i], ttm[0]))
    newdmpos.set_data(xdm, initial_act_pos + CM.dot(grad[CL][i]))

    return dmposCL, newdmpos

ani = animation.FuncAnimation(fig, animate, numpy.arange(0, len(CL)),
        interval=15, blit=True, init_func=init)

ani.save('Proportional_test.mp4', dpi=320)

print "done"

#fig.show()

