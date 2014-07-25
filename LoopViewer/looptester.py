import scipy
import pyfits
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy

fig = pyplot.figure(0)

#refpos = pyfits.getdata("/home/deen/Data/GRAVITY/")

CM = pyfits.getdata("../Control/Output/HODM_CM21.fits")
CM = CM[0:60]

datadir = '/home/deen/Data/GRAVITY/LoopClosure/closed_loop_1/'
df = datadir+'closed_loop_1.fits'

data = pyfits.getdata(df)

closed_frame = 929842

frames = data.field(0)
grads = data.field(4)
hodms = data.field(5)

fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

avg_grad = numpy.mean(grads, axis=0)
random_grad = numpy.random.randn(136)*0.06

deltapos = CM.dot(avg_grad)
rand_pos = CM.dot(random_grad)

ax.plot(deltapos)
ax.plot(rand_pos)


#for i in [0, 10, 45]:
#    ax.plot(grads[:,i])
#    ax

fig.show()
