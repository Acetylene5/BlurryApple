import scipy
import numpy
import pyfits

#Comments
comment = 'Created by makeMaps.py'

#Number of Apertures
naps = 68
nacts = 60

#=========FLAT==================================
data = numpy.ones((72,72), dtype=numpy.float32)

outfile = 'Acq.DET1.FLAT.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'Acq.DET1.FLAT'))

hdu.writeto("Output/"+outfile, clobber=True)

#==============REFSLOPE

#=========BACKGROUND==================================
data = numpy.zeros((72,72), dtype=numpy.int16)

outfile = 'Acq.DET1.BACKGROUND.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', 'Acq.DET1.BACKGROUND'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========DARK==================================
data = numpy.zeros((72,72), dtype=numpy.int16)

outfile = 'Acq.DET1.DARK.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', 'Acq.DET1.DARK'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========DEAD==================================
data = numpy.zeros((72,72), dtype=numpy.int16)

outfile = 'Acq.DET1.DEAD.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', 'Acq.DET1.DEAD'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========REFSLP==================================
data = numpy.ones((1,136), dtype=numpy.float32)*1.5

outfile = 'Acq.DET1.REFSLP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'Acq.DET1.REFSLP'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========THRESH==================================
data = numpy.ones((1,68), dtype=numpy.int16)*1000.0

outfile = 'Acq.DET1.THRESH.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', 'Acq.DET1.THRESH'))

hdu.writeto("Output/"+outfile, clobber=True)


#=========WEIGHT==================================
data = numpy.ones((1,5184), dtype=numpy.float32)

outfile = 'Acq.DET1.WEIGHT.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'Acq.DET1.WEIGHT'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.ACT_USER_TO_LOGICAL_MAP============
data = numpy.arange(nacts+2, dtype=numpy.int32)

outfile = 'Recn.ACT_USER_TO_LOGICAL_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int32', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.HODM_ACT_USER_TO_LOGICAL_MAP=====
data = numpy.arange(nacts+2, dtype=numpy.int32)

outfile = 'Recn.HODM_ACT_USER_TO_LOGICAL_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int32', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.ACT_UNSCR_MAP============
data = numpy.array([numpy.arange(nacts+2, dtype=numpy.int32)])

outfile = 'Recn.ACT_UNSCR_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int32', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.REC1.CM============
data = numpy.zeros((nacts, 2*naps), dtype=numpy.float32)

for i in range(nacts):
    data[i][i] = 1.0

outfile = 'Recn.REC1.CM.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.SIMVECTOR============
data = numpy.zeros((1,20*naps), dtype=numpy.float32)

for i in range(len(data[0])):
    data[0][i] = i+1

outfile = 'Recn.SIMVECTOR.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========Recn.SUBAP_UNSCR_MAP.fits============
data = numpy.zeros((1,2*naps), dtype=numpy.int32)

for i in range(len(data[0])):
    data[0][i] = i

outfile = 'Recn.SUBAP_UNSCR_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========CODE.MIRROR_HODM.QSPATTERN.fits======
data = numpy.zeros((1,nacts), dtype=numpy.float32)

outfile = 'CODE.MIRROR_HODM.QSPATTERN.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'CODE.MIRROR_HODM.QSPATTERN'))

hdu.writeto("Output/"+outfile, clobber=True)

#=======CODE.MIRROR_HODM.USERMAPPING.fits========
data = numpy.zeros((1,nacts), dtype=numpy.int32)

for i in range(len(data[0])):
    data[0][i] = i

outfile = 'CODE.MIRROR_HODM.USERMAPPING.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', 'CODE.MIRROR_HODM.USERMAPPING'))

hdu.writeto("Output/"+outfile, clobber=True)

#======HOCtr.ACT_POS_REF_MAP.fits===========
data = numpy.zeros((1,nacts), dtype=numpy.float32)

outfile = 'HOCtr.ACT_POS_REF_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#======HOCtr.SMA_BASIS.fits===========
data = numpy.zeros((1,nacts*nacts), dtype=numpy.float32)

for i in range(3600):
    data[0][i] = float(i)+ 1.0

outfile = 'HOCtr.SMA_BASIS.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.SMA_BASIS'))

hdu.writeto("Output/"+outfile, clobber=True)

#======HOCtr.AWF_IM_KERNEL.fits===========
data = numpy.ones((1,nacts*3), dtype=numpy.float32)

outfile = 'HOCtr.AWF_IM_KERNEL.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.AWF_IM_KERNEL'))

hdu.writeto("Output/"+outfile, clobber=True)

#======HOCtr.ACT_UNSCR_MAP.fits===========
data = numpy.zeros((1,nacts), dtype=numpy.int32)

for i in range(len(data[0])):
    data[0][i] = i

outfile = 'HOCtr.ACT_UNSCR_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', 'HOCtr.ACT_USCR_MAP'))

hdu.writeto("Output/"+outfile, clobber=True)

#=====HOCtr.HO_TO_TT.fits================
data = numpy.ones((1,2*nacts), dtype=numpy.float32)

outfile = 'HOCtr.HO_TO_TT.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.HO_TO_TT'))

hdu.writeto("Output/"+outfile, clobber=True)

#======HOCtr.PRA_PISTON_MODE.fits================
data = numpy.ones((1,nacts), dtype=numpy.float32)

outfile = 'HOCtr.PRA_PISTON_MODE.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.PRA_PISTON_MODE'))

hdu.writeto("Output/"+outfile, clobber=True)

#========HOCtr.PRA_PISTON_PROJECTION.fits=========
data = numpy.ones((1,nacts), dtype=numpy.float32)

outfile = 'HOCtr.PRA_PISTON_PROJECTION.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.PRA_PISTON_PROJECTION'))

hdu.writeto("Output/"+outfile, clobber=True)

#========HOCtr.PRA_PISTON_PROJECTION2.fits=========
data = numpy.ones((1,nacts), dtype=numpy.float32)

outfile = 'HOCtr.PRA_PISTON_PROJECTION2.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.PRA_PISTON_PROJECTION2'))

hdu.writeto("Output/"+outfile, clobber=True)

#=======HOCtr.TT_TO_HO.fits=========================
data = numpy.zeros((nacts, 2), dtype=numpy.float32)

outfile = 'HOCtr.TT_TO_HO.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HOCtr.TT_TO_HO'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========HORecnCalibrat.REF_IM.fits==================
data = numpy.zeros((2*naps, nacts), dtype=numpy.float32)

outfile = 'HORecnCalibrat.REF_IM.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HORecnCalibrat.REF_IM'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========HORecnCalibrat.ZONAL_60.fits=================
data = numpy.zeros((nacts, nacts), dtype=numpy.float32)

for i in range(nacts):
    data[i][i] = 1.0

outfile = 'HORecnCalibrat.ZONAL_60.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'HORecnCalibrat.ZONAL_49'))

hdu.writeto("Output/"+outfile, clobber=True)


#=========TTCtr.ACT_POS_REF_MAP.fits====================
data = [0.06, -0.035]

data =  numpy.array(data, dtype='float32')

outfile = 'TTCtr.ACT_POS_REF_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)

#=========LoopDisplaySrv.SUBAP_MAP.fits=================
data = [[ 0,  0,  1,  2,  3,  4,  5,  0,  0],
        [ 0,  6,  7,  8,  9, 10, 11, 12,  0],
        [13, 14, 15, 16, 17, 18, 19, 20, 21],
        [22, 23, 24, 25, 26, 27, 28, 29, 30],
        [31, 32, 33, 34,  0, 35, 36, 37, 38],
        [39, 40, 41, 42, 43, 44, 45, 46, 47],
        [48, 49, 50, 51, 52, 53, 54, 55, 56],
        [ 0, 57, 58, 59, 60, 61, 62, 63,  0],
        [ 0,  0, 64, 65, 66, 67, 68,  0,  0]]
data = numpy.array(data, dtype='uint16')

outfile = 'LoopDisplaySrv.SUBAP_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.scale('int16', bzero=32768, bscale=1)

hdu.writeto("Output/"+outfile, clobber=True)


#=========LoopDisplaySrv.UNSCR_MAP.fits=================
data = numpy.zeros((1, naps), dtype='uint16')

for i in range(naps):
    data[0][i] = float(i)+1

outfile = 'LoopDisplaySrv.UNSCR_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.scale('int16', bzero=32768, bscale=1)

hdu.writeto("Output/"+outfile, clobber=True)


#=========LoopDisplaySrv.HODM_MAP.fits=================
data = [[0, 0, 0, 0, 46, 45, 0, 0, 0, 0],
        [0, 0, 0, 47, 29, 28, 44, 0, 0, 0],
        [0, 0, 48, 30, 16, 15, 27, 43, 0, 0],
        [0, 49, 31, 17, 7, 6, 14, 26, 42, 0],
        [50, 32, 18, 8, 2, 1, 5, 13, 25, 41],
        [51, 33, 19, 9, 3, 4, 12, 24, 40, 60],
        [0, 52, 34, 20, 10, 11, 23, 39, 59, 0],
        [0, 0, 53, 35, 21, 22, 38, 58, 0, 0],
        [0, 0, 0, 54, 36, 37, 57, 0, 0, 0],
        [0, 0, 0, 0, 55, 56, 0, 0, 0, 0]]
data = numpy.array(data, dtype=numpy.int16)

outfile = 'LoopDisplaySrv.HODM_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=======LoodDisplaySrv.HODM_MAP_test.fits==================
data = numpy.zeros((9,9), dtype = numpy.int16)
outfile = "LoopDisplaySrv.HODM_MAP_test.fits"
hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int16', bzero=32768, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#=========LoopMonitor.POSITIONS2FOCUS.fits=================
data = numpy.zeros((1, nacts), dtype=numpy.float32)

for i in range(nacts):
    data[0][i] = i+1

outfile = 'LoopMonitor.POSITIONS2FOCUS.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'LoopMonitor.POSITIONS2FOCUS'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========LoopMonitor.DMPOS_PROJ.fits=================
data = numpy.zeros((nacts, nacts), dtype=numpy.float32)

for i in range(nacts):
    data[i][i] = 1.0

outfile = 'LoopMonitor.DMPOS_PROJ.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'LoopMonitor.DMPOS_PROJ'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========LoopMonitor.SLOPES2FOCUS.fits=================
data = numpy.zeros((1, naps*2), dtype=numpy.float32)

for i in range(naps*2):
    data[0][i] = i+1

outfile = 'LoopMonitor.SLOPES2FOCUS.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'LoopMonitor.SLOPES2FOCUS'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========LoopMonitor.SLOPES2TT.fits=================
data = numpy.zeros((2, naps*2), dtype=numpy.float32)

for i in range(naps*2):
    data[0][i] = i+1
    data[1][i] = 1.0

outfile = 'LoopMonitor.SLOPES2TT.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'LoopMonitor.SLOPES2TT'))

hdu.writeto("Output/"+outfile, clobber=True)

#=========RTC.PROJ_HODM_FOCUS.fits=================
data = numpy.zeros((1, nacts), dtype=numpy.float32)

outfile = 'RTC.PROJ_HODM_FOCUS.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', 'RTC.PROJ_HODM_FOCUS'))

hdu.writeto("Output/"+outfile, clobber=True)


#=========TTCtr.SEC_ACT_UNSCR_MAP=====
data = numpy.arange(nacts, dtype=numpy.int32)

outfile = 'TTCtr.SEC_ACT_UNSCR_MAP.fits'

hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.scale('int32', bzero=0, bscale=1)
hdu.header.append(('EXTNAME', ''))

hdu.writeto("Output/"+outfile, clobber=True)

#========TTCtr.TERM_A
data = [1.0]
data = numpy.array(data, dtype ='float32')
outfile = "TTCtr.TERM_A.fits"
hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)

#========TTCtr.TERM_B
data = [ 0.1, 0.0]
data = numpy.array(data, dtype ='float32')
outfile = "TTCtr.TERM_B.fits"
hdu = pyfits.PrimaryHDU(data)
hdu.header.add_comment(comment)
hdu.header.append(('EXTNAME', ''))
hdu.writeto("Output/"+outfile, clobber=True)

