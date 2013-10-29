import scipy
import pyfits
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy

fig = pyplot.figure(0)

datadir = '/home/deen/Data/GRAVITY/LoopClosure/'
cmdir = '/home/deen/Code/Python/GRAVITY/WFS_scripts/Inversion/HODM_CM'
CM10 = scipy.matrix(pyfits.getdata(cmdir+'10.fits'))
CM20 = scipy.matrix(pyfits.getdata(cmdir+'19.fits'))
CM50 = scipy.matrix(pyfits.getdata(cmdir+'49.fits'))

opendf = 'openloop/openloop.fits'
closed1 = 'LoopData/LoopData.fits'

openloop = pyfits.getdata(datadir+opendf)
c1 = pyfits.getdata(datadir+closed1)

grad_open = openloop.field(4)
g1 = c1.field(4)

hodm_open = openloop.field(5)
h1 = c1.field(5)

ttm_open = openloop.field(6)
t1 = c1.field(6)

fig.clear()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.8, 0.4])

dmposOL, = ax1.plot([], [], 'o-', lw=2, label='Open')
dmposCL, = ax1.plot([], [], 'o-', lw=2, label='Closed')
ax1.set_ybound(-1.0, 1.0)
ax1.set_xbound(0, len(hodm_open[0])+len(ttm_open[0]))
label1 = ax1.text(0.05, 0.2, 'DM positions', transform=ax1.transAxes)
ax1.legend(ncol=3, frameon=False)

refslopeOL, = ax2.plot([], [], 'o-', lw=2, label='Open Loop')
refslopeCL, = ax2.plot([], [], 'o-', lw=2, label='Closed Loop')
ax2.set_xbound(0, len(grad_open[0]))
ax2.set_ybound(-0.5, 0.5)
txt = ax2.text(0.75, 0.85, '', transform=ax2.transAxes)
label2 = ax2.text(0.05, 0.2, 'Gradients', transform=ax2.transAxes)

#ax2.legend()
xdm = numpy.arange(len(hodm_open[0])+len(ttm_open[0]))
xrs = numpy.arange(len(grad_open[0]))
delta = []

for grad in g1:
    delta.append(CM10.dot(grad))

delta = numpy.array(delta).swapaxes(0,1)[0]
avg_delt = delta.mean(0)
new_dm_pos = numpy.append(h1[0],t1[0]) - avg_delt

outfile = 'HOCtr.ACT_POS_REF_MAP.fits'
hdu = pyfits.PrimaryHDU(new_dm_pos)
hdu.writeto(outfile, clobber=True)

#avg.set_data(xdm, avg_delt)

def init():
    dmposOL.set_data([], [])
    dmposCL.set_data([], [])
    refslopeOL.set_data([], [])
    refslopeCL.set_data([], [])
    return dmposOL, dmposCL, refslopeOL, refslopeCL

def animate(i):
    dmposOL.set_data(xdm, numpy.append(hodm_open[i], ttm_open[0]))
    refslopeOL.set_data(xrs, grad_open[i])

    txt.set_text('Frame : %d' % i)
    dmposCL.set_data(xdm, numpy.append(h1[i], t1[i]))
    refslopeCL.set_data(xrs, g1[i])
    return dmposOL, refslopeOL, dmposCL, refslopeCL, txt

ani = animation.FuncAnimation(fig, animate, numpy.arange(0, len(h1)),
        interval=15, blit=True, init_func=init)

ani.save('CM_3_modes.mp4', dpi=320)

print "done"

fig.show()

