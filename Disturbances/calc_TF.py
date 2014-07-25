import scipy
import pyfits
import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import leastsq as lsq

fig = pyplot.figure(0)
fig.clear()

df = '/home/deen/Data/GRAVITY/Disturbance/disturb_0_0.1_open/disturb_0_0.1_open.fits'
CMf = '/home/deen/Code/Python/BlurryApple/Control/Output/HODM_CM20.fits'

data = pyfits.getdata(df)
CM = pyfits.getdata(CMf)
CM = CM[0:60]

frames = data.field(0)
times = data.field(1)+1e-6*data.field(2)
grad = data.field(4)
hodm = data.field(5)

counter = numpy.array(range(len(times)-1))
avg_dt = times[counter+1] - times[counter]
print numpy.mean(avg_dt)
d = numpy.mean(avg_dt)

projections = []
for g in grad:
    projections.append(CM.dot(g))

projections = numpy.array(projections)

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

#ax.plot(projections[:,0])
#ax.plot(hodm[:,0])
#ax.scatter(hodm[0:400,0], projections[1:401,0])

sig_H = hodm[0:400,0]
sig_P = projections[0:400,0]

FFT_H = numpy.fft.fft(sig_H)
FFT_P = numpy.fft.fft(sig_P)

ratio = FFT_P/FFT_H
ratio_freq = numpy.fft.fftfreq(len(sig_H), d=d)
#phase = numpy.arctan(ratio)
phase = numpy.arctan2(numpy.imag(ratio), numpy.real(ratio))

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

ax.plot(ratio_freq[freqs], phase[freqs])
ax.plot(ratio_freq[freqs], line)

latency = fit[0][0]/(2.0*3.14159)
print "Latency : ", numpy.abs(latency)
#ax.plot(ratio_freq, numpy.abs(ratio))
fig.show()
