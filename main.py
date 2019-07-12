# Import the atom class
from Atom import Atom
from DMC import dmc, get_energy, print_walkers_to_file

def main():

    ############## PARAMETERS ###############
    NBR_OF_SIMS         = 5000
    INIT_NBR_OF_WALKERS = 400
    ALPHA               = 1e-1
    NBR_OF_DIMENSIONS   = 3
    INIT_TRIAL_ENERGY   = NBR_OF_DIMENSIONS*0.5-0.2#-3
    TIMESTEP            = 1e-3
    SAVE_WALKERS        = True

    ############# INITIALIZATION ############
    # Initialize the trial energy used to compute ground state
    trial_energy = INIT_TRIAL_ENERGY
    mean_trial   = trial_energy
    time         = 0

    # Initialize atom of choice
    state = Atom(alpha = ALPHA,
                nbr_of_walkers = INIT_NBR_OF_WALKERS,
                dims = NBR_OF_DIMENSIONS,
                element = "Hydrogen")

    with open('results.data', mode="w+") as f:
        with open('walkers.data', mode="w+") as w:

            print("Simulation started.")
            ################## START SIMULATION ##################
            for sim in range(NBR_OF_SIMS):

                # Save data as written file
                f.write("%d\t%d\t%f\t%f\n" % (sim, state.nbr_of_walkers, trial_energy, mean_trial))

                # Print walkers
                if SAVE_WALKERS:
                    print_walkers_to_file(state.walkers, time, w)

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
                time += TIMESTEP

                if not (sim % 1000):
                    print("Iteration %d/%d" % (sim, NBR_OF_SIMS))
                    print("E = %f" % mean_trial)

    f.close()
    w.close()
    print("#####################")
    print("Simulation complete.")
    print("E = %f" % mean_trial)
    print("#####################")



if __name__ == "__main__":
    main()
