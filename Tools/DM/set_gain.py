import scipy
import numpy
import pyfits
import VLTTools

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)

gain = 0.2

aortc.set_gain(gain)

