import scipy
import numpy
import pyfits

data = numpy.zeros((2000,2), dtype=numpy.float32)

k = 100.0

for i in range(2000):
    data[i][0] = 0.5*numpy.sin(i/k)
    data[i][1] = 0.5*numpy.cos(i/k)

outfile = 'TTDisturb.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.writeto(outfile, clobber=True)


data = numpy.ones((2000,2), dtype=numpy.float32)*0.234

print data[0]
hdu = pyfits.PrimaryHDU(data)
hdu.writeto("TT_Constant.fits", clobber=True)
