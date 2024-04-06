import random

def randomizer() : 
    # Return a random number between 0 and 1
    return random.uniform(0, 1)

def set_seed(seed = 42) : 
    random.seed(seed)

def gather_constraints(list_of_constraints, seed = None, num_constraints = -1, constraint_type = None) :
    '''
    This function randomly selects constraints to add to the list of constraints
    list_of_constraints : list of constraints to choose from
    seed : seed for random number generator, this is for a single run, if you want to run multiple times, you also need to have an external seed via the function set_seed(seed)
    ''' 
    constraints = []
    if seed : # Single run seed for random number generator, multiple runs will require an external seed
        set_seed(seed)
    # Randomly select constraints to add
    if num_constraints == -1 :
        for constraint in list_of_constraints : 
            if randomizer() > 0.5 : 
                if constraint_type : 
                    if constraint_type == constraint.category : 
                        constraints.append(constraint)
    else: 
        if constraint_type : 
            constraints = random.sample([constraint for constraint in list_of_constraints if constraint.category == constraint_type], num_constraints)
    return constraints