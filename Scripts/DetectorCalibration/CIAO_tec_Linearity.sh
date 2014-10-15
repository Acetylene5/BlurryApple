# This template determines non-linearity coefficients.
# Description: A halogen light in the LSM is illuminated, the detector 
# linearity is measured by varying the exposure times and measuring 
# the effect on the number of counts

# Not sure we actually can do this with the lenslet array installed

#Setup optical path
Move Filter Wheel to Open Position
Move AOMS to On(Off?)-Axis position

#Prepare to take image
Turn on Reference Light Source
Set up detector

#Take first exposure
Take exposure
Calculate mean counts

#Prepare second image
Change DIT

#Take second exposure
Take exposure
Calcualte mean counts

#How many samples/integration times should we do?
#Repeat ad nauseum

Calculate Linearity
Save linearity coefficients

#Shut Down
Turn off Reference Light Source

