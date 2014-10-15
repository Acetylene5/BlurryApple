import scipy
import numpy

#This routine calculates the displacement of the focus point given
#an entrance window of index n and thickness d

n = 3.4

d = 2.0       #mm


focal_length = 1100.0 #mm
beam_diameter = 80.0  #mm

theta0 = numpy.arctan(beam_diameter/(2.0*focal_length))

theta1 = numpy.arcsin(numpy.sin(theta0)/n)

focal_distance = d*(1.0- numpy.tan(theta1)/numpy.tan(theta0))

print focal_distance


