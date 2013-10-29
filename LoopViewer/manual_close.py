import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.8, 0.4])

n = 5

datadir = '/home/deen/Data/GRAVITY/LoopClosure/'
cmdir = '/home/deen/Code/Python/GRAVITY/WFS_scripts/Inversion/HODM_CM'
CM10 = scipy.matrix(pyfits.getdata(cmdir+'10.fits'))

opendf = 'openloop/openloop.fits'
openloop = pyfits.getdata(datadir+opendf)
grad_open = openloop.field(4)
hodm_open = openloop.field(5)
ttm_open = openloop.field(6)

xact = numpy.arange(len(hodm_open[0])+len(ttm_open[0]))
xgrad = numpy.arange(len(grad_open[0]))

ol_grad = ax1.plot(xgrad, grad_open.mean(0), label='Flat')
ol_act = ax2.plot(xact, numpy.append(hodm_open[0], ttm_open[0]))

for i in numpy.arange(n)+1:
    #if n == 0:
    #    closeddf = 'manual_close/manual_close.fits'
    #else:
    #    closeddf = 'manual_close_'+str(i)+'/manual_close_'+str(i)+'.fits'
    closeddf = 'manual_close_'+str(i)+'/manual_close_'+str(i)+'.fits'

    closedloop = pyfits.getdata(datadir+closeddf)
    grad_closed = closedloop.field(4)
    hodm_closed = closedloop.field(5)
    ttm_closed = closedloop.field(6)

    delta = []

    for grad in grad_closed:
        delta.append(CM10.dot(grad))

    delta = numpy.array(delta).swapaxes(0,1)[0]
    avg_delt = delta.mean(0)
    new_dm_pos = numpy.append(hodm_closed[0], ttm_closed[0]) - avg_delt
    
    ax1.plot(xgrad, grad_closed.mean(0), label='N='+str(i))
    ax2.plot(xact, numpy.append(hodm_closed[0], ttm_closed[0]))


    outfile = 'HOCtr.ACT_POS_REF_MAP_'+str(i+1)+'.fits'
    hdu = pyfits.PrimaryHDU(new_dm_pos[0:60])
    hdu.writeto(outfile, clobber=True)

ax1.legend(ncol=5)
fig.show()
fig.savefig("manual_closure.png")
print "done"

