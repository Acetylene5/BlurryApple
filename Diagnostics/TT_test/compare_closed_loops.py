import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)

datadir = '/home/deen/Data/GRAVITY/FISBA/TipTilt/refslope0/'
closed_files = ["T+T_closed.fits", "T-T_closed.fits", "TT+_closed.fits", "TT-_closed.fits"]

images = []
mask = numpy.ones((1024, 1020), dtype=numpy.bool)
for closed in closed_files:
    image = pyfits.getdata(datadir+closed)
    hdr = pyfits.getheader(datadir+closed)
    nonapval = hdr["NONAPVAL"]
    new_mask = numpy.not_equal(image, nonapval)
    mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())), axis=0).reshape(image.shape)
    #complement = numpy.equal(image, nonapval)
    #image[complement] = numpy.median(image[mask])
    images.append(image)

images = numpy.array(images)
average = numpy.zeros(image.shape)
average[mask] = numpy.mean(images[:,mask], axis=0)

minval = numpy.min(images[:,mask]-average[mask])
maxval = numpy.max(images[:,mask]-average[mask])

for i in range(len(images)):
    ax = fig.add_axes([0.1+0.4*(i/2), 0.1+0.4*(i%2), 0.4, 0.4])
    template = numpy.zeros(image.shape)
    template[mask] = images[i,mask]
    im = ax.imshow(template-average, vmin=minval, vmax=maxval)

fig.show()
