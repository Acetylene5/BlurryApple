import scipy
import numpy
import pyfits
from scipy.linalg import *
import matplotlib.pyplot as pyplot
import inversion
import VLTTools

hostname = "aortc3"
username = "spacimgr"

aortc= VLTTools.VLTConnection(hostname=hostname, username = username)



#"""
def pseudoInverse(filename, numFilteredModes=50):
    A = scipy.matrix(pyfits.getdata(filename))

    dims = A.shape
    
    U,S,V = svd(A)
    D = 1.0/(S[0:-numFilteredModes])
    #S[-numFilteredModes+1:-1] = 0.0
    S[-numFilteredModes:] = 0.0
    newS = numpy.zeros([dims[0], dims[1]])
    I = [i for i in range(dims[1])]
    for i in range(len(D)):
        newS[i][i] = D[i]

    #S = newS.copy()

    retval = scipy.matrix(V.T.dot(newS.T.dot(U.T)), dtype=numpy.float32)

    singular_values = newS.diagonal()
    svs = singular_values[singular_values.nonzero()[0]]
    #print asdf
    return retval, numpy.max(svs)/numpy.min(svs), retval.dot(A)
#"""

datadir = './data/'

HOCM = pyfits.getdata('/home/deen/Data/GRAVITY/HODM_CM5.fits')
TTCM = pyfits.getdata('./data/HODM_CM5.fits')


CM = numpy.copy(HOCM)
CM[-2] = TTCM[-2]
CM[-1] = TTCM[-1]
aortc.set_CommandMatrix(CM)

print asdf

#HODM_IMdf, TTM_IMdf = aortc.get_InteractionMatrices()

#HODM_IMdf = datadir+'IM_9Dec2014.fits'
#HODM_IMdf = 'HODM_Calibration_150813.fits'
#HODM_IMdf = 'HO_IM_1021.fits'
HODM_CMdf = 'HODM_CM'

#TTM_IMdf = datadir+'TTRecnCalibrat.RESULT_IM.fits'
#TTM_IMdf = datadir+'TT_IM.fits'
TTM_CMdf = 'TTM_CM.fits'

A = scipy.matrix(pyfits.getdata(datadir+TTM_IMdf)).getI()

cns = []
fmodes = []

inv, cn, junk = pseudoInverse(datadir+HODM_IMdf, 10)
CM = numpy.resize(inv, (62, 136))
CM[-2] = A[0]
CM[-1] = A[1]
pyfits.writeto('data/'+HODM_CMdf+'.fits', CM, clobber=True)

aortc.set_CommandMatrix(CM)

"""
for i in range(57):
    inv, cn, junk = pseudoInverse(HODM_IMdf, i+1)
    fmodes.append(i+1)
    cns.append(cn)
    #CM = inv
    CM = numpy.resize(inv, (62, 136))
    #CM = numpy.zeros((62, 136), dtype='float32')
    #CM[-2] = numpy.zeros(136, dtype='float32')
    #CM[-1] = numpy.zeros(136, dtype='float32')
    CM[-2] = A[0]
    CM[-1] = A[1]
    pyfits.writeto('data/'+HODM_CMdf+str(i)+'.fits', CM, clobber=True)
    #pyfits.writeto('Output/ident_'+str(i)+'.fits', junk.T, clobber=True)

zeros = numpy.zeros(CM.shape, dtype=numpy.float32)
pyfits.writeto("Output/Zeros.fits", zeros, clobber=True)
addone = zeros.copy()
addone[9][37] = 1.0
pyfits.writeto("Output/test.fits", addone, clobber=True)

f = pyplot.figure(0)
f.clear()
ax = f.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_yscale('log')
ax.plot(fmodes, cns)
ax.set_xlabel('Number of Filtered Modes')
ax.set_ylabel('Condition Number')
f.show()
f.savefig('ConditionNumbers.png')

print 'done!'
"""
pyfits.writeto(TTM_CMdf, A, clobber=True)
