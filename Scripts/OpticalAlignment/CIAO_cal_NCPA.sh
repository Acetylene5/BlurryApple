# Purpose: Calibrate static aberrations between the reference Nasmyth point
#   source and the VLTI lab
# Description: A point source created by the LSM is observed by the acquisition
#   camera, and time-averaged low-order aberrations are provided to the AO RTC.
#   The AO RTC incoreporates these aberrations into the calculation of the
#   correction signal sent to the MACAO DM.  The procedure is iterated until
#   sufficiently low residual aberrations are observed by the acquisition
#   camera. The observations are carried out for different VLTI configurations
#   (delay line length, VCM settings).

# Setup Optical Path
Move Filter Wheel to Open (ND/HK/?) position
Turn on Nasmyth Reference light source
Move AOMS to Off-Axis Position
Establish communication with VLTI acquisition camera

# Take initial data
Close the CIAO loop
Record data with VLTI acquisition camera for 100 seconds
Open the CIAO loop

# Process the data, iterate until convergence
Get images from the VLTI acquisition camera
Process images, calculate aberrations
Apply calculated NCPA to reference slopes
Close the CIAO loop
Record data with VLTI acquisition camera for 100 seconds
Open the loop

Repeat process with On-Axis beam
