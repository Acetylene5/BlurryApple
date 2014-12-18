import pyfits
import numpy
import scipy
import VLTTools

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)



df = '/home/deen/Data/GRAVITY/DM/FlatData/FlatPatternData.fits'

data = pyfits.getdata(df)

hodm = data.field(5)
ttm = data.field(6)

new_hodm = numpy.sum(hodm, 0)/len(hodm)
new_ttm = numpy.sum(ttm, 0)/len(ttm)

aortc.set_new_HO_flat_map(new_hodm)
aortc.set_new_TT_flat_map(new_ttm)
