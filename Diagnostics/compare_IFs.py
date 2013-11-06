import scipy
import matplotlib.pyplot as pyplot
import numpy
import pyfits

oldf = '/home/deen/Data/GRAVITY/InfluenceFunctions/IF_cube_2012.fits'
newf = '/home/deen/Data/GRAVITY/InfluenceFunctions/IF_cube_041113.fits'
newf = '/home/deen/Data/GRAVITY/InfluenceFunctions/IF_cube.fits'

old = pyfits.getdata(oldf)
new = pyfits.getdata(newf)

fig = pyplot.figure(0)

i = 0
for actuator in zip(old, new):
    fig.clear()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    old_nans = numpy.isnan(actuator[0])
    new_nans = numpy.isnan(actuator[1])

    actuator[0][old_nans] = 0.0
    actuator[1][new_nans] = 0.0

    print i
    i += 1
    diff = ax.imshow(actuator[1])
    fig.colorbar(diff)
    fig.show()
    raw_input()

    
