
import numpy as np
import matplotlib.pyplot as plt

results = np.loadtxt("results.data")
#walkers = np.loadtxt("walkers.data")



plt.plot(results[:,1])
plt.plot(results[:,2])
plt.plot(results[:,3])
