import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
import NGCTools

detector = NGCTools.detector()

print "Flat"
detector.generateFrame([0.0, 0.0, 0.0, 0.0, 0.0])
print "Tip"
detector.generateFrame([100.0, 0.0, 0.0, 0.0, 0.0])
print "Tilt"
detector.generateFrame([0.0, 100.0, 0.0, 0.0, 0.0])
print "Defocus"
detector.generateFrame([0.0, 0.0, 100.0, 0.0, 0.0])
#detector.generateFrame([0.0, 0.0, 0.0, 1.0, 0.0])
#detector.generateFrame([0.0, 0.0, 0.0, 0.0, 1.0])

fig = pyplot.figure(0)
ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.4, 0.4])
ax3 = fig.add_axes([0.5, 0.1, 0.4, 0.4])
ax4 = fig.add_axes([0.5, 0.5, 0.4, 0.4])

ax1.imshow(detector.z[0])
ax2.imshow(detector.z[1])
ax3.imshow(detector.z[2])
ax4.imshow(detector.z[3])
fig.show()
