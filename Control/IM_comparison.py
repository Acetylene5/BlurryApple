import scipy
import pyfits
import matplotlib.pyplot as pyplot
import glob
import numpy

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

datadir = './Data/'
dfs = glob.glob(datadir+'IM*.fits')

data = []
amplitude = []

for f in dfs:
    data.append(pyfits.getdata(f))
    hdr = pyfits.getheader(f)
    amplitude.append( hdr["AMPLITUDE"])

data = numpy.array(data)
amplitude = numpy.array(amplitude)

avg = data.mean(0)
std = data.std(0)

#for line in std.T:
#    ax.plot(line)

ax.plot(data[0].T[9])
ax.plot(data[0].T[8])

#ax.imshow(data[3])
#print amplitude[3]

fig.show()
