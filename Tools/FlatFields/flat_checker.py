import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot
import glob

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

datadir = '/home/deen/Data/GRAVITY/DetectorTests/FlatFields/Casey/Flats/Double/'
files = glob.glob(datadir+"*s.fits")

ndit = []
dit = []

stacked_frame = numpy.zeros((256,320), dtype=numpy.float32)
nframes = 0.0

for df in files:
   data = pyfits.getdata(df)
   header = pyfits.getheader(df)

   stacked_frame += data/numpy.median(data)
   nframes += 1.0

stacked_frame /= nframes

frame = []
mean = []
std = []

for df in files:
   data = pyfits.getdata(df)
   header = pyfits.getheader(df)
   data /= numpy.median(data)
   data -= stacked_frame
   #frame.append(data)
   ndit.append(header["ESO DET NDIT"])
   dit.append(header["ESO DET SEQ1 DIT"])
   mean.append(data.mean())
   std.append(data.std())

#frame = numpy.array(frame)

ax.scatter(dit, mean, color='r')
ax.scatter(dit, std, color='b')


#ax.imshow(frame.std(axis=0))

fig.show()
