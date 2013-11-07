import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
from scipy.linalg import *
import datetime
import os
import re

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'
datafiles = os.listdir(datadir)
#datafiles = ["HODM_IM_RT.fits", "HO_IM_Oct282013.fits", "HO_IM.fits", 'HO_IM_1021.fits', "HODM_IM_RefSlope0.fits", "IM_03Jun.fits", "IM_AIT_HODM_Flat_MSV.fits"]

fig = pyplot.figure(0)
fig.clear()
ax1=fig.add_axes([0.1, 0.15, 0.8, 0.4])
ax2=fig.add_axes([0.1, 0.55, 0.8, 0.4])

dates = []
tips = []
tilts = []

for df in datafiles:
    if ((df.find('TT') == -1) & (df.find("IM") != -1)):
        measdf = datadir+df
        meas = pyfits.getdata(measdf)
        head = pyfits.getheader(measdf)
        dates.append(datetime.datetime.strptime(head["DATE"], "%Y-%m-%dT%H:%M:%S.%f"))
        meas = scipy.matrix(meas)
        U,S,V = svd(meas)

        tips.append(V[1,:])
        tilts.append(V[2,:])

dates = numpy.array(dates)
chronology = dates.argsort()

for i in chronology:
    ax1.plot(tips[i], label = dates[i].strftime("Day %j"))
    ax2.plot(tilts[i])

box = ax1.get_position()
ax1.set_position([box.x0, box.y0+box.height*0.2, box.width, box.height*0.80])
ax1.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, -0.05))
ax1.text(2, 0.25, 'Tip')
ax2.text(2, 0.25, 'Tilt')
fig.show()
fig.savefig("tiptilt_evolution.png")
