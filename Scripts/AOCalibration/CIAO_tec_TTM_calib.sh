# Purpose: Calibrate the tip/tilt mount response
# Description: Calibration of the Tip/Tilt mount using the acquisition camera

# Setup Optical path
Turn on Nasmyth light source
Move AOMS to off-axis beam (so beam from Nasmyth LS passes to tunnel)
Establish Communication with the VLTI Acquisition camera
Flatten Mirror
Set Tip/Tilt mirror to 0,0 values
Apply NCPA

# Prepare to take data
Acquire source with Acquisition Camera
Find centroid
Apply sequence of motions on the Tip mount
Record/track motion of image on acquisition camera
Using plate scale, calibrate stroke of DM in arcsec
Return Tip mount to center value
Repeat process with Tilt mount
Save values in CDMS

# Clean up
Turn off Nasmyth light source
