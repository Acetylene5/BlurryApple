import scipy
import numpy
import looptools
import matplotlib.pyplot as pyplot
import pyfits

fig = pyplot.figure(0)

datadir = '/home/deen/Data/GRAVITY/LoopClosure/'

df = datadir+'lcirtc2_5.dat'

values = looptools.readRTCoutput(df)

refpos = pyfits.getdata(datadir+'RefActPosMaps/HOCtr.ACT_POS_REF_MAP.fits')
CM = scipy.matrix(pyfits.getdata(datadir+'CMs/HODM_CM50.fits'))
CM = CM[0:60]

closed = 'closed_10/closed_10.fits'
#closed = 'open/open.fits'

loop = pyfits.getdata(datadir+closed)
frame = loop.field(0)
grad = loop.field(4)
hodm = loop.field(5)
ttm = loop.field(6)

xdm = range(len(hodm[0]))

overlap = numpy.intersect1d(frame, values[0])
closed = scipy.where(overlap > 822)[0]

for i in overlap[closed]:
    print i
    lcntr = scipy.where(frame==i)[0]
    dcntr = scipy.where(values[0] == i)[0]-2
    fig.clear()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    g = grad[lcntr][0]
    delta = numpy.array(CM.dot(g).tolist()[0])
    expected = hodm[lcntr-1][0] - delta*0.1
    recn = ax.plot(xdm, hodm[lcntr][0])
    sent = ax.plot(xdm, values[1][dcntr][1:]/8191.0 - 1.0)
    exp = ax.plot(xdm, expected)
    fig.show()
    raw_input()
    
