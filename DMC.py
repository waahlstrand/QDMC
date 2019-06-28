from Atom import Atom
from Electron import Electron
from Walker import Walker
import numpy as np

def dmc(state: Atom, trial_energy, timestep = 1e-3, importance = False):

    # Update position of all walkers with all electrons
    trial_state = make_trial_state(state, timestep)

    # Evaluate the new state in a birth or death process
    merits = birth_or_death(trial_state, state, trial_energy, timestep)

    # Branch state based on the merits
    new_state = branch_state(trial_state, merits)
            
    return new_state


def make_trial_state(state, timestep):

    new_electrons = []
    
    for electron in state.electrons:

        new_walkers = []

        for walker in electron.walkers:
            
            # Calculate new position based on former walker
            new_walker = make_trial_walker(electron, walker, timestep)
            
            # Add new walker to set
            new_walkers.append(new_walker)

        # Create new electrons and add associated walkers
        new_electron = Electron(id = electron.id,
                                walkers = new_walkers)
        
        new_electrons.append(new_electron)

    # Create new trial state to compare with previous
    trial_state = Atom(alpha = state.alpha,
                       electrons = new_electrons,
                       element = state.element)                      

    return trial_state


def birth_or_death(trial_state, state, trial_energy, timestep):

    # Calculate the potential for the walkers in the trial state
    trial_potential = trial_state.get_potential()

    # Calculate the weight probability
    energy = trial_potential - trial_energy
    weight = np.exp(- timestep * energy)

    # Get the merit value
    r = np.random.uniform(0, 1, state.nbr_of_walkers)
    merits = np.floor(weight + r).astype(int).squeeze()

    #print(merits)

    if np.sum(merits) <= 0:
        print("All walkers dead: merits = %d" % np.sum(merits))
        quit()

    return list(merits)


def get_energy(alpha, mean_trial, trial_energy, init_nbr_of_walkers, nbr_of_walkers, iteration, timestep):

    trial_energy = mean_trial + (alpha/timestep) * np.log(init_nbr_of_walkers/nbr_of_walkers)
 
    mean_trial= mean_trial*iteration/(iteration+1) + trial_energy/(iteration+1)

    return (trial_energy, mean_trial)

    

def make_trial_walker(electron, walker, timestep):

    # Zero mean Gaussian
    G = np.random.normal(0, 1, walker.position.shape)

    # Calculate new position
    new_position = walker.position + np.sqrt(timestep) * G

    # Create new walker
    new_walker = Walker(id = walker.id,
                        electron = electron.id,
                        position = new_position)

    return new_walker

def branch_state(state, merits):

    # New electrons
    branch_electrons = []

    for electron in state.electrons:

        # Create new walkers
        branch_walkers = []

        for i in range(state.nbr_of_walkers):

            nbr_of_copies = merits[i]

            #print(merits[i])

            # Append all copies of these walkers
            for _ in range(nbr_of_copies):

                branch_walkers.append(electron.walkers[i])


        # Re-number all walkers
        for walker, i in zip(branch_walkers, range(len(branch_walkers))):
            walker.id = i

        # Create new electrons
        branch_electron = Electron(electron.id, walkers = branch_walkers)

        branch_electrons.append(branch_electron)

    # Create new state
    new_state = Atom(alpha = state.alpha,
                    electrons = branch_electrons,
                    element = state.element)

    return new_state
