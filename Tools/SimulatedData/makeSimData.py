import pyfits
import scipy
import numpy
import matplotlib.pyplot as pyplot
import NGCTools

"""
df1 = '/home/deen/Data/GRAVITY/SimulatedData/ciaoSimulatedFrameBuffer.fits'
df2 = '/home/deen/Data/GRAVITY/SimulatedData/pixelUnscramblingMap.fits'
df3 = '/home/deen/Data/GRAVITY/NAOMI/NAOMI_simulated_buffer_5_frames_rand.fits'

dat1 = pyfits.getdata(df1)
dat2 = pyfits.getdata(df2)
dat3 = pyfits.getdata(df3)

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])


fig.show()
"""

frames = NGCTools.frameBuffer()

frames.generateRandomFrames(nframes=5)

frames.saveFile('test_bright.fits')
frames.saveCentroids('centroids_bright.fits')
