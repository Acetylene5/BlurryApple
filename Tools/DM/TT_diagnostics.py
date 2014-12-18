import pyfits
import numpy
import scipy
import VLTTools
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

df = '/home/deen/Data/GRAVITY/LoopData/LoopData_3.fits'

data = pyfits.getdata(df)

hodm = data.field(5)
ttm = data.field(6)
seconds = data.field(0)

for i in range(60):
    ax.plot(seconds, hodm[:,i])

fig.show()
