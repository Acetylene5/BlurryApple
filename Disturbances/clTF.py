import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import leastsq as lsq

fig = pyplot.figure(0)
fig.clear()

closeddf = '/home/deen/Data/GRAVITY/LoopClosure/cld_1/cld_1.fits'
opendf = '/home/deen/Data/GRAVITY/LoopClosure/old/old.fits'
CMf = '/home/deen/Code/Python/BlurryApple/Control/Output/HODM_CM20.fits'

cl = pyfits.getdata(closeddf)
op = pyfits.getdata(opendf)
CM = pyfits.getdata(CMf)
CM = CM[0:60]

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

projections_CL = []
projections_OP = []
for og, cg in zip(op_grad, cl_grad):
    projections_CL.append(CM.dot(cg))
    projections_OP.append(CM.dot(og))


projections_CL = numpy.array(projections_CL)
projections_OP = numpy.array(projections_OP)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#ax.plot(projections[:,0])
#ax.plot(hodm[:,0])
#ax.scatter(hodm[0:400,0], projections[1:401,0])

for i in range(60):
    op_sig_P = projections_OP[:,i]
    cl_sig_P = projections_CL[:,i]

    FFT_OP = numpy.fft.fft(op_sig_P)
    FFT_CL = numpy.fft.fft(cl_sig_P)

    ratio = FFT_CL/FFT_OP
    ratio_freq = numpy.fft.fftfreq(len(op_sig_P), d=d)
    #phase = numpy.arctan(ratio)
    #phase = numpy.arctan2(numpy.imag(ratio), numpy.real(ratio))

    """
freqs = scipy.where( (ratio_freq > 0) & (ratio_freq < 20.0))[0]

guess = [-1.0]

def calc_error(g, xvals, yvals):
    e = 0.0;
    for x, y in zip(xvals, yvals):
        e+= (x*g[0] - y)**2.0
    return e

fit = lsq(calc_error, guess, args=(ratio_freq[freqs], phase[freqs]))

line = []

for i in ratio_freq[freqs]:
    line.append(i*fit[0][0])
    """
    ax.clear()
    ax.plot(ratio_freq, numpy.abs(ratio))
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ybound(1e-2, 1e2)
    #ax.plot(ratio_freq[freqs], phase[freqs])
    #ax.plot(ratio_freq[freqs], line)

    #latency = fit[0][0]/(2.0*3.14159)
    #print "Latency : ", numpy.abs(latency)
    #ax.plot(ratio_freq, numpy.abs(ratio))
    fig.show()
    print i
    raw_input()
