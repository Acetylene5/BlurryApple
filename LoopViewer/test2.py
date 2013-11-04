import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot

closed = 'test_2/test_data_2/test_data.fits'
datadir = '/home/deen/Data/GRAVITY/LoopClosure/'
CMfile = '/home/deen/Data/GRAVITY/LoopClosure/test_1/HODM_CM0.fits'
CM = scipy.matrix(pyfits.getdata(CMfile))
CM = CM[0:60]
refposfile = '/home/deen/Data/GRAVITY/LoopClosure/test_1/HOCtr.ACT_POS_REF_MAP.fits'

ref = pyfits.getdata(refposfile)


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

# OL are frames in open loop, CL are frames in closed loop
OL = scipy.where( (frame >= open_start[0]) & (frame <= open_stop[0]))[0]
CL = scipy.where( (frame >= close_start[0]) & (frame <= close_stop[0]))[0]

cmd488 = hodm[487]
cmd489 = hodm[488]
cmd490 = hodm[489]
slp488 = grad[487]
slp489 = grad[488]
slp490 = grad[489]

expected = cmd489-0.1*CM.dot(slp490)

unsaturated = numpy.abs(expected) < 1.0

print numpy.max(numpy.abs(expected[unsaturated] - cmd490[unsaturated]))

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

ax.plot(cmd488)
ax.plot(cmd490)
ax.plot(numpy.array(expected.tolist()[0]))

fig.show()
