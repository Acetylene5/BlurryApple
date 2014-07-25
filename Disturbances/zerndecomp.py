import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import leastsq as lsq

fig = pyplot.figure(0)
fig.clear()

closeddf = '/home/deen/Data/GRAVITY/LoopClosure/cld_4/cld_4.fits'
opendf = '/home/deen/Data/GRAVITY/LoopClosure/old_2/old_2.fits'
CMf = '/home/deen/Code/Python/BlurryApple/Control/Output/HODM_CM20.fits'
zern = '/home/deen/Data/GRAVITY/Zernike/mrz_9_136.fits'

cl = pyfits.getdata(closeddf)
op = pyfits.getdata(opendf)
CM = pyfits.getdata(CMf)
CM = CM[0:60]
Z = pyfits.getdata(zern)

cl_frames = cl.field(0)
cl_times = cl.field(1)+1e-6*cl.field(2)
cl_grad = cl.field(4)
op_frames = op.field(0)
op_times = op.field(1)+1e-6*op.field(2)
op_grad = op.field(4)

counter = numpy.array(range(len(cl_times)-1))
avg_dt = cl_times[counter+1] - cl_times[counter]
print numpy.mean(avg_dt)
d = numpy.mean(avg_dt)   # time between integrations

pixscale = 0.51 # "/pix
pixscale *= numpy.pi/(180*3600)

Rvlt = 3.25 * 1e6 # radius of pupil in microns

projections_CL = []
projections_OP = []
for og, cg in zip(op_grad, cl_grad):
    projections_CL.append(Z.dot(cg)*pixscale*Rvlt)
    projections_OP.append(Z.dot(og)*pixscale*Rvlt)


noll = numpy.array([0.054015,0.054015,0.0144646,0.0144646,0.0144646,0.00507638,0.00507638, 0.00507638,0.00507638,0.00220356,0.00220356,0.00220356,0.00220356,0.00220356, 0.00111228,0.00111228,0.00111228,0.00111228,0.00111228,0.00111228,0.000624994, 0.000624994,0.000624994,0.000624994,0.000624994,0.000624994,0.000624994,0.000379966,0.000379966,0.000379966,0.000379966,0.000379966,0.000379966, 0.000379966,0.000379966,0.000245272,0.000245272,0.000245272,0.000245272, 0.000245272,0.000245272,0.000245272,0.000245272,0.000245272,0.000165955, 0.000165955,0.000165955,0.000165955,0.000165955,0.000165955,0.000165955,0.000165955,0.000165955,0.000165955])*(0.633/(2.0*3.14159))**2.0

#noll = numpy.array([0.448879,0.448879,0.0232179,0.0232179,0.0232179,0.00619143,0.00619143, 0.00619143,0.00619143,0.00245392,0.00245392,0.00245392,0.00245392,0.00245392, 0.00119041,0.00119041,0.00119041,0.00119041,0.00119041,0.00119041,0.000655102, 0.000655102,0.000655102,0.000655102,0.000655102,0.000655102,0.000655102,0.000393378,0.000393378,0.000393378,0.000393378,0.000393378,0.000393378, 0.000393378,0.000393378,0.000251913,0.000251913,0.000251913,0.000251913, 0.000251913,0.000251913,0.000251913,0.000251913,0.000251913,0.000169519, 0.000169519,0.000169519,0.000169519,0.000169519,0.000169519,0.000169519, 0.000169519,0.000169519,0.000169519])*(0.633/(2.0*3.14159))**2.0

projections_CL = numpy.array(projections_CL)
projections_OP = numpy.array(projections_OP)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

r0 = 400.0

var_CL_um = numpy.sum(numpy.std(projections_CL, axis=0)**2.0)
var_OL_um = numpy.sum(numpy.std(projections_OP, axis=0)**2.0)

lam_IR = 1.25  # ir lamda in microns
SR_CL = numpy.exp(-var_CL_um * (2*3.14159/lam_IR)**2.0)
print 'Strehl at 1.25 um'+str(SR_CL)

ax.plot(numpy.std(projections_CL, axis=0))
ax.plot(numpy.std(projections_OP, axis=0))
ax.plot(numpy.sqrt(noll*(6500/r0)**(5.0/3.0)))
ax.set_yscale('log')
fig.show()
#ax.plot(projections[:,0])
#ax.plot(hodm[:,0])
#ax.scatter(hodm[0:400,0], projections[1:401,0])

