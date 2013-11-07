import scipy
import numpy
import pyfits
from scipy.linalg import *
import matplotlib.pyplot as pyplot

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

    S = newS.copy()

    retval = scipy.matrix(V.T.dot(S.T.dot(U.T)), dtype=numpy.float32)

    singular_values = S.diagonal()
    svs = singular_values[singular_values.nonzero()[0]]
    
    return retval, numpy.max(svs)/numpy.min(svs), retval.dot(A)

