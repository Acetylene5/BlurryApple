import scipy
import numpy
import pyfits
import VLTTools

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)

#=========TTCtr.ACT_POS_REF_MAP.fits====================
#data = pyfits.getdata("../../Maps/Archive/TTCtr.ACT_POS_REF_MAP.fits")
data = [0.26, 0.19]
data =  numpy.array(data, dtype='float32')

#aortc.set_new_TT_flat_map(data)

#========HOCtr.ACT_POS_REF_MAP.fits=====================
#data = pyfits.getdata("../../Maps/Output/flatter.fits")
data = pyfits.getdata("../../Maps/Archive/HOCtr.ACT_POS_REF_MAP.fits")
#data = numpy.random.randn(60)*0.1 - 0.1
#print data

aortc.set_new_HO_flat_map(data)

