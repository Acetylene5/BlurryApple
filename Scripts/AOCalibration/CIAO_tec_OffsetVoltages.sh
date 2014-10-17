# Purpose: Calculate the DM and TT Offset voltages
# Description: Apply reference voltages for achieving a "flat" wavefront,
#    measure residual WFS slopes, apply offset voltages based on previous
#    command matrix, and repeat until convergence.

# Setup Optical Path
Move Filter Wheel to open/HK/ND position
Turn on Nasmyth
