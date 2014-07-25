import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import leastsq as lsq

fig = pyplot.figure(0)
fig.clear()

closeddf = '/home/deen/Data/GRAVITY/LoopData/ClosedLoopx10k.fits'
CMf = '/home/deen/Code/Python/BlurryApple/Control/Output/HODM_CM20.fits'

cl = pyfits.getdata(closeddf)
CM = pyfits.getdata(CMf)
CM = CM[0:60]

cl_frames = cl.field(0)
cl_times = cl.field(1)+1e-6*cl.field(2)
cl_grad = cl.field(4)

counter = numpy.array(range(len(cl_times)-1))
avg_dt = cl_times[counter+1] - cl_times[counter]
print numpy.mean(avg_dt)
d = numpy.mean(avg_dt)   # time between integrations

projections_CL = []
for cg in cl_grad:
    projections_CL.append(CM.dot(cg))


projections_CL = numpy.array(projections_CL)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for i in range(3):
    cl_sig_P = projections_CL[:,i]

    FFT_CL = numpy.fft.fft(cl_sig_P)

    ratio_freq = numpy.fft.fftfreq(len(cl_sig_P), d=d)
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
    ax.plot(ratio_freq, numpy.abs(cl_sig_P))
    ax.set_xscale('log')
    ax.set_yscale('log')
    #ax.set_ybound(1e-2, 1e2)
    #ax.plot(ratio_freq[freqs], phase[freqs])
    #ax.plot(ratio_freq[freqs], line)

    #latency = fit[0][0]/(2.0*3.14159)
    #print "Latency : ", numpy.abs(latency)
    #ax.plot(ratio_freq, numpy.abs(ratio))
    fig.show()
    print i
    raw_input()
