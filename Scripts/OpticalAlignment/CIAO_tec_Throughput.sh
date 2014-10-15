# Purpose: Monitor the throughput for the different AO mode selector settings
# with an artificial source
# Description: An intensity-stabilized point source created by the CNWRS is 
# observed by the WFS, and the integrated flux is measured in each of the sub
# apertures.  The observations are carried out for each AO mode selector
# setting for GRAVITY (Off- and On-axis).

# Setup optical path
Move Filter Wheel to open (ND/H/K-band?) filter position
Move AOMS to On-axis position
Turn on CNWRS

# Prepare to take images
Setup detector (DIT, read-out mode)
Take sequence of 100 images
Compute median image
Compute integrated flux
Store image, integrated flux in archive
Compare integrated flux to historical trend (generate plot?)

# Test Off-axis position
Move AOMS to Off-Axis position
Take sequence of 100 images
Turn off CNWRS
Compute median image
Compute integrated flux
Store image, integrated flux in archive
Compare integrated flux to historical trend (generae plot?)

#Clean up?
