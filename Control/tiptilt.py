import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
from scipy.linalg import *
import datetime
import os
import re

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'
#datafiles = os.listdir(datadir)
#datafiles = ["HODM_HighSNR_IM.fits", "HODM_HighSNR_IM_1.fits", "HODM_HighSNR_IM_2.fits", "HODM_HighSNR_IM_3.fits", "HODM_HighSNR_IM_4.fits", "HODM_HighSNR_IM_5.fits", "HODM_HighSNR_IM_6.fits", "HODM_HighSNR_IM_7.fits", "HODM_HighSNR_IM_8.fits"]
datafiles = ["HODM_rapid_016.fits","HODM_rapid_017.fits","HODM_rapid_018.fits","HODM_rapid_019.fits","HODM_rapid_020.fits","HODM_rapid_021.fits","HODM_rapid_022.fits","HODM_rapid_023.fits"]

fig = pyplot.figure(0)
fig.clear()
ax1=fig.add_axes([0.1, 0.15, 0.8, 0.4])
ax2=fig.add_axes([0.1, 0.55, 0.8, 0.4])

dates = []
amplitudes = []
tips = []
tilts = []

for df in datafiles:
    #if ((df.find('TT') == -1) & (df.find("rapid") != -1)):
    if True:#if ((df.find('TT') == -1) & (df.find("IM") != -1) & (df.find("fits") != -1)):
        measdf = datadir+df
        meas = pyfits.getdata(measdf)
        head = pyfits.getheader(measdf)
        dates.append(datetime.datetime.strptime(head["DATE"], "%Y-%m-%dT%H:%M:%S.%f"))
        amplitudes.append(head["AMPLITUDE"])
        meas = scipy.matrix(meas)
        U,S,V = svd(meas)

        tips.append(V[1,:])
        tilts.append(V[2,:])

dates = numpy.array(dates)
chronology = dates.argsort()

for i in chronology:
    #ax1.plot(tips[i], label = dates[i].strftime("Day %j"))
    ax1.plot(tips[i], label = "A = "+str(amplitudes[i]))
    ax2.plot(tilts[i])

box = ax1.get_position()
ax1.set_position([box.x0, box.y0+box.height*0.2, box.width, box.height*0.80])
ax1.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.05))
ax1.text(2, 0.25, 'Tip')
ax2.text(2, 0.25, 'Tilt')
fig.show()
fig.savefig("tiptilt_evolution.png")
