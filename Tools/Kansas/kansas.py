import scipy
import numpy
import VLTTools
from pyevolve import Util
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Consts
import math
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

sinewave = numpy.sin(numpy.arange(60))
wave_guess = numpy.zeros_like(sinewave)

def send_actuator_positions_to_DM(actuator_positions):
    #aortc.set_new_flat_map(actuator_positions)
    global wave_guess
    wave_guess = actuator_positions
    #print "Sent Actuator Positions to DM!"

def getStrehlRatio():
    image = getImage()

def getImage():
    """
       Returns an image from the camera
    """

def within_limits(actuator_positions):
    for actpos in actuator_positions:
        if numpy.abs(actpos) > 1.0:
            return False

    return True

def eval_func(deltas):

    actuator_positions = base_map + deltas.genomeList
    if within_limits(actuator_positions):
        send_actuator_positions_to_DM(actuator_positions)
        score = calculateStrehl()
    else:
        score = numpy.finfo(numpy.float).max
    #interferogram = get_interferogram_from_FISBA()
    #score = 1.0/calculate_RMS(interferogram)

    return score

hostname = "aortc3"
username = "spacimgr"

aortc = VLTTools.VLTConnection(hostname=hostname, username=username)

#base_map = pyfits.getdata("base_flat_map.fits")

base_map = numpy.zeros(60)

genome = G1DList.G1DList(60)
genome.setParams(rangemin=-1.0, rangemax=1.0, bestrawscore=0.0000, rounddecimal=4)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
genome.evaluator.set(eval_func)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setMinimax(Consts.minimaxType["minimize"])
ga.setGenerations(8000)
ga.setMutationRate(0.05)
ga.setPopulationSize(100)
ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

ga.evolve(freq_stats=250)

# Best individual
best = ga.bestIndividual()
print best
print "Best individual score: %.2f" % best.getRawScore()

ax.plot(sinewave)
ax.plot(best.genomeList)
fig.show()

