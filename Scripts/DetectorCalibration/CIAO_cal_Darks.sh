# Purpose: Remove zero level offset and check RON
# Description: Dark frames are obtained regularly for the most commonly used
# detector settings (readout mode, DIT).  Three darks are taken for each
# setting.  These frames can be used to estimate the zero level offset (dark)
# and the RON

# Setup optical path
Move Filter Wheel to Closed Position

For detector configuration in common configurations
   Set up detector
   Take three images
   Median combine the images
   Store median combined dark in CDMS
   Calculate RON
   Store RON in CDMS (or somewhere else)


