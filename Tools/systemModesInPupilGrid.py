import scipy
import numpy
import matplotlib.pyplot as pyplot
from scipy.linalg import *
import pyfits

fig = pyplot.figure(0, figsize=(20,15))
fig.clear()

IMdf = '/home/deen/Data/GRAVITY/InteractionMatrices/HODM_HighSNR_IM.fits'
IFMdf = '/home/deen/Data/GRAVITY/InfluenceFunctions/IFs_nov82013/IF_cube.fits'

IM = scipy.matrix(pyfits.getdata(IMdf))
IFM = pyfits.getdata(IFMdf)

U,S,V = svd(IM)

mode = numpy.zeros(IFM.shape[0])
modeStack = numpy.zeros([IFM.shape[1], IFM.shape[2], IM.shape[1]])

for i in range(len(V[0])):
    mode[:] = V[i,:]
    for j in range(IM.shape[1]):
        modeStack[:,:,i] = modeStack[:,:,i] + mode[j]*IFM[j,:,:]
    ax = fig.add_axes([0.1+(i/8)*0.1, 0.1+(i%8)*0.1, 0.1, 0.1])
    m = ax.imshow(modeStack[:,:,i])
    ax.set_xticks([])
    ax.set_yticks([])

fig.savefig("SystemModes.png")
fig.show()
