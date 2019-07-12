from Atom import Atom
from Walker import Walker
import numpy as np

def dmc(state: Atom, trial_energy, timestep = 1e-3, importance = False):

    # Make trial displacement of all walkers
    trial_state = make_trial_state(state, timestep)

    # Evaluate the new state in a birth or death process
    merits = birth_or_death(trial_state, state, trial_energy, timestep)

    # Branch state based on the merits
    trial_state.branch_state(merits)
            
    return trial_state


def make_trial_state(state, timestep):

    new_walkers = []
    
    for walker in state.walkers:
            
        # Calculate new position based on former walker
        new_walker = make_trial_walker(walker, timestep)
            
        # Add new walker to set
        new_walkers.append(new_walker)


    # Create new trial state to compare with previous
    trial_state = Atom(alpha = state.alpha,
                       walkers = new_walkers,
                       element = state.element,
                       dims = state.dims) 

    trial_state.max_walker_id = state.max_walker_id

    return trial_state


def birth_or_death(trial_state, state, trial_energy, timestep):

    # Calculate the potential for the walkers in the trial state
    trial_potential = trial_state.make_potential()

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

def make_trial_walker(walker, timestep):

    # Zero mean Gaussian
    G = np.random.normal(0, 1, walker.position.shape)

    # Displace walker by diffusion
    new_position = walker.position + np.sqrt(timestep) * G

    # Create new walker
    new_walker = Walker(id = walker.id,
                        position = new_position,
                        dims = walker.dims)

    return new_walker

def branch_state(state, merits):

    # New walkers
    branch_walkers = []

    for i in range(state.nbr_of_walkers):

        # Make m-1 copies of each walker
        nbr_of_copies = merits[i]

        # Append all copies of these walkers
        for _ in range(nbr_of_copies):

            branch_walkers.append(state.walkers[i])


        # Re-number all walkers
        for walker, i in zip(branch_walkers, range(len(branch_walkers))):
            walker.id = i


    # Create new state
    new_state = Atom(alpha = state.alpha,
                    walkers = branch_walkers,
                    element = state.element,
                    dims = state.dims)

    return new_state

def print_walkers_to_file(walkers, time, file):
    
    for walker in walkers:
        file.write("%d\t%f\t%+.4f\n" % (walker.id, time, walker.position[0]))

    #file.write("\n")