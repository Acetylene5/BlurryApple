import scipy
import numpy
import matplotlib.pyplot as pyplot
from scipy.linalg import *
import pyfits

fig = pyplot.figure(0)

IMdf = '/home/deen/Data/GRAVITY/InteractionMatrices/HO_IM.fits'
IFMdf = '/home/deen/Data/GRAVITY/InfluenceFunctions/IF_cube.fits'

IM = scipy.matrix(pyfits.getdata(IMdf))
IFM = pyfits.getdata(IFMdf)

U,S,V = svd(IM)

mode = numpy.zeros(IFM.shape[0])
modeStack = numpy.zeros([IFM.shape[1], IFM.shape[2], IM.shape[1]])

for i in range(len(V[0])):
    print i
    mode[:] = V[i,:]
    for j in range(IM.shape[1]):
        modeStack[:,:,i] = modeStack[:,:,i] + mode[j]*IFM[j,:,:]
    fig.clear()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    m = ax.imshow(modeStack[:,:,i])
    fig.colorbar(m)
    fig.show()
    raw_input()


