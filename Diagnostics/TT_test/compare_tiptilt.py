import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)

datadir = '/home/deen/Data/GRAVITY/FISBA/TipTilt/refslope0/'
flat = "flat.fits"
files = ["T+T.fits", "T-T.fits", "TT+.fits", "TT-.fits"]

images = []
mask = numpy.ones((1024, 1020), dtype=numpy.bool)
flat_img = pyfits.getdata(datadir+flat)
flat_hdr = pyfits.getheader(datadir+flat)
nonapval=flat_hdr["NONAPVAL"]
new_mask = numpy.not_equal(flat_img, nonapval)
mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())), axis=0).reshape(flat_img.shape)
flat_image = numpy.zeros(flat_img.shape)
flat_image[mask] = flat_img[mask]

for f in files:
    image = pyfits.getdata(datadir+f)
    hdr = pyfits.getheader(datadir+f)
    nonapval = hdr["NONAPVAL"]
    new_mask = numpy.not_equal(image, nonapval)
    mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())), axis=0).reshape(image.shape)
    #complement = numpy.equal(image, nonapval)
    #image[complement] = numpy.median(image[mask])
    images.append(image)

images = numpy.array(images)

minval = numpy.min(images[:,mask]-flat_image[mask])
maxval = numpy.max(images[:,mask]-flat_image[mask])

for i in range(len(images)):
    ax = fig.add_axes([0.1+0.4*(i/2), 0.1+0.4*(i%2), 0.4, 0.4])
    template = numpy.zeros(image.shape)
    template[mask] = images[i,mask]
    im = ax.imshow(template-flat_image, vmin=minval, vmax=maxval)

fig.show()
