import pyfits
import scipy
import numpy
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

flat = pyfits.getdata('./Data/flatter.fits')

frames = []
actuator = 0
amplitude = 0.05
vals = []

for i in range(2000):
    newframe = numpy.zeros(flat[0].shape)
    newval = amplitude*numpy.random.randn()
    newval = numpy.max([-0.9, numpy.min([0.9, newval])])
    vals.append(newval)
    newframe[actuator] = newval
    frames.append(newframe)

frames = numpy.array(frames)

ax.plot(vals)
fig.show()

frames_hdu = pyfits.PrimaryHDU( frames.astype(numpy.float32))
frames_hdu.writeto("./Output/Disturbance_0_0.1.fits", clobber=True)
