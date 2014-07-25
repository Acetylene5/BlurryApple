import scipy
import pyfits
import matplotlib.pyplot as pyplot
import numpy

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'

synth = pyfits.getdata(datadir+'gravity_on_axis_K7-mat.fits')
meas = pyfits.getdata(datadir+'HODM_HighSNR_IM_9.fits')

synIM = synth[0]

subaps = []
for i in range(68):
    subaps.append(i)
    subaps.append(i+68)
subaps = numpy.array(subaps)

synIM = synIM[:,subaps].T

figure = pyplot.figure(0)
figure.clear()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])

for i in range(40):
    ax.scatter( synIM[:,i], -meas[:,i], s=1, color='r')

for i in range(41,60):
    ax.scatter( synIM[:,i], -meas[:,i], s=1, color='b')

figure.show()
