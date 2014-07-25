import scipy
import pyfits

import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()

datadir = '/home/deen/Data/GRAVITY/LoopClosure/refslopes/'

openloop = pyfits.getdata(datadir+'refslopes.fits')
grad = openloop.field(4)

refslopes = grad.mean(0) + 1.5

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(refslopes)

pyfits.writeto('Output/Refslopes.fits', refslopes, clobber=True)
pyfits.writeto('Output/Refslopes_zero.fits', refslopes*0.0+1.5, clobber=True)
fig.show()
