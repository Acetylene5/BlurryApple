# Purpose: Measure the field-lens interaction matrix
# Description: A circular(?) mask is mounted in front of the DM.  The Naysmith
# reference light source is used to illuminate the DM/Mask  The WFS subaperture
# fluxes are measured for different positions of the X-Y piezo stage holding
# the field lens.

# Required Off-line Setup
Install mask in front of DM

# Setup optical path
Move Filter Wheel to Open (ND? H-band? K-band) Filter position
Move Field Lens to central position
Move Derotator to correct/nominal position
Flatten DM

# Prepare detector for taking images
Set up detector
Take baseline image
Calculate centroid of DM mask

# Generate Interaction Matrix
Move Piezo stage in X-direction
Take image
Calculate centroid of DM mask (dX)
Move Piezo stage back to nominal position
Move Piezo stage in Y-direction
Take image
Calculate centroid of DM mask (dY)
Generate IM
Store IM
Calculate CM
Store CM

