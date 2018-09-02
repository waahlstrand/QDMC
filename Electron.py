from Walker import Walker
import numpy as np
from itertools import zip_longest as zip


class Electron:
    def __init__(self, nbr_of_walkers, number):
        self.number = number
        self.nbr_of_walkers = nbr_of_walkers
        self.walkers = self.get_walkers()
        self.positions = self.get_positions()
        self.distances = [walker.distance for walker in self.walkers]

    def get_walkers(self):
        walkers = []
        number = 0
        for _ in range(self.nbr_of_walkers):
            walker = Walker(number=number, electron=self.number)
            walkers.append(walker)
            number += 1

        return walkers

    def get_positions(self):

        pos = np.zeros((self.nbr_of_walkers, 3))

        for walker, i in zip(self.walkers, range(self.nbr_of_walkers)):
            pos[i] = walker.position

        return pos