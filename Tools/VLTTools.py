import os
import paramiko
import numpy
import pyfits
import warnings

class VLTConnection( object ):
    """
    VLTConnection:  This object allows python to log into a computer
    running the VLT SPARTA Light software and do the following:
        - Send a new flat pattern to the DM
        - Retrieve data from the RTC (slopes, intensities, etc...)
        - what else?

    """
    def __init__(self, hostname, username):
        self.hostname = hostname
        self.username = username
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.connect(self.hostname, username=self.username)
        self.ftp = self.ssh.open_sftp()
        self.localpath = './data/'
        self.remotepath = './local/test/'
        self.CDMS = CDMS()

    def set_new_flat_map(self, pattern):
        self.CDMS.maps["HOCtr.ACT_POS_REF_MAP"].replace(pattern)
        self.CDMS.maps["HOCtr.ACT_POS_REF_MAP"].write(path=self.localpath)
        #self.ftp.put(self.localpath+"HOCtr.ACT_POS_REF_MAP.fits", self.remotepath+"HOCtr.ACT_POS_REF_MAP.fits")
        #print "Put flat map on "+self.hostname
        #print "Applying flat map to CDMS"
        #output = self.ssh.command_exec("cdmsLoad -f "+self.remotepath+flat_file+" HOCtr.ACT_POS_REF_MAP --rename")

    

class CDMS_Map( object ):
    def __init__(self, name, ax1, ax2, dtype, filltype, bscale):
        if dtype == "float32":
            self.dtype = numpy.float32
        elif dtype == "float16":
            self.dtype = numpy.float16
        elif dtype == "int32":
            self.dtype = numpy.int32
        elif dtype == "int16":
            self.dtype = numpy.int16
        else:
            print "Error!"
        if filltype == 0.0:
            self.data = numpy.zeros((ax1, ax2), dtype=self.dtype)
        elif filltype >= 1.0:
            self.data = numpy.ones((ax1, ax2), dtype=self.dtype)*filltype
        elif filltype == -1.0:
            self.data = numpy.arange(ax1, dtype=self.dtype)
        else:
            print "Error! I can't understand the fill type!"
        self.data_template = self.data.copy()
        self.bscale = bscale
        self.outfile = name+'.fits'

    def replace(self, newmap):
        self.data = self.dtype(newmap).copy()
        
    def revert(self):
        self.data = self.data_template.copy()

    def write(self, path=''):
        self.hdu = pyfits.PrimaryHDU(self.data)
        if self.bscale == 'minmax':
            self.hdu.scale(option='minmax')
        elif self.bscale == 'True':
            self.hdu.scale()
        warnings.resetwarnings()
        warnings.filterwarnings('ignore', category=UserWarning, append=True)
        self.hdu.writeto(path+self.outfile, clobber=True)
        warnings.resetwarnings()
        warnings.filterwarnings('always', category=UserWarning, append=True)


class CDMS( object ):
    def __init__(self):
        self.maps = {}
        self.populateMapDefs()

    def populateMapDefs(self):
        definitionFile = '../CDMS_Map_Definitions.dat'
        df = open(definitionFile, 'r')
        for line in df:
            l = line.split(',')
            name = l[0]
            ax1 = int(l[1])
            ax2 = int(l[2])
            dtype = l[3].strip()
            filltype = float(l[4])
            bscale = bool(l[5])
            self.maps[name] = CDMS_Map(name, ax1, ax2, dtype, filltype, bscale)

