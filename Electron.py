from Walker import Walker
import numpy as np
from itertools import zip_longest as zip


class Electron:
    def __init__(self, id, nbr_of_walkers = 10, walkers = None):
        self.id = id
        self.nbr_of_walkers = self.set_nbr_of_walkers(nbr_of_walkers, walkers)
        self.walkers = self.set_walkers(walkers)
        self.positions = self.get_positions()
        self.distances = [walker.distance for walker in self.walkers]


    def set_nbr_of_walkers(self, nbr_of_walkers, walkers = None):

        if walkers:

            return len(walkers)

        else:
            return nbr_of_walkers



    def set_walkers(self, walkers = None):
        
        if walkers:
            
            return walkers

        else:
        
            walkers = []
            id = 0
            for _ in range(self.nbr_of_walkers):
                walker = Walker(id=id, electron=self.id)
                walkers.append(walker)
                id += 1

            return walkers

    def get_positions(self):

        pos = np.zeros((self.nbr_of_walkers, 3))

        for walker, i in zip(self.walkers, range(self.nbr_of_walkers)):
            pos[i] = walker.position

        return pos


    def __str__(self):

        outstring = ""

        for walker in self.walkers:
            outstring += "Walker %d at x = [%.3f, %.3f, %.3f] with m = %.3f\n" % (walker.id, 
                                                                                walker.position[0], 
                                                                                walker.position[1], 
                                                                                walker.position[2], 
                                                                                walker.merit)

        return outstring