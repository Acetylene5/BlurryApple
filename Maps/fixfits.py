import scipy
import pyfits
import numpy

df = 'Input/slopes2focus.fits'

data = pyfits.getdata(df)

data = numpy.array(data, dtype=numpy.float32)

hdu = pyfits.PrimaryHDU(data)

hdu.writeto("slopes2focus.fits")

