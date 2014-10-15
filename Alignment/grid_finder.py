import pyfits
import numpy
import scipy
import matplotlib.pyplot as pyplot

#Calculates the nominal x and y positions for the images of the lenslet array

def generate_model(npeaks, height, fwhm, spacing):
    feature_width = int(npeaks*spacing+4*fwhm)
    feature_x = numpy.arange(feature_width)
    feature_y = numpy.zeros(feature_width)
    for i in range(npeaks):
        c = (i+1)*spacing
        feature_y += height*numpy.exp(-(feature_x-c)**2.0/(2.0*fwhm/2.4)**2.0)

    return feature_x, feature_y

def find_centers(n, collapse, h, fwhm, spacing):
    x, y = generate_model(n, h, fwhm, spacing)
    y_corr = scipy.correlate(collapse, y)
    x_corr = scipy.linspace(0, len(y_corr)-1, num=len(y_corr))

    peak = x_corr[numpy.argsort(y_corr)[-1]]

    centers = []
    for i in range(n):
        centers.append((i+1)*spacing+peak)

    return numpy.array(centers)

nx = 20
ny = 21


df = 'clocking_image.fits'
data = pyfits.getdata(df)

xcollapse = data.sum(axis=0)
ycollapse = data.sum(axis=1)

fwhm = 2.5
spacing = 8.1
height = 0.75*numpy.max(xcollapse)

xcenters = find_centers(nx, xcollapse, height, fwhm, spacing)
ycenters = find_centers(ny, ycollapse, height, fwhm, spacing)



outfile = open('subaperture_positions.dat', 'w')
for xc in xcenters:
    outfile.write("%.1f " % xc)
outfile.write("\n")
for yc in ycenters:
    outfile.write("%.1f " % yc)
outfile.close()
