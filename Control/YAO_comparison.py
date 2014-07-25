import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot

datadir = '/home/deen/Data/GRAVITY/InteractionMatrices/'

synthdf = datadir+'gravity_on_axis_K7-mat.fits'
measdf = datadir+'HODM_HighSNR_IM_8.fits'

synth = pyfits.getdata(synthdf)
meas = pyfits.getdata(measdf)

synIM = synth[0]

subaps = []
for i in range(68):
    subaps.append(i)
    subaps.append(i+68)
subaps = numpy.array(subaps)

norm_synth = []
norm_meas = []

fig = pyplot.figure(0, figsize=(20,15))
fig.clear()
#pyplot.rc('font', family='serif')
pyplot.rc('xtick', labelsize=8)
pyplot.rc('ytick', labelsize=8)
for i in range(8):
    for j in range(8):
        if (i*8+j < 60):
            ax = fig.add_axes([0.1+i*0.1, 0.1+j*0.1, 0.1, 0.1])
            s = synIM[i*8+j][subaps]
            norm_synth.append(numpy.max(numpy.abs(s)))
            s /= 0.0014#norm_synth[-1]
            m = -meas.T[i*8+j]
            norm_meas.append(numpy.max(numpy.abs(m)))
            m /= 0.3#norm_meas[-1]
            ax.plot(s, color='b')
            ax.plot(m, color='r')
            if i != 0:
                ax.set_yticks([])
            if j != 0:
                ax.set_xticks([])
            ax.text(2, 0.7, str(i*8+j))

fig.savefig("YAO_IM_Comparison.png")
fig.show()
raw_input()

norm_synth = numpy.array(norm_synth)
norm_meas = numpy.array(norm_meas)
fig = pyplot.figure(1)
fig.clear()
pyplot.rc('xtick', labelsize=10)
pyplot.rc('ytick', labelsize=10)
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax1.plot(norm_synth, color = 'b')
ax1.set_ylabel('Synthetic', color = 'b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax2 = ax1.twinx()
ax2.plot(norm_meas, color='r')
ax2.set_ylabel('Measured', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
fig.savefig("YAO_IM_norms.png")
