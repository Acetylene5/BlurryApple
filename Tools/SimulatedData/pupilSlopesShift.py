import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
import NGCTools

detector = NGCTools.detector()

print "No Decenter"
#detector.makeRamp()
pokes = numpy.zeros(60)
pokes[0] = 1.1
detector.generateFrame([0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0], pokes, 0.0)
#"""
print "Actuator 1"
detector.generateFrame([0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0], pokes, 45.0)
print "Actuator 1"
detector.generateFrame([0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 2.0], pokes, 90.0)
print "Actuator 3"
detector.generateFrame([0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0], pokes, 235.0)
#"""
detector.saveFrames("PupilShiftSlopes.fits")
#"""
fig = pyplot.figure(0)
ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
ax2 = fig.add_axes([0.1, 0.5, 0.4, 0.4])
ax3 = fig.add_axes([0.5, 0.1, 0.4, 0.4])
ax4 = fig.add_axes([0.5, 0.5, 0.4, 0.4])

ax1.imshow(detector.z[0])
ax2.imshow(detector.z[1])
ax3.imshow(detector.z[2])
ax4.imshow(detector.z[3])
#fig.savefig("PupilShiftFlux.png")
fig.show()
#"""


#Kolmorogorov turbulence spectrum
