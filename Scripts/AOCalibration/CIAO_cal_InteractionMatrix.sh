# Purpose: Measure the interaction matrix
# Description: A point source created by the Nasmyth LSM is observed
#    by the WFS with a flattened DM, and the positions of the point source
#    calculated in each of the subapertures.  The actuators of the DM are
#    then pushed and pulled according to a pre-defined pattern (e.g. zonal,
#    modal, or Hadamard).  The observed shifts of the point source in the sub
#    apertures are used to calculate the interaction matrix

# Setup optical path
Move Filter Wheel to open (ND/HK/?) position
Turn on NLSM
Apply flat pattern to DM
Move AOMS to On-(Off-?)Axis position
Move Field Lens to nominal position/center the pupil
Move Derotator to nominal position

# Measure Interaction Matrix
Initialize actuator pattern/IM measurement script in SL
Extract IM
Calculate CM
Verify CM
Archive CM
Load CM to System


