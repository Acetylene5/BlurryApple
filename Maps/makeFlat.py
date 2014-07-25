import pyfits
import numpy
import os

a = pyfits.getdata('Input/influence.fits')
b = pyfits.getdata('Input/flat.fits')

#gain = -6.0
#
#c = numpy.copy(b)

c = numpy.copy(b)
#remove central depression
#"""
for i in range(12):
    c[0][i] = 0.0

for i in range(4):
    c[0][i] += 0.02

c[0][18] += 0.02
c[0][19] += 0.02
c[0][20] += 0.02

#c[0][56] -= 0.05
#c[0][54] -= 0.15
#c[0][53] -= 0.15
#c[0][52] -= 0.05
#c[0][51] -= 0.10
#c[0][50] -= 0.10
#c[0][49] -= 0.10
#c[0][46] -= 0.10

c[0][57] += 0.025
c[0][58] += 0.025
c[0][59] += 0.025

c[0][49] -= 0.035
c[0][50] -= 0.035
c[0][51] -= 0.035
c[0][52] -= 0.075
c[0][53] -= 0.075
c[0][54] -= 0.055

c[0][46] -= 0.1

#gain = -3.5
#c[0] += a[3]*gain
#"""

c[0][40] += 0.1
c[0][58] -= 0.1
c[0][48] -= 0.1
c[0][51] -= 0.1

pyfits.writeto('Output/flatter.fits', c, clobber=True)

##print (c - b)
