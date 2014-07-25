import pyfits
import matplotlib.pyplot as pyplot
import scipy
import numpy

datadir = '/home/deen/Data/GRAVITY/InfluenceFunctions/IFs_nov82013/'

fig = pyplot.figure(0, figsize=(20, 15))
fig.clear()

influence_functions = []
N_act = 60
rebinned_img_width = 64
rebinned_IF_cube = numpy.zeros((N_act, rebinned_img_width, rebinned_img_width))

for i in range(60):
    print i
    ax = fig.add_axes([0.1+(i/8)*0.1, 0.1+(i%8)*0.1, 0.1, 0.1])
    plus_file = datadir+'poke+'+str(i)+'.fits'
    minus_file = datadir+'poke-'+str(i)+'.fits'
    
    plus = pyfits.getdata(plus_file)
    minus = pyfits.getdata(minus_file)
    plus_hdr = pyfits.getheader(plus_file)
    minus_hdr = pyfits.getheader(minus_file)
    img_shape = plus.shape

    nonapval = plus_hdr["NONAPVAL"]

    plus_mask = numpy.not_equal(plus, nonapval)
    minus_mask = numpy.not_equal(minus, nonapval)

    data_mask = numpy.all(numpy.vstack((plus_mask.ravel(),
        minus_mask.ravel())), axis=0).reshape(img_shape)

    y_beg = min(numpy.where(data_mask==True)[0])
    y_end = max(numpy.where(data_mask==True)[0])
    x_beg = min(numpy.where(data_mask==True)[1])
    x_end = max(numpy.where(data_mask==True)[1])

    subtraction = numpy.zeros(img_shape)
    subtraction[data_mask] = plus[data_mask] - minus[data_mask]
    influence_functions.append(subtraction/10000.0)

    bin_size = max([y_end-y_beg, x_end-x_beg])/rebinned_img_width

    if_img = subtraction/10000.0 # Convert from Angstroems to microns

    #"""
    for xbin in range(rebinned_img_width):
        for ybin in range(rebinned_img_width):
            N_sum = 0
            for x in range(x_beg + xbin*bin_size, x_beg+(xbin+1)*bin_size):
                for y in range(y_beg+ybin*bin_size, y_beg+(ybin+1)*bin_size):
                    if (x < img_shape[1] and y < img_shape[0] and
                            data_mask[y,x]==True):
                        rebinned_IF_cube[i, ybin, xbin] += if_img[y,x]
                        N_sum += 1
            if N_sum > 0:
                rebinned_IF_cube[i, ybin, xbin] /= N_sum
            else:
                rebinned_IF_cube[i, ybin, xbin] = 0.0

    ax.imshow(rebinned_IF_cube[i])
    ax.set_yticks([])
    ax.set_xticks([])
    #"""

IFs = numpy.array(influence_functions)
IF_cube_hdu = pyfits.PrimaryHDU( rebinned_IF_cube.astype(numpy.float32))
IF_cube_hdu.writeto('IF_cube_zeros.fits', clobber=True)
#IF_cube_hdu = pyfits.PrimaryHDU( IFs.astype(numpy.float32))
#IF_cube_hdu.writeto('IF_cube_HR.fits', clobber=True)

#pyfits.writeto('IF_cube.fits', IFs)
#fig.show()
#fig.savefig("IF_cube.png")
