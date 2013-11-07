import scipy
import matplotlib.pyplot as pyplot
import numpy
import pyfits

datadir = '/home/deen/Data/GRAVITY/InfluenceFunctions/'
newf = datadir+'IF_cube.fits'
newest = pyfits.getdata(newf)

fig = pyplot.figure(0)

def loadMACAO(index):
    datafile = open(datadir+'IF_DM4_act%02d.dat'%index, 'r')
    retval = []
    for line in datafile:
        retval.append(numpy.array(line.split(), dtype = numpy.float32))

    return retval

i = 0
for new in zip(newest):
    old = loadMACAO(i)
    fig.clear()
    ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
    ax2 = fig.add_axes([0.5, 0.5, 0.4, 0.4])
    #old_nans = numpy.isnan(old)
    #new_nans = numpy.isnan(new)

    #old[old_nans] = 0.0
    #new[new_nans] = 0.0

    print i
    i += 1
    o = ax1.imshow(old)
    n = ax2.imshow(new[0])
    #diff = ax.imshow(actuator[1])
    fig.colorbar(o)
    fig.show()
    raw_input()

    
