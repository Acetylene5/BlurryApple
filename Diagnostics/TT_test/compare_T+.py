import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot
import looptools

fig = pyplot.figure(0)

IF_file = '../../Tools/IF_cube_HR.fits'
ifcube = pyfits.getdata(IF_file)
FISBA_datadir = '/home/deen/Data/GRAVITY/FISBA/TipTilt/refslope0/'
loopdir = '/home/deen/Data/GRAVITY/LoopClosure/'
flat_loop = loopdir+'flat_2/flat_2.fits'

flat_img = pyfits.getdata(FISBA_datadir+'flat.fits')
flat_hdr = pyfits.getheader(FISBA_datadir+'flat.fits')
mask = numpy.ones((1024, 1020), dtype=numpy.bool)
nonapval = flat_hdr["NONAPVAL"]
new_mask = numpy.not_equal(flat_img, nonapval)
mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())),
        axis=0).reshape(flat_img.shape)
flat_image = numpy.zeros(flat_img.shape)
flat_image[mask] = flat_img[mask]

prefixes = ["T+T", "T-T", "TT+", "TT-"]
closed_frame_nums = [1812095, 1836160, 1848362, 1863631]

for prefix, cfn in zip(prefixes, closed_frame_nums):

    print prefix
    fig.clear()
    FISBA_open = FISBA_datadir+prefix+".fits"
    FISBA_closed = FISBA_datadir+prefix+"_closed.fits"
    TT_loop = loopdir+prefix+'/'+prefix+'.fits'

    mask = numpy.ones((1024, 1020), dtype=numpy.bool)
    open_img = pyfits.getdata(FISBA_open)
    open_hdr = pyfits.getheader(FISBA_open)
    nonapval=open_hdr["NONAPVAL"]
    new_mask = numpy.not_equal(open_img, nonapval)
    mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())),
            axis=0).reshape(open_img.shape)
    open_image = numpy.zeros(open_img.shape)
    open_image[mask] = open_img[mask]

    closed_img = pyfits.getdata(FISBA_closed)
    closed_hdr = pyfits.getheader(FISBA_closed)
    nonapval=closed_hdr["NONAPVAL"]
    new_mask = numpy.not_equal(closed_img, nonapval)
    mask = numpy.all(numpy.vstack((mask.ravel(),
        new_mask.ravel())), axis=0).reshape(closed_img.shape)
    closed_image = numpy.zeros(closed_img.shape)
    closed_image[mask] = closed_img[mask]

    flatloop = looptools.readLoopFile(flat_loop)
    TTloop = looptools.readLoopFile(TT_loop)

    flat_dms = flatloop.field(5)
    TT_dms = TTloop.field(5)
    TT_frames = TTloop.field(0)

    closed = scipy.where(TT_frames > cfn)

    avg_flat = numpy.mean(flat_dms, axis=0)
    avg_closed = numpy.mean(TT_dms[closed], axis=0)

    difference = avg_closed-avg_flat

    result = open_image.copy()

    for diff, IF in zip(difference, ifcube):
        new_mask = numpy.isfinite(IF)
        mask = numpy.all(numpy.vstack((mask.ravel(), new_mask.ravel())),
                axis=0).reshape(closed_img.shape)
        result[mask] += IF[mask]*diff*10000.0*1.0

    mx = numpy.max([closed_image-flat_image, result-flat_image])
    mn = numpy.min([closed_image-flat_image, result-flat_image])

    ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.4])
    ax2 = fig.add_axes([0.5, 0.5, 0.4, 0.4])
    #j = ax2.imshow(closed_image, vmin = mn, vmax =mx)
    #i = ax1.imshow(result, vmin = mn, vmax = mx)
    j = ax2.imshow(flat_image, vmin = mn, vmax =mx)
    i = ax1.imshow(result, vmin = mn, vmax = mx)

    #ax.plot(avg_closed)
    fig.colorbar(i)
    fig.show()
    raw_input()
