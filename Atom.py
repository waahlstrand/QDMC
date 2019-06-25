from Electron import Electron
import numpy as np


class Atom:

    def __init__(self, alpha, nbr_of_walkers = 10, electrons = None, element="Helium"):
        self.element = element
        self.alpha = alpha
        self.nbr_of_electrons = self.get_nbr_of_electrons()
        self.nbr_of_walkers = self.set_nbr_of_walkers(nbr_of_walkers, electrons)
        self.electrons = self.set_electrons(electrons)
        self.potential = []
        self.wavefunction = []
        self.local_energy = []
        self.inter_electron_distances = self.get_inter_electron_distance()

    def set_nbr_of_walkers(self, nbr_of_walkers, electrons = None):

        if electrons:

            return electrons[0].nbr_of_walkers

        else:
            return nbr_of_walkers


    def set_electrons(self, electrons = None):

        if electrons:

            # Add predefined electrons
            return electrons

        else:

            # Initialize new electrons
            electrons = []

            # Create new electrons
            for _ in range(self.nbr_of_electrons):
                
                electron = Electron(nbr_of_walkers=self.nbr_of_walkers, id=_)
                electrons.append(electron)
            
            return electrons


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

    def get_potential(self):
        """

        :return:
        """
        potential_list = np.zeros(self.nbr_of_walkers)
        if self.nbr_of_electrons == 1:
            K = 1
            for electron in self.electrons:
                for walker, i in zip(electron.walkers, range(self.nbr_of_walkers)):
                    pot = 0

                    for pos in walker.position:
                        pot += pos*pos

                    potential_list[i] += 0.5*K*pot

            return potential_list

        elif self.nbr_of_electrons == 2:
            pass

    def get_wavefunction(self):

        if self.nbr_of_electrons == 2:
            first_electron = self.electrons[0]
            second_electron = self.electrons[1]
            inter = self.inter_electron_distances

            wave_list = np.exp(- 2*first_electron.distances
                               - 2*second_electron.distances
                               + np.divide(inter, (2*(1 + self.alpha*inter)))
                               )

            return wave_list

    def get_inter_electron_distance(self):
        """

        :return:
        """
        if self.nbr_of_electrons != 2:
            print(self.nbr_of_electrons)

        electrons = self.electrons
        d_list = []
        d = 0

        for first_walker, second_walker in zip(electrons[0].walkers, electrons[1].walkers):
            for first_pos, second_pos in zip(first_walker.position, second_walker.position):
                d += (first_pos-second_pos)*(first_pos-second_pos)

            d_list.append(np.sqrt(d))

        return np.asarray(d_list)

    def get_force(self):

        force_list = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

        for j in range(self.nbr_of_electrons):
            for i in range(self.nbr_of_walkers):

                electron = self.electrons[j]
                other = self.electrons[0] if j == 1 else self.electrons[1]

                r = electron.walkers[i].position
                r_ = other.walkers[i].position

                r1 = electron.walkers[i].distance if j == 1 else other.walkers[i].distance

                r12 = self.inter_electron_distances[i]

                force_list[j, i] = -4 * r/r1 + 2 * (r-r_)/(r12*(1+self.alpha*r12)*(1+self.alpha*r12))

        return force_list

    def get_force_fast(self):

        force = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

        first = self.electrons[0].positions
        second = self.electrons[1].positions

        r1 = self.electrons[0].distances
        r2 = self.electrons[1].distances

        r12 = self.inter_electron_distances[:, None]

        force[0] = -4 * first/r1 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))
        force[0] = -4 * second/r2 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))

    def get_electrons(self):
        """

        :return:
        """
        electrons = []

        for _ in range(self.nbr_of_electrons):
            electron = Electron(nbr_of_walkers=self.nbr_of_walkers, id=_)
            electrons.append(electron)

        return electrons

    def get_potential(self):
        """

        :return:
        """
        potential_list = np.zeros(self.nbr_of_walkers)
        if self.nbr_of_electrons == 1:
            K = 1
            for electron in self.electrons:
                for walker, i in zip(electron.walkers, range(self.nbr_of_walkers)):
                    pot = 0

                    for pos in walker.position:
                        pot += pos*pos

                    potential_list[i] += 0.5*K*pot

            return potential_list

        elif self.nbr_of_electrons == 2:
            pass

    def get_wavefunction(self):

        if self.nbr_of_electrons == 2:
            first_electron = self.electrons[0]
            second_electron = self.electrons[1]
            inter = self.inter_electron_distances

            wave_list = np.exp(- 2*first_electron.distances
                               - 2*second_electron.distances
                               + np.divide(inter, (2*(1 + self.alpha*inter)))
                               )

            return wave_list

    def get_inter_electron_distance(self):
        """

        :return:
        """
        if self.nbr_of_electrons != 2:
            print(self.nbr_of_electrons)

        electrons = self.electrons
        d_list = []
        d = 0

        for first_walker, second_walker in zip(electrons[0].walkers, electrons[1].walkers):
            for first_pos, second_pos in zip(first_walker.position, second_walker.position):
                d += (first_pos-second_pos)*(first_pos-second_pos)

            d_list.append(np.sqrt(d))

        return np.asarray(d_list)

    def get_force(self):

        force_list = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

        for j in range(self.nbr_of_electrons):
            for i in range(self.nbr_of_walkers):

                electron = self.electrons[j]
                other = self.electrons[0] if j == 1 else self.electrons[1]

                r = electron.walkers[i].position
                r_ = other.walkers[i].position

                r1 = electron.walkers[i].distance if j == 1 else other.walkers[i].distance

                r12 = self.inter_electron_distances[i]

                force_list[j, i] = -4 * r/r1 + 2 * (r-r_)/(r12*(1+self.alpha*r12)*(1+self.alpha*r12))

        return force_list

    def get_force_fast(self):

        force = np.zeros((self.nbr_of_electrons, self.nbr_of_walkers, 3))

        first = self.electrons[0].positions
        second = self.electrons[1].positions

        r1 = self.electrons[0].distances
        r2 = self.electrons[1].distances

        r12 = self.inter_electron_distances[:, None]

        force[0] = -4 * first/r1 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))
        force[0] = -4 * second/r2 + 2 * np.divide((first-second), (r12*(1+self.alpha*r12)*(1+self.alpha*r12)))


