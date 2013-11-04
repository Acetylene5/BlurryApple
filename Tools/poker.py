import scipy
import pyfits
import numpy
import sys

df = './Data/flatter.fits'

flat = pyfits.getdata(df)

#actuator = int(sys.argv[1])

for i in range(4):
    flat[0][i] -= 0.01

for actuator in range(60):
    flat[0][actuator] += 0.3
    pyfits.writeto("Output/poked_"+str(actuator)+".fits", flat, clobber=True)
    flat[0][actuator] -= 0.3

pyfits.writeto("Output/flat.fits", flat, clobber=True)
