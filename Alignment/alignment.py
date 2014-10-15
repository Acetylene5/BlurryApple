import scipy
import numpy
import matplotlib.pyplot as pyplot
import pyfits
from scipy import optimize

class postage_stamp( object ):
    def __init__(self, nx=8, ny=8):
        self.image = numpy.zeros((nx, ny), dtype=numpy.float32)
        self.xcenters = []
        self.ycenters = []
        self.fwhms = []

    def add(self, data):
        #fit = self.fit_gaussian(data)
        scaling_factor = numpy.max(data)
        self.image += data/scaling_factor

    def show(self):
        fig = pyplot.figure(0)
        fig.clear()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        ax.imshow(self.image)
        fig.show()

def fit_line(x, y):
    fitfunc = lambda p, x : p[0]+(x*p[1])
    errfunc = lambda p, x, y: numpy.abs(fitfunc(p,x) - y)
    coeffs = [numpy.mean(y), 0.1]
    pfit = optimize.leastsq(errfunc, coeffs, args=(x,y) )

    return numpy.arctan(numpy.abs(pfit[0][1]))*180.0/3.14159262

def sufficient_flux(x, y, img):
    median = 16*numpy.median(img)
    flux = numpy.sum(img[round(y-2):round(y+2),round(x-2):round(x+2)])
    #print x, y
    #print median, flux
    #raw_input()
    return flux > 50.0*median

def calc_cog(img):
    nx = len(img)
    ny = len(img[0])
    valx = 0.0
    valy = 0.0
    tot = 0.0
    for i in range(nx):
        for j in range(ny):
            valx += i*img[i][j]
            valy += j*img[i][j]
            tot += img[i][j]


    return valx/tot + x-2, valy/tot + y-2

def extract(x, y, img):
    background = numpy.median(img)
    stamp = img[round(y-4):round(y+4),round(x-3):round(x+5)]
    stamp -= background
    xcog, ycog = calc_cog(stamp)
    return stamp, xcog, ycog

def subtract_gradient(img):
    background = img[:,0:70]
    gradient = background.sum(axis=1)/len(background[0,:])
    cleaned = img.copy()
    for i in range(len(img[0])):
        cleaned[:,i] -= gradient

    return cleaned



subaperture_positions_file = open('subaperture_positions.dat', 'r')
xpositions = numpy.array(subaperture_positions_file.readline().split(), 
        dtype=numpy.float32)
ypositions = numpy.array(subaperture_positions_file.readline().split(),
        dtype=numpy.float32)
subaperture_positions_file.close()

df = 'clocking_image.fits'
data = pyfits.getdata(df)

cleaned = subtract_gradient(data)

stacked = postage_stamp()
xc = []
yc = []

for x in xpositions:
    for y in ypositions:
        if sufficient_flux(x, y, cleaned):
            extracted, cogx, cogy = extract(x, y, cleaned)
            stacked.add(extracted)
            xc.append(cogx)
            yc.append(cogy)
            #xc.append(x)
            #yc.append(y)

xc = numpy.array(xc)
yc = numpy.array(yc)
xangle = []
yangle = []

for x in xpositions:
    col = scipy.where(abs(xc - x) < 2.0)
    if len(col[0]) > 13:
        xangle.append(fit_line(yc[col], xc[col]))

for y in ypositions:
    row = scipy.where(abs(yc - y) < 2.0)
    if len(row[0]) > 13:
        yangle.append(fit_line(xc[row], yc[row]))

print numpy.mean(xangle), numpy.std(xangle)
print numpy.mean(yangle), numpy.std(yangle)
fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#ax.plot(cleaned.sum(axis=0)/len(cleaned[:,0]))
ax.imshow(cleaned)
ax.scatter(xc, yc, color = 'y')
fig.show()

#stacked.show()
