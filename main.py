# Import the atom class
from Atom import Atom
from DMC import dmc, get_energy


def main():

    ############## PARAMETERS ###############
    NBR_OF_SIMS         = 1
    INIT_NBR_OF_WALKERS = 10
    ALPHA               = 1e-1
    INIT_TRIAL_ENERGY   = -3
    TIMESTEP            = 1e-3


    ############# INITIALIZATION ############
    
    # Initialize the trial energy used to compute ground state
    trial_energy = INIT_TRIAL_ENERGY

    # Initialize atom of choice
    atom = Atom(alpha = ALPHA, 
                nbr_of_walkers = INIT_NBR_OF_WALKERS,
                element = "Helium")



    for _ in range(NBR_OF_SIMS):
        
        # Save data as written file

        # Perform diffusion Monte Carlo without importance sampling
        trial_state = dmc(state = atom,
                        trial_energy = trial_energy,
                        timestep = TIMESTEP, 
                        importance = False
                        )

        # Calculate the new trial energy for saving





if __name__ == "__main__":
    main()