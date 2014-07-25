import scipy
import pyfits
import inversion
import matplotlib.pyplot as pyplot
import numpy

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'
old = "HO_IM_1021.fits"
rapids = ["HODM_rapid_004.fits","HODM_rapid_005.fits", "HODM_rapid_006.fits", "HODM_rapid_007.fits", "HODM_rapid_008.fits", "HODM_rapid_009.fits", "HODM_rapid_010.fits", "HODM_rapid_011.fits"]
highsnrs = ["HODM_HighSNR_IM_1.fits","HODM_HighSNR_IM_2.fits","HODM_HighSNR_IM_3.fits","HODM_HighSNR_IM_4.fits","HODM_HighSNR_IM_5.fits","HODM_HighSNR_IM_6.fits","HODM_HighSNR_IM_7.fits","HODM_HighSNR_IM_8.fits"]

fig = pyplot.figure(0)
fig.clear()

oldIM = pyfits.getdata(datadir+old)
oldCM, cn, I = inversion.pseudoInverse(datadir+old, numFilteredModes=20)

rapidCMs = []
rapidIMs = []

for f in rapids:
    rapidIMs.append(pyfits.getdata(datadir+f))
    hdr = pyfits.getheader(datadir+f)
    CM, cn, I = inversion.pseudoInverse(datadir+f, numFilteredModes=20)
    rapidCMs.append(CM)

highCMs = []
highIMs = []

for f in highsnrs:
    highIMs.append(pyfits.getdata(datadir+f))
    hdr = pyfits.getheader(datadir+f)
    CM, cn, I = inversion.pseudoInverse(datadir+f, numFilteredModes=20)
    highCMs.append(CM)

avgrapidIM = numpy.mean(rapidIMs, axis=0)
stdrapidIM = numpy.std(rapidIMs, axis=0)
avgrapidCM = numpy.mean(rapidCMs, axis=0)
stdrapidCM = numpy.std(rapidCMs, axis=0)

avghighIM = numpy.mean(highIMs, axis=0)
stdhighIM = numpy.std(highIMs, axis=0)
avghighCM = numpy.mean(highCMs, axis=0)
stdhighCM = numpy.std(highCMs, axis=0)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#a = ax.imshow(avgrapidIM-avghighIM)
#a = ax.imshow(avgrapidIM-oldIM)
a = ax.imshow(avghighIM-oldIM)
#a = ax.imshow(avgrapidCM-avghighCM)
fig.colorbar(a)
fig.show()
fig.savefig("high-old_IM.png")
