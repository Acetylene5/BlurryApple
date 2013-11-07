import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'

synthdf = datadir+'gravity_on_axis_K7-mat.fits'
measdf = datadir+'HO_IM.fits'

synth = pyfits.getdata(synthdf)
meas = pyfits.getdata(measdf)

synIM = synth[0]

fig = pyplot.figure(0)

subaps = []
for i in range(68):
    subaps.append(i)
    subaps.append(i+68)

subaps = numpy.array(subaps)

i = 0
for s, m in zip(synIM[:-2], meas.T):
    fig.clear()
    print i
    i += 1
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    ax.plot(-s[subaps]/numpy.max(s))
    ax.plot(m/numpy.max(m))
    fig.show()
    raw_input()

