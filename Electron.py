from Walker import Walker
import numpy as np
from itertools import zip_longest as zip


class Electron:

    def __init__(self, id, nbr_of_walkers = 10, dims = 1, walkers = None):

        # Set parameters of object
        self.id             = id

        # Other parameters
        self.nbr_of_walkers = None
        self.walkers        = []
        self.dims           = dims

        # Walker derived parameters
        self.positions      = None
        self.distances      = []

        # Set walkers: Either list of supplied walkers or random initializations
        self.set_walkers(nbr_of_walkers, walkers)


    def set_walkers(self, nbr_of_walkers, walkers):
        
        if walkers:

            # Set number of walkers
            self.nbr_of_walkers = len(walkers)
            
            # Set list of walkers
            self.walkers = walkers

        elif nbr_of_walkers:
            
            # Set number of walkers
            self.nbr_of_walkers = nbr_of_walkers

            # Declare new set of walkers
            walkers = []

            # Create walkers
            for _ in range(self.nbr_of_walkers):

                # Generate random locations
                position = np.random.uniform(-2, 2, self.dims)

                walker = Walker(id=_, 
                                electron=self.id, 
                                position = position)

                walkers.append(walker)

            self.walkers = walkers

        # Walker derived parameters
        self.positions      = self.get_positions()
        self.distances      = self.get_distances()


    def get_positions(self):

        pos = np.zeros((self.nbr_of_walkers, self.dims))

        # Extract all walker positions as a numpy array
        for walker, i in zip(self.walkers, range(self.nbr_of_walkers)):
            pos[i] = walker.position

        return pos

    def get_distances(self):

        return np.linalg.norm(self.positions, ord=2, axis=1)


    def __str__(self):

        outstring = ""

        for walker in self.walkers:
            outstring += "Walker %d\t at x = [%.3f, %.3f, %.3f]\t with m = %.3f\n" % (walker.id, 
                                                                                walker.position[0], 
                                                                                walker.position[1], 
                                                                                walker.position[2], 
                                                                                walker.merit)

        return outstring