import scipy
import pyfits

import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()

datadir = '/home/deen/Data/GRAVITY/LoopClosure/openloop/'

openloop = pyfits.getdata(datadir+'openloop.fits')
grad = openloop.field(4)

refslopes = grad.mean(0) + 3.5

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(refslopes)

pyfits.writeto('Refslopes.fits', refslopes, clobber=True)
pyfits.writeto('Refslopes_zero.fits', refslopes*0.0+3.5, clobber=True)
fig.show()
