# Purpose: To measure the subaperture pixel scale
# Description: To calibrate the subaperture pixel scale, the flattened DM is 
#    illuminated with the Nasmyth light source.  The Tip/Tilt mount is moved
#    by a known/calibrated amount.  The distance moved by the subaperture is 
#    then used to calibrate the plate scale of the WFS.

# Setup Optical Path
Move Filter Wheel to open/HK/ND position
Turn on Nasmyth light source
Move AOMS to On/Off axis position
Move Derotator to nominal postion
Apply derotator-specific correction to reference slopes
Apply Flat Pattern + Static Aberrations
Center the Tip/Tilt Mount
Verify gradients are within a given range of stored values

# Perform measurements
Apply a calibrated tilt of a known angle.
Record subaperture positions/gradients
Return Tilt mount to the nominal position
Apply a calibrated tip of a known angle
Record subaperture positions/gradients
Return Tip mount to the nominal position

Calculate mean pixel shift for known angle.
Store in CDMS

Turn off Nasmyth light source

