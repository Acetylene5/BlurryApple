import numpy
import pyfits
import scipy
import matplotlib.pyplot as pyplot

#df = '/home/deen/Data/GRAVITY/NAOMI/NAOMI_simulated_buffer_5_frames_rand.fits'

#naomi, hdr =pyfits.getdata(df, header=True)

fig = pyplot.figure()
fig.clear()
ax1 = fig.add_subplot(1,1,1)
#f1 = ax1.plot(naomi[0])
#f2 = ax1.plot(naomi[1])
#f3 = ax1.plot(naomi[2])
#f4 = ax1.plot(naomi[3])
#f5 = ax1.plot(naomi[4])

#fig.show()

def twoDgaussian(x, y, center, stdev, A):
    retval = A * (numpy.exp(-(x-center[0])**2/stdev[0]) * 
                  numpy.exp(-(y-center[1])**2/stdev[1]))
    return retval

nx = 96
ny = 72

npix = nx*ny

apertureMap = [[False, False, True, True, True, True, True, False, False],
               [False, True, True, True, True, True, True, True, False],
               [True, True, True, True, True, True, True, True, True],
               [True, True, True, True, True, True, True, True, True],
               [True, True, True, True, False, True, True, True, True],
               [True, True, True, True, True, True, True, True, True],
               [True, True, True, True, True, True, True, True, True],
               [False, True, True, True, True, True, True, True, False],
               [False, False, True, True, True, True, True, False, False]]

apertureSize = 8.0

#xpos = numpy.linspace(0.0, nx, num=len(apertureMap[0]), 
#        endpoint=False)+nx/(len(apertureMap[0])*2.)
#ypos = numpy.linspace(0.0, ny, num=len(apertureMap),
#        endpoint=False)+ny/(len(apertureMap)*2.)
xpos = numpy.arange(len(apertureMap[0]))*apertureSize+4.0
ypos = numpy.arange(len(apertureMap))*apertureSize+4.0
centroids = []
for apvec, y in zip(apertureMap, ypos):
    for ap, x in zip(apvec, xpos):
        if ap:
            centroids.append((numpy.random.rand(2)-0.5)*apertureSize/4.0+(x, y))
            #centroids.append((x, y))

xpix = numpy.arange(nx)
ypix = numpy.arange(ny)

xx, yy = numpy.meshgrid(xpix, ypix)
z = numpy.zeros((ny, nx))

stdev = (3.0, 3.0)
amplitude = 1.0

for centroid in centroids:
    z += twoDgaussian(xx, yy, centroid, stdev, amplitude)


ax1.imshow(z)
fig.show()
