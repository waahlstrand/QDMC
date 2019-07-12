from Walker import Walker
import numpy as np


class Atom:

    def __init__(self, alpha, nbr_of_walkers = None, dims = 1, walkers = [], element = "Hydrogen"):
        
        # Set important state parameters
        self.element            = element
        self.alpha              = alpha
        self.nbr_of_electrons   = self.get_nbr_of_electrons()
        #self.inter_electron_distances = []
        self.dims               = dims
        
        # Set walkers
        self.walkers            = walkers if walkers else self.make_walkers(nbr_of_walkers)        
        self.nbr_of_walkers     = nbr_of_walkers if nbr_of_walkers else len(self.walkers)
        self.max_walker_id      = self.nbr_of_walkers

        # Walker derived values
        self.positions      = self.make_positions()
        self.distances      = self.make_distances()




    def make_walkers(self, nbr_of_walkers):
            
        # Declare new set of walkers
        walkers = []

        # Create walkers
        for _ in range(nbr_of_walkers):

            # Generate random locations
            position = np.random.uniform(-2, 2, self.dims)

            walker = Walker(id=_, position = position)

            walkers.append(walker)

        return walkers

    def make_positions(self):



        pos = np.zeros((self.nbr_of_walkers, self.dims))

        # Extract all walker positions as a numpy array
        for walker, i in zip(self.walkers, range(self.nbr_of_walkers)):

            pos[i] = walker.position

        return pos

    def make_distances(self):

        return np.linalg.norm(self.positions, ord=2, axis=1)

    def get_nbr_of_electrons(self):
        """
        Given an element of a certain type, gives the number of electrons of that element.
        Currently only supports hydrogen and helium
        :return:
        """
        if self.element is ("Hydrogen" or "H"):
            return 1
        elif self.element is ("Helium" or "He"):
            return 2
        else:
            print("Element not supported.")
            return 0

    def make_potential(self):
        """

        :return:
        """

        # Calculate the potential for each walker and electron (a potentially 6D problem)
        K = 1
        potential = 0.5 * K * np.power(self.distances, 2)

        return potential

    def branch_state(self, merits):

        # New walkers
        branch_walkers = []

        for i in range(self.nbr_of_walkers):

            # Make m-1 copies of each walker
            nbr_of_copies = merits[i]

            # Append all copies of these walkers
            for copy_id in range(nbr_of_copies):

                # Make a copy
                walker = self.walkers[i].copy()

                if copy_id > 0:

                    # Update new number of walkers
                    self.max_walker_id += 1
                    
                    walker.id = self.max_walker_id

                   

                branch_walkers.append(walker)


            # Re-number all walkers
            #for walker, i in zip(branch_walkers, range(len(branch_walkers))):
            #    walker.id = i


        # Update state
        self.set_walkers(branch_walkers)


    def set_walkers(self, walkers):

        # Set walkers
        self.walkers = walkers

        # Set number of walkers
        self.nbr_of_walkers = len(walkers)

        # Set walker derived values
        self.positions      = self.make_positions()
        self.distances      = self.make_distances()


    # def get_wavefunction(self):

    #     if self.nbr_of_electrons == 2:
    #         first_electron = self.electrons[0]
    #         second_electron = self.electrons[1]
    #         inter = self.inter_electron_distances

    #         wave_list = np.exp(- 2*first_electron.distances
    #                            - 2*second_electron.distances
    #                            + np.divide(inter, (2*(1 + self.alpha*inter)))
    #                            )

    #         return wave_list

    # def get_inter_electron_distance(self):
    #     """

    #     :return:
    #     """
    #     if self.nbr_of_electrons != 2:
    #         print(self.nbr_of_electrons)

    #     electrons = self.electrons
    #     d_list = []
    #     d = 0

    #     for first_walker, second_walker in zip(electrons[0].walkers, electrons[1].walkers):
    #         for first_pos, second_pos in zip(first_walker.position, second_walker.position):
    #             d += (first_pos-second_pos)*(first_pos-second_pos)

    #         d_list.append(np.sqrt(d))

    #     return np.asarray(d_list)

    # def get_force(self):

    #     force_list = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

    #     for j in range(self.nbr_of_electrons):
    #         for i in range(self.nbr_of_walkers):

    #             electron = self.electrons[j]
    #             other = self.electrons[0] if j == 1 else self.electrons[1]

    #             r = electron.walkers[i].position
    #             r_ = other.walkers[i].position

    #             r1 = electron.walkers[i].distance if j == 1 else other.walkers[i].distance

    #             r12 = self.inter_electron_distances[i]

    #             force_list[j, i] = -4 * r/r1 + 2 * (r-r_)/(r12*(1+self.alpha*r12)*(1+self.alpha*r12))

    #     return force_list

    # def get_force_fast(self):

    #     force = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

    #     first = self.electrons[0].positions
    #     second = self.electrons[1].positions

    #     r1 = self.electrons[0].distances
    #     r2 = self.electrons[1].distances

    #     r12 = self.inter_electron_distances[:, None]

    #     force[0] = -4 * first/r1 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))
    #     force[0] = -4 * second/r2 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))

    # def get_electrons(self):
    #     """

    #     :return:
    #     """
    #     electrons = []

    #     for _ in range(self.nbr_of_electrons):
    #         electron = Electron(nbr_of_walkers=self.nbr_of_walkers, id=_)
    #         electrons.append(electron)

    #     return electrons
