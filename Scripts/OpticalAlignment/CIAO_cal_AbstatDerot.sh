# Purpose: To check for static aberrations due to the derotator
# Description: A point source created by the LSM is observed by the WFS.  The
# WFS subaperture fluxes and slopes are measured as a full rotation of the
# derotator is made.  The corrections to the reference slopes are calculated
# as a function of the derotator position

# Set up optical path
Move Filter Wheel to Open Position
Move AOMS to On(Off?)-Axis Position
Move derotator to home position

#Prepare to take image
Turn on Reference Light Source
Set up detector

For angle in angular steps:
   Take image
   Measure slopes, fluxes
   Calculate aberrations
   Save slopes, fluxes
   Move to next angle
   Wait

Calculate static aberrations as function of derotator position
Save to CDMS

#Shut down
Turn off Reference Light Source

