import scipy
import numpy
import VLTTools

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

