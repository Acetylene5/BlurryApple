import scipy
import numpy
import pyfits
from scipy.linalg import *
import matplotlib.pyplot as pyplot

f1 = pyplot.figure(0)
f1.clear()
a1 = f1.add_axes([0.1, 0.1, 0.8, 0.8])
f2 = pyplot.figure(1)
f2.clear()
a2 = f2.add_axes([0.1, 0.1, 0.8, 0.8])
f3 = pyplot.figure(2)
f3.clear()
a3 = f3.add_axes([0.1, 0.1, 0.8, 0.8])

datadir = '/home/deen/Documents/GRAVITY/Integration_And_Testing/Software/Notes/TipTilt_CloseLoop/'

HODM_IM_df = 'IM_AIT_HODM_Flat.fits'
HODM_CM_df = 'HODM_CM_ESO.fits'
a = pyfits.getdata(HODM_IM_df)
b = pyfits.getdata(datadir+HODM_CM_df)
A = scipy.matrix(a)
c = scipy.matrix.getI(A)

blah = a1.imshow(c)
a1.set_title("Blind Inversion")
junk = a2.imshow(b)
a2.set_title("ESO Inversion")
f1.colorbar(blah)
f1.show()
f2.colorbar(junk)
f2.show()

numFilteredModes = 50
U,S,V = svd(A)
D = 1.0/(S[0:-numFilteredModes])
S[-numFilteredModes+1:-1] = 0.0
newS = numpy.zeros([136,60])
I = [i for i in range(60)]
for i in range(len(D)):
    newS[i][i] = D[i]

S = newS.copy()

retval = V.T.dot(S.T.dot(U.T))

new = a3.imshow(retval)
a3.set_title("PseudoInverse")
f3.colorbar(new)
f3.show()
#I = 1:

