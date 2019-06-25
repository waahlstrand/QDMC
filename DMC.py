from Atom import Atom
from Electron import Electron
from Walker import Walker
import numpy as np

def dmc(state: Atom, trial_energy, timestep = 1e-3, importance = False):

    # Update position of all walkers with all electrons
    trial_state = make_trial_state(state, timestep)

    # Evaluate the new state in a birth or death process
    state = birth_or_death(trial_state, trial_energy, timestep)
            
    return None


def make_trial_state(state, timestep):

    new_electrons = []
    
    for electron in state.electrons:

        new_walkers = []

        for walker in electron.walkers:
            
            # Calculate new position based on former walker

            # Zero mean Gaussian
            G = np.random.multivariate_normal(0, np.eye(3), walker.position.shape)

            # Calculate new position
            new_position = walker.position * np.sqrt(timestep) * G

            # Create new walker
            new_walker = Walker(id = walker.id,
                                electron = electron.id,
                                position = new_position)

            # Test new walker against previous
            
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


def birth_or_death(state, trial_energy, timestep):
    pass


def get_energy():
    pass