import scipy
import numpy
import pyfits

#Comments
comment = 'Created by makeMaps.py'

#Number of Apertures
naps = 68
nacts = 60

#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.04, -0.035]

data =  numpy.array(data, dtype='float32')

outfile = 'TT_flat.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)
#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.14, -0.035]

data =  numpy.array(data, dtype='float32')

outfile = 'T+T.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)
#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.02, -0.035]

data =  numpy.array(data, dtype='float32')

outfile = 'T-T.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)
#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.04, -0.015]

data =  numpy.array(data, dtype='float32')

outfile = 'TT+.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)

#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.04, -0.055]

data =  numpy.array(data, dtype='float32')

outfile = 'TT-.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)

