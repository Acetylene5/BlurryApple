import looptools

df = '/home/deen/Data/GRAVITY/LoopClosure/alpha_2/alpha_2.fits'

x, y, stdx, stdy = looptools.measureResidualGradients(df)

print x, y, stdx, stdy
