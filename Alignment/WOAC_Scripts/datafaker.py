import scipy
import pyfits
import matplotlib.pyplot as pyplot
import numpy

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#VISIBLE DATA
nx = 1024
ny = 1388

bkglvl = 40.0
bkgstd = 5.0

xcent = 550
ycent = 600
beam_radius = 20.0
beam_strength = 100

outfile = './fakeData/VIS_fakedata.fits'

data = numpy.zeros([nx, ny], dtype=numpy.int16)

background = bkgstd*numpy.random.randn(nx, ny)+bkglvl

data += background

for x in range(nx):
    for y in range(ny):
        if ( (x-xcent)**2.0 + (y-ycent)**2.0) < beam_radius**2.0:
            data[x][y] += beam_strength

ax.imshow(data)

fig.show()

hdu = pyfits.PrimaryHDU(data)
hdu.writeto(outfile, clobber=True)


#IR Data
nx 
