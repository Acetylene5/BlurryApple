import pyfits
import numpy
import scipy
import matplotlib.pyplot as pyplot
import emcee

nx = 20
ny = 21

best = -numpy.inf + 1.0
best_model = None

#counter = 0

def lnprob(coord, n, collapsed):
    global best
    global best_model
    #global counter
    length = len(collapsed)
    ampl = coord[:n]
    pattern_start = coord[n]
    pattern_spacing = coord[n+1]
    fwhm = coord[n+2]
    env_ampl = coord[n+3]
    env_center = coord[n+4]
    env_fwhm = coord[n+5]

    model = numpy.zeros(length)
    x = range(length)

    outofbounds = False

    if (fwhm > 2.0*pattern_spacing) | (env_fwhm < n*fwhm) | (pattern_spacing < 2) | (pattern_spacing > length/n) | (pattern_start < 0) | (pattern_start > length) | (env_ampl < 0) | (env_center < 0) | (env_center > length) | (fwhm < 0):
        outofbounds = True
    else:
        for i in range(len(ampl)):
            a = ampl[i]
            c = pattern_start+i*pattern_spacing
            if (0 > a) | (max_x < a) | (c > length) :
                outofbounds = True
            model += a*numpy.exp(-(x-c)**2.0/(2.0*fwhm/2.4)**2.0)

        model+= env_ampl*numpy.exp(-(x-env_center)**2.0/(2.0*env_fwhm/2.4)**2.0)
        lnprob = -numpy.sum((collapsed - model)**2.0)
        #counter += 1

        """
        if (counter > 100) & (not outofbounds):
            counter = 0
            xline.set_ydata(model)
            pyplot.draw()
            print 'random'
            print pattern_start, pattern_spacing, fwhm, env_fwhm, lnprob
            raw_input()

        """

        if lnprob > best:
            best = lnprob
            #xline.set_ydata(model)
            #pyplot.draw()
            #print 'Best!'
            print pattern_start, pattern_spacing, fwhm, env_fwhm, lnprob
            best_model = model.copy()
            #raw_input()


    if outofbounds:
        lnprob = -numpy.inf

    return lnprob

df = 'clocking_image.fits'
data = pyfits.getdata(df)

fig = pyplot.figure(0)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

xcollapse = data.sum(axis=0)
ycollapse = data.sum(axis=1)

xline, = ax.plot(xcollapse)
fig.show()


nwalkers = 10000

iv = []
rng = []

max_x = xcollapse.max()
max_y = ycollapse.max()
length_x = len(xcollapse)
length_y = len(ycollapse)

for i in range(nx):    #Amplitudes
    iv.append(0)
    rng.append(max_x)
iv.append(0)           #pattern start
rng.append(length_x)
iv.append(2)           #pattern spacing
rng.append(10)
iv.append(0)           #FWHM
rng.append(length_x/nx)
iv.append(max_x/3.0)           #envelope amplitude
rng.append(max_x/2.0)
iv.append(0)           #envelope center
rng.append(length_x)
iv.append(0)           #envelope FWHM
rng.append(length_x/2)

ndim = len(iv)

p0x = [iv+numpy.random.rand(ndim)*rng for j in range(nwalkers)]
sampler_x = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[nx, xcollapse])
pos_x, prob, state = sampler_x.run_mcmc(p0x, 500)
print('Burn in complete!')
sampler_x.reset()
sampler_x.run_mcmc(pos_x, 5000)
print('Done!')

xsamples = sampler_x.chain[:,1000:,:].reshape((-1,ndim))

#ax.plot(best_model)
#raw_input()

for i in range(ndim):
    ax.clear()
    print(i)
    ax.hist(sampler_x.flatchain[:,i], 100, color = 'k', histtype='step')
    ax.figure.canvas.draw()
    raw_input()

iv = []
rng = []

for i in range(ny):    #Amplitudes
    iv.append(0)
    rng.append(max_y)
iv.append(0)           #pattern start
rng.append(length_x)
iv.append(2)           #pattern spacing
rng.append(10)
iv.append(0)           #FWHM
rng.append(length_y/ny)
iv.append(0)           #envelope amplitude
rng.append(max_y)
iv.append(0)           #envelope center
rng.append(length_y)
iv.append(0)           #envelope FWHM
rng.append(length_y/2)

ndim = len(iv)

p0y = [iv+numpy.random.rand(ndim)*rng for j in range(nwalkers)]
sampler_y = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[ny, ycollapse])
pos_y, prob, state = sampler_y.run_mcmc(p0y, 500)
print('Burn in complete!')
sampler_y.reset()
sampler_y.run_mcmc(pos_y, 5000)
print('Done!')

ysamples = sampler_y.chain[:,1000:,:].reshape((-1,ndim))

outfile = open('subaperture_positions.dat', 'w')
outfile.write("#Variable   |  Value     |   dPlus   | dMinus")
outfile.write("x_start %f.3 %f.3 %f.3" % (map()) )
