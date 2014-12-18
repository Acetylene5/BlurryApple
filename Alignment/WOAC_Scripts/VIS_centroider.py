import scipy
import pyfits
import matplotlib.pyplot as pyplot
import numpy

class image(object):
    def __init__(self, df):
        self.data = pyfits.getdata(df)
        self.original_data = pyfits.getdata(df)

    def __sub__(self, other):
        self.data -= other.data

    def __add__(self, other):
        self.data += other.data

    def smart_threshold(self):
        self.median = numpy.median(self.data)
        self.std = numpy.std(self.data)
        blank = scipy.where(self.data < self.median+0.25*self.std)
        signal = scipy.where(self.data > self.median+0.25*self.std)
        self.data[blank] = 0.0
        self.data[signal] = 1.0

    def threshold(self, threshold):
        mask = scipy.where(self.data < threshold)
        self.data[mask] = 0.0

    def centroid(self):
        xcollapse = numpy.sum(self.data, axis=0)
        self.xcent = numpy.sum([float(x*xcollapse[x]) for x in 
            range(len(xcollapse))])/numpy.sum(xcollapse)
        ycollapse = numpy.sum(self.data, axis=1)
        self.ycent = numpy.sum([float(y*ycollapse[y]) for y in 
            range(len(ycollapse))])/numpy.sum(ycollapse)

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#Open image, read data
datadir = '/home/deen/Data/GRAVITY/Alignment/WOAC/CCD CAM TEST/'
df = 'test_spot.fits'
#df = 'Focus002_000um.fits'
#datadir = './fakeData/'
#df = 'VIS_fakedata.fits'

im = image(datadir+df)
#im.threshold(60.0)
im.smart_threshold()
im.centroid()


print "x = ", im.xcent
print "y = ", im.ycent

ax.imshow(im.original_data)
#ax.plot(im.xcent, im.ycent, marker='x', color='g')
fig.show()

#Threshold

#Compute weighted COG

#Print Results

#Profit
