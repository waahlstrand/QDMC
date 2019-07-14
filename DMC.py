from Atom import Atom
from Walker import Walker
import numpy as np

def dmc(state, trial_energy, timestep = 1e-3, importance = False):
    """A function to perform one diffusion step in diffusion Monte Carlo, or DMC.
    
    Arguments:
        state {Atom} -- The previous state of the of the atom simulation.
        trial_energy {double} -- The trial energy to compare with the walker potential.
    
    Keyword Arguments:
        timestep {double} -- Size of the time step of each iteration. (default: {1e-3})
        importance {bool} -- Whether to use importance sampling. (default: {False})
    
    Returns:
        Atom -- An updated reference to the state from diffusion and branching.
    """

    ######## CREATE TRIAL STATE #########
    # Make trial displacement of all walkers
    trial_state = make_trial_state(state, timestep)

    # Evaluate the new state in a birth or death process
    merits = birth_or_death(trial_state, state, trial_energy, timestep)

    ######## UPDATE PREVIOUS STATE #########
    # Set new walkers from the trial state
    state.set_walkers(trial_state.walkers)

    # Branch state based on the merits
    state.branch_state(merits)
            
    return state


def make_trial_state(state, timestep):
    """ Creates a trial state by generating trial walkers from driven diffusion.
    
    Arguments:
        state {Atom} -- An atom state from the previous iteration.
        timestep {double} -- Size of the time step of each iteration.
    
    Returns:
        Atom -- A trial state with updated walker positions from diffusion.
    """

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

    # Update the id of the newest walker, for plotting purposes
    trial_state.max_walker_id = state.max_walker_id

    return trial_state


def birth_or_death(trial_state, state, trial_energy, timestep):
    """The birth or death operation creates a list of merit values for all walkers. 
    The merit m decides how many copies of each walker creates,
        
        m = 0: The walker is removed.
        m = 1: The walker is preserved.
        m > 1: The walker is preserved and m-1 copies are created.
    
    Arguments:
        trial_state {Atom} -- A trial state with updated walker positions
        state {Atom} -- The state from the previous iteration
        trial_energy {double} -- The trial energy to compare with the walker potential.
        timestep {double} -- Size of the time step of each iteration.
    
    Raises:
        Exception: If the merits of all walkers is zero, the simulation dies and 
        the hyperparameters must be adjusted.
    
    Returns:
        list -- A list of merits for all walkers
    """

    # Calculate the potential for the walkers in the trial state
    trial_potential = trial_state.make_potential()

    # Calculate the weight probability
    energy = trial_potential - trial_energy
    weight = np.exp(- timestep * energy)

    # Calculate the merit value
    r = np.random.uniform(0, 1, state.nbr_of_walkers)
    merits = np.floor(weight + r).astype(int).squeeze()

    # On rare occasions and combinations of parameters,
    # all walkers may die. Increase INIT_NBR_OF_WALKERS or
    # decrease ALPHA.
    if np.sum(merits) <= 0:
            raise Exception("All walkers dead: merits = %d" % np.sum(merits))


    return list(merits)


def get_energy(alpha, mean_trial, trial_energy, init_nbr_of_walkers, nbr_of_walkers, iteration, timestep):

    trial_energy = mean_trial + (alpha/timestep) * np.log(init_nbr_of_walkers/nbr_of_walkers)
 
    mean_trial= mean_trial*iteration/(iteration+1) + trial_energy/(iteration+1)

    return (trial_energy, mean_trial)

def make_trial_walker(walker, timestep):
    """Function which given a walker returns a trial walker with displaced
    position by means of self-diffusion.
    
    Arguments:
        walker {Walker} -- A Walker object with a position attribute
        timestep {double} -- Size of the time step of each iteration.
    
    Returns:
        Walker -- A displaced walker from self-diffusion.
    """

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
    """Function to print 1D walkers to a file, along with the current iteration.
    
    Arguments:
        walkers {list} -- List of Walker objects
        time {integer} -- Time or iteration of Walker objects
        file {File} -- A file reference for printing.
    """
    
    # Print walker id, time of position, position.
    for walker in walkers:
        file.write("%d\t%f\t%+.4f\n" % (walker.id, time, walker.position[0]))