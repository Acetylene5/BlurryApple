import scipy
import SPARTATools

df = '/home/deen/Data/GRAVITY/Henri/Test_Henri_Pixels/Test_Henri_Pixels.fits'

fv = SPARTATools.framesViewer()

fv.loadFile(df)

exit = ''
i = 0
while exit != 'Q':
    fv.showFrame(i)
    i+=1
    exit = raw_input()

