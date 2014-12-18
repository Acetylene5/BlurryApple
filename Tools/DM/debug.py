import pyfits
import numpy
import scipy
import VLTTools
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#ax2 = fig.add_axes([0.1, 0.5, 0.8, 0.4])

df = '/home/deen/Data/GRAVITY/LoopData_10.fits'

data = pyfits.getdata(df)

gradients = data.field(4)
hodm = data.field(5)
ttm = data.field(6)
seconds = data.field(0)

#ax1.plot(seconds, gradients[:,0])
for i in range(16):
    ax1.plot(seconds, gradients[:,i])

#for i in range(60):
#    ax1.plot(seconds, hodm[:,i])

#for i in range(2):
#    ax2.plot(seconds, ttm[:,i])

fig.show()
