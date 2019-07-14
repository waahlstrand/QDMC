from Walker import Walker
import numpy as np


class Atom:

    def __init__(self, alpha, nbr_of_walkers = 0, dims = 1, walkers = [], element = "Hydrogen"):
        """Initializes the Atom object. Requires either specifying a number of walkers
        or a list of Walker objects.
        
        Arguments:
            alpha {double} -- Hyperparameter describing the step size of the trial energy updates.
        
        Keyword Arguments:
            nbr_of_walkers {int} -- An int describing the number of walkers. (default: {None})
            dims {int} -- The number of dimensions of the Atom. (default: {1})
            walkers {list} -- A list of Walker objects. (default: {[]})
            element {str} -- The element to simulate, either Hydrogen or Helium. (default: {"Hydrogen"})
        """
        
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
        """Creates a list of Walker objects given a number of walkers. Initialized uniformly in
        [-2, 2]. The dimensionality is decided by the object parameter dims.
        
        Arguments:
            nbr_of_walkers {int} -- The desired number of walkers in the list.
        
        Returns:
            list -- A list of Walker objects with randomly initialized positions.
        """
            
        # Declare new set of walkers
        walkers = []

        # Create walkers
        for _ in range(nbr_of_walkers):

            # Generate random locations
            position = np.random.uniform(-2, 2, self.dims)

            # Create the walker with an identification number
            walker = Walker(id=_, position = position)

            walkers.append(walker)

        return walkers

    def make_positions(self):
        """A function to extract the position array of all Walker objects attached to the object.
        
        Returns:
            list -- A list of numpy.array with the positions of each walker.
        """

        pos = np.zeros((self.nbr_of_walkers, self.dims))

        # Extract all walker positions as a numpy array
        for walker, i in zip(self.walkers, range(self.nbr_of_walkers)):

            pos[i] = walker.position

        return pos

    def make_distances(self):
        """A function to calculate the Walker-wise distance to the origin.
        
        Returns:
            numpy.array -- A numpy array with the Walker-wise distance to the origin.
        """

        return np.linalg.norm(self.positions, ord=2, axis=1)

    def get_nbr_of_electrons(self):
        """Gets the number of electrons of the Atom object, either 1 (Hydrogen)
        or 2 (Helium).
        
        Raises:
            Exception: If the element is not hydrogen or helium, it is not supported.
        
        Returns:
            int -- The number of electrons of the element.
        """

        if self.element is ("Hydrogen" or "H"):
            return 1
        elif self.element is ("Helium" or "He"):
            return 2
        else:
            raise Exception("Element not supported. Use Hydrogen or Helium.")

    def make_potential(self):
        """A function to calculate the Walker-wise energy potential. The potential
        is a harmonic oscillator with spring constant K = 1.
        
        Returns:
            numpy.array -- A numpy array with the walker-wise potential energy.
        """

        # Calculate the potential for each walker and electron (a potentially 6D problem)
        K = 1
        potential = 0.5 * K * np.power(self.distances, 2)

        return potential

    def branch_state(self, merits):
        """Updates and branches the list of walkers based on a list of merit values. The 
        merits m decide how many copies are created from each walker, or if it is removed:

        m = 0: The walker is removed.
        m = 1: The walker is preserved.
        m > 1: The walker is preserved and m-1 copies are created.
        
        Arguments:
            merits {list} -- List of ints denoting the merit value of the 
            correspondingly indexed walker.
        """

        # New walkers
        branch_walkers = []

        for i in range(self.nbr_of_walkers):

            # Make m-1 copies of each walker
            nbr_of_copies = merits[i]

            # Append all copies of these walkers
            for copy_id in range(nbr_of_copies):

                # Make a copy
                walker = self.walkers[i].copy()

                # If new walkers are being created
                if copy_id > 0:

                    # Update newest walker id
                    self.max_walker_id += 1
                    walker.id = self.max_walker_id

                branch_walkers.append(walker)

        # Update state
        self.set_walkers(branch_walkers)


    def set_walkers(self, walkers):
        """Sets the list of walkers of the Atom object, as well as nbr_of_walkers,
        positions and distances.
        
        Arguments:
            walkers {list} -- A list of Walker objects to attach to object.
        """

        # Set walkers
        self.walkers = walkers

        # Set number of walkers
        self.nbr_of_walkers = len(walkers)

        # Set walker derived values
        self.positions      = self.make_positions()
        self.distances      = self.make_distances()

    def copy(self):
        """Returns a new Atom object with the same attributes.
        
        Returns:
            Atom -- An Atom object with the same alpha, list of walkers, dims and element.
        """

        return Atom(alpha = self.alpha, 
                    walkers = self.walkers, 
                    dims = self.dims, 
                    element = self.element)


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
