#! /usr/bin/env python
"""
Neil Zimmerman

"""

import numpy as np
import os
import pyfits
import matplotlib
import matplotlib.pyplot as plt
import scipy.signal
import scipy.io

if __name__ == "__main__":

    #data_dir = '/home/zimmerman/Data/GRAVITY/fisba/poke_run_2012march12'
    data_dir = '/home/deen/Data/GRAVITY/InfluenceFunctions/IFs_nov82013'
    assert(os.path.exists(data_dir)), 'Error: hard-coded raw data directory %s does not exist' % data_dir
    N_act = 60

    flat_fname_list = [data_dir+'/flat.fits']
    #flat_fname_list = [data_dir + '/flat_before_ring1.fits', data_dir + '/flat_before_ring2.fits', data_dir + '/flat_before_ring3.fits', data_dir + '/flat_before_ring4.fits', data_dir + '/flat_after.fits', data_dir + '/flatten_fillins.fits']

    first_flat_hdulist = pyfits.open(flat_fname_list[0])
    first_flat_hdr = first_flat_hdulist[0].header
    first_flat_img = first_flat_hdulist[0].data
    img_shape = first_flat_img.shape
    nonapval = first_flat_hdr['NONAPVAL']
    first_flat_hdulist.close()

    #
    # Determine the mask that specifies valid pixels in common to all surface measurements
    #
    data_mask = np.not_equal(first_flat_img, nonapval)
    print "%d valid FISBA pixels in first flat" % len(np.where(data_mask == True)[0])

    poke_fname_list = list()
    for i in range(0,N_act):
        poke_fname_list.append(data_dir + '/poke'+str(i)+'.fits')
        poke_hdulist = pyfits.open(poke_fname_list[-1], mode='readonly')
        poke_img = poke_hdulist[0].data
        poke_hdulist.close()
        nonapval_test = np.not_equal(poke_img, nonapval)
        data_mask = np.all(np.vstack((nonapval_test.ravel(), data_mask.ravel())), axis=0).reshape(img_shape)

    for flat_fname in flat_fname_list:
        flat_hdulist = pyfits.open(flat_fname, mode='readonly') 
        flat_img = flat_hdulist[0].data
        flat_hdulist.close()
        nonapval_test = np.not_equal(flat_img, nonapval)
        data_mask = np.all(np.vstack((nonapval_test.ravel(), data_mask.ravel())), axis=0).reshape(img_shape)

    nonap_loc = np.where(data_mask == False)
    y_beg = min(np.where(data_mask == True)[0])
    y_end = max(np.where(data_mask == True)[0])
    x_beg = min(np.where(data_mask == True)[1])
    x_end = max(np.where(data_mask == True)[1])
    print "%d valid FISBA pixels common to all images" % len(np.where(data_mask == True)[0])
    print "Cropping IF data to [%d:%d, %d:%d]" % (y_beg, y_end, x_beg, x_end)

    #
    # For each actuator, subtract the flattened surface measured closest in time,
    # and then rebin the result to a 64x64 array
    #
    IF_dict = dict()
    rebinned_img_width = 64
    rebinned_IF_cube = np.zeros((N_act, rebinned_img_width, rebinned_img_width))
    bin_size = max([y_end - y_beg, x_end - x_beg])/rebinned_img_width
    #for i in range(60,61):
    for i in range(0,N_act):
        if i in [18, 19, 20, 32]:
            flat_fname = flat_fname_list[0]
        elif i <= 4:
            flat_fname = flat_fname_list[0]
        elif i <= 12:
            flat_fname = flat_fname_list[0]
        elif i <= 24:
            flat_fname = flat_fname_list[0]
        elif i <= 40:
            flat_fname = flat_fname_list[0]
        elif i <= N_act:
            flat_fname = flat_fname_list[0]

        flat_hdulist = pyfits.open(flat_fname, 'readonly')
        flat_img = flat_hdulist[0].data
        flat_hdulist.close()
        poke_hdulist = pyfits.open(poke_fname_list[i-1], mode='readonly')
        poke_img = poke_hdulist[0].data
        poke_hdulist.close()

        if_img = (poke_img - flat_img) / 10000. # convert from Angstroems to microns
        for xbin in range(rebinned_img_width):
            for ybin in range(rebinned_img_width):
                N_sum = 0
                for x in range(x_beg + xbin*bin_size, x_beg + (xbin+1)*bin_size):
                    for y in range(y_beg + ybin*bin_size, y_beg + (ybin+1)*bin_size):
                        if x < img_shape[1] and y < img_shape[0] and data_mask[y, x] == True:
                            rebinned_IF_cube[i-1, ybin, xbin] += if_img[y, x]
                            N_sum += 1
                if N_sum > 0:
                    rebinned_IF_cube[i-1, ybin, xbin] /= N_sum
                else:
                    rebinned_IF_cube[i-1, ybin, xbin] = np.nan

    IF_dict['IF_cube'] = rebinned_IF_cube
    IF_cube_fname = data_dir + '/IF_cube.mat'
    scipy.io.savemat(IF_cube_fname, IF_dict, oned_as='row')

    IF_cube_hdu = pyfits.PrimaryHDU( rebinned_IF_cube.astype(np.float32) )
    IF_cube_hdu.writeto(data_dir + '/IF_cube.fits', clobber=True)
