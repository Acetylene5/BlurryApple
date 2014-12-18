import scipy
import pyfits
import matplotlib.pyplot as pyplot
import numpy
import PIL

class image(object):
    def __init__(self, df):
        self.pil = PIL.Image.open(df)
        #a = list(self.pil.getdata())
        self.data = numpy.reshape(numpy.array(list(self.pil.getdata()))[:,1],
                self.pil.size)
                #(self.pil.size[1], self.pil.size[0]))

    def subtract(self, other):
        self.data -= other.data

    def add(self, other):
        self.data += other.data

    def smart_threshold(self):
        median = numpy.median(self.data)
        std = numpy.std(self.data)
        mask = scipy.where(self.data < median+5.0*std)
        self.data[mask] = 0.0

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
datadir = '/home/deen/Data/GRAVITY/Alignment/WOAC/IR CAM TEST/'
bf = 'Background001.BMP'
df = 'CD_037_export001.BMP'

bkgnd = image(datadir+bf)
im = image(datadir+df)
#im.subtract(bkgnd)
#im.threshold(60.0)
#im.smart_threshold()
im.centroid()


print im.xcent
print im.ycent

ax.imshow(im.data)
fig.show()

#Threshold

#Compute weighted COG

#Print Results

#Profit
