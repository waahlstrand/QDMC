# Import the atom class
from Atom import Atom
from DMC import dmc, get_energy

def main():

    ############## PARAMETERS ###############
    NBR_OF_SIMS         = 50000
    INIT_NBR_OF_WALKERS = 400
    ALPHA               = 1e-1
    INIT_TRIAL_ENERGY   = 0.1#-3
    TIMESTEP            = 1e-3
    NBR_OF_DIMENSIONS   = 1

    ############# INITIALIZATION ############
    # Initialize the trial energy used to compute ground state
    trial_energy = INIT_TRIAL_ENERGY
    mean_trial   = trial_energy

    # Initialize atom of choice
    state = Atom(alpha = ALPHA,
                nbr_of_walkers = INIT_NBR_OF_WALKERS,
                dims = NBR_OF_DIMENSIONS,
                element = "Hydrogen")

    with open('walkers.data', mode="w+") as f:
        print("Simulation started.")
        ################## START SIMULATION ##################
        for sim in range(NBR_OF_SIMS):

            # Save data as written file
            f.write("%d\t%d\t%f\t%f\n" % (sim, state.nbr_of_walkers, trial_energy, mean_trial))

            # Perform diffusion Monte Carlo without importance sampling
            state = dmc(state = state,
                        trial_energy = trial_energy,
                        timestep = TIMESTEP, 
                        importance = False
                        )

            # Calculate the new trial energy for saving
            (trial_energy, mean_trial) = get_energy(alpha = ALPHA,
                                                    trial_energy = trial_energy,
                                                    mean_trial = mean_trial,
                                                    iteration = sim,
                                                    init_nbr_of_walkers = INIT_NBR_OF_WALKERS,
                                                    nbr_of_walkers = state.nbr_of_walkers,
                                                    timestep = TIMESTEP)

            if not (sim % 10000):
                print("Iteration %d/%d" % (sim, NBR_OF_SIMS))
                print("E = %f" % mean_trial)

    f.closed
    print("Simulation complete.")



if __name__ == "__main__":
    main()




import numpy as np
import matplotlib.pyplot as plt

main()

data = np.loadtxt("walkers.data")

plt.plot(data[:,1])
plt.plot(data[:,2])
plt.plot(data[:,3])
