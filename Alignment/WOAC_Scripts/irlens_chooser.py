import scipy
import numpy
import matplotlib.pyplot as pyplot

nx = 320
ny = 256
pitch = 30.0 #microns

diameter = 10.0 #mm
lam = 0.0015  #mm


fl = 27.0 #mm

di = 122.0 #mm

do = 1.0/(1.0/fl - 1.0/di)

mag = -di/do

ho = pitch/mag

airy = (1.22*lam/diameter)*fl

print do, mag, ho, airy
