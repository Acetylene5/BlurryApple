import scipy
import numpy
import matplotlib.pyplot as pyplot

class wavefront( object ):
    def __init__(self, subsampling):
        self.subsampling = subsampling
        self.time = 0.0

    def generate_data(self, dt):
        t = numpy.arange(self.time, self.time+dt, self.subsampling)
        d = scipy.randn(len(t))+50.0*numpy.sin(t)+13.0*numpy.cos(t*23.0)
        self.time = t[-1]
        return d

    def move_actuator(self, correction):
        self.correction = correction

class detector( object ):
    def __init__(self, sampling_rate, openloop, closedloop):
        self.sampling_rate = sampling_rate
        self.openloop = openloop
        self.closedloop = closedloop

    def integrate(self):
        dt = 1.0/self.sampling_rate
        ol = self.openloop.generate_data(dt)
        cl = self.closedloop.generate_data(dt)
        int_open = numpy.sum(ol)/len(ol)
        int_closed = numpy.sum(cl)/len(cl)
        return int_open, int_closed

class controlcomputer( object ):
    def __init__(self, refpos):
        self.refpos = refpos

    def calculate_correction(self, measurement):
        correction = self.refpos - measurement
        return correction

class deformablemirror( object ):
    def __init__(self, wavefront):
        self.wave = wavefront
        self.correction = 0.0

    def apply_correction(self, correction):
        self.correction += correction

    def correct_wavefront(self, dt):
        data = self.wave.generate_data(dt) + self.correction
        return data

    def generate_data(self, dt):
        return self.correct_wavefront(dt)

class realtimecomputer( object ):
    def __init__(self):
        self.wave = wavefront(0.001)
        self.dm = deformablemirror(self.wave)
        self.det = detector(500.0, self.wave, self.dm)
        self.cc = controlcomputer(0.0)

    def closeloop(self, looptime):
        open_loop = []
        closed_loop = []
        time = []
        correction = []
        while self.wave.time < looptime:
            ol, cl = self.det.integrate()
            corr = self.cc.calculate_correction(cl)
            self.dm.apply_correction(corr)

            open_loop.append(ol)
            closed_loop.append(cl)
            correction.append(self.dm.correction)
            time.append(self.wave.time)

        self.open_loop = numpy.array(open_loop)
        self.closed_loop = numpy.array(closed_loop)
        self.time = numpy.array(time)
        self.correction = numpy.array(correction)

rtc = realtimecomputer()
rtc.closeloop(100.0)

fig = pyplot.figure(0)
fig.clear()

a = fig.add_axes([0.1, 0.1, 0.8, 0.8])
a.plot(rtc.time, rtc.open_loop)
a.plot(rtc.time, rtc.closed_loop)
a.plot(rtc.time, rtc.correction)

fig.show()
