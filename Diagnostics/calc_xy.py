import scipy
import numpy
import pyfits
import matplotlib.pyplot as pyplot

def findRegion(x, y, regions):
    for r in range(len(regions)):
        for pix in regions[r]:
            if (abs(x-pix[0]) < 2) & (abs(y-pix[1]) < 2):
                return r
    return -1

def findContiguousRegions(nonzero):
    regions = []
    for x, y in zip(nonzero[0], nonzero[1]):
        index = findRegion(x, y, regions)
        if index >= 0:
            regions[index].append([x, y])
        else:
            regions.append([[x,y]])
    return regions

def computeCentroid(image, coords):
    sdrooc = coords.T
    xvals = numpy.unique(sdrooc[0])
    yvals = numpy.unique(sdrooc[1])
    x = 0.0
    y = 0.0
    x_c = 0.0
    y_c = 0.0
    intensity = 0.0
    i_c = 0.0
    for pix in coords:
        pixval = image[pix[0]][pix[1]]
        intensity += pixval
        x += pixval*pix[0]
        y += pixval*pix[1]
        x_c += pix[0]
        y_c += pix[1]
        i_c += 1.0
    #print x_c/i_c, y_c/i_c
    #print x/intensity, x_c/i_c
    #print y/intensity, y_c/i_c
    return x/intensity, y/intensity, x_c/i_c, y_c/i_c


def avgGradients(image, nonzero):
    gradx = []
    grady = []
    xc_pos = []
    yc_pos = []
    postageStamps = findContiguousRegions(nonzero)
    for postageStamp in postageStamps:
        x, y, x_c, y_c = computeCentroid(image, numpy.array(postageStamp))
        gradx.append(x-x_c)
        grady.append(y-y_c)
        xc_pos.append(x_c)
        yc_pos.append(y_c)

    return gradx, grady, xc_pos, yc_pos



fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

datadir = '/home/deen/Data/GRAVITY/'

image = 'RefSlopes/RefSlopes_5.fits'

bkgnd = 'Bkgnd/Bkgnd.fits'

back = pyfits.getdata(datadir+bkgnd)
backstack = numpy.zeros([72, 72])

f = numpy.resize(back[0][-1].copy(), [72,72])
nonzero = numpy.nonzero(f)
backstack += f
initial_median = numpy.median(f[nonzero])

for frame in back[1:]:
    f = numpy.resize(frame[-1].copy(), [72, 72])
    backstack += f*initial_median/numpy.median(f[nonzero])

backstack /= float(len(back))

data = pyfits.getdata(datadir+image)
imgstack = numpy.zeros([72, 72])

f = numpy.resize(data[0][-1].copy(), [72, 72])
imgstack += f
#nonzero = numpy.nonzero(f)
#initial_median = numpy.median(f[nonzero])
f = numpy.resize(data[0][-1].copy(), [72, 72])
nonzero = numpy.nonzero(f)
initial_median = numpy.median(f[nonzero])

for frame in data[1:]:
    f = numpy.resize(frame[-1].copy(), [72, 72])
    imgstack+= f*initial_median/numpy.median(f[nonzero])

imgstack /= float(len(data))

calibrated = imgstack
#calibrated = imgstack - backstack

gx, gy, x_c, y_c = avgGradients(calibrated, nonzero)

#calibrated[nonzero] += 50000.0

ax.imshow(calibrated.transpose())
ax.scatter(x_c, y_c, color = 'r', marker = '+')
ax.scatter(numpy.array(x_c)+numpy.array(gx), numpy.array(y_c)+numpy.array(gy), color = 'k', marker = '+')

for p in zip(x_c, y_c, gx, gy):
    ax.plot([p[0], p[0]+p[2]], [p[1], p[1]+p[3]], color = 'k')

print("Mean X gradient: %f" % numpy.mean(gx))
print("Mean Y gradient: %f" % numpy.mean(gy))

ax.set_title("Gradients: x=%5.3f, y=%5.3f" %(numpy.mean(gx), numpy.mean(gy)))

fig.show()
#fig.savefig('centroids_stretch.png')
#fig.savefig('centroids.png')
