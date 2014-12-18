import scipy
import numpy
import pyfits
import VLTTools

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)

aortc.make_TT_unscr()

