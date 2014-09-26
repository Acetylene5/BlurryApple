import scipy
import matplotlib.pyplot as pyplot
import numpy
import pickle

df = open('junk1.dat', 'rb')
data = pickle.load(df)
df.close()

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

walkers = data.transpose()

for w in data[0:10]:
    ax.plot(w)

fig.show()
