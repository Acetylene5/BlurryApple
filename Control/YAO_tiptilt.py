import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
from scipy.linalg import *

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'

synthdf = datadir+'gravity_on_axis_K7-mat.fits'
measdf = datadir+'HODM_IM_RT.fits'

synth = pyfits.getdata(synthdf)
meas = pyfits.getdata(measdf)

synIM = synth[0]

fig = pyplot.figure(0)

subaps = []
for i in range(68):
    subaps.append(i)
    subaps.append(i+68)

subaps = numpy.array(subaps)
newmat = []
for s in synIM[:-2]:
    newmat.append(s[subaps])

newmat = scipy.matrix(newmat)
meas = scipy.matrix(meas)

U,S,V = svd(newmat.T)
fig.clear()
ax1=fig.add_axes([0.1, 0.1, 0.8, 0.4])
ax2=fig.add_axes([0.1, 0.5, 0.8, 0.4])
ax1.plot(V[1,:])
ax1.plot(V[2,:])

U,S,V = svd(meas)
ax2.plot(V[1,:])
ax2.plot(V[2,:])

fig.show()
