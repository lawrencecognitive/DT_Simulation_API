import numpy as np
from numpy.random import normal
import pickle
import itertools

float_package = pickle.load(open('flotation_model.pickle', 'rb'))
smelt_package = pickle.load(open('smelting_model.pickle', 'rb'))

def max_prod(package, constraints):
    if package == 'float': package = float_package
    elif package == 'smelt': package = smelt_package

    inputs = constraints
    print(constraints)

    gridsearch = create_grid(package, inputs) # create all possible permutations of free variables

    gridsearch_scaled = package['min_max_scaler'].transform(gridsearch)  # Perform pre-processing inputs

    output = package['model'].predict(gridsearch_scaled)  # Run model prediction

    max_index = np.argmax(output)  # find index of maximum output (i.e. highest metal concentration)

    opt_in = package['min_max_scaler'].inverse_transform(gridsearch_scaled)[max_index]  # inverse transform max index
    opt_in = opt_in.tolist()  # convert data type
    opt_out = output[max_index].tolist()  # convert data type

    print(opt_in)
    print(opt_out)

    return [round(i, 2) for i in opt_in], round(opt_out, 2)

def create_grid(package, inputs):
    # This function creates all possible permutations of free-variables. This essentially creates a grid search matrix
    # which will be passed to the model.

    # Find missing / free variables and generate linear space values between min and max bounds
    gridsearch = []
    linspace = []
    for i, v in enumerate(inputs):
        if v is None:
            low_bound = package['safety_thresh']['Inputs'][0][i]
            high_bound = package['safety_thresh']['Inputs'][1][i]
            linspace.append(np.linspace(low_bound, high_bound, num=20))

    # Generate all possible permutations of free variables
    iterations = list(itertools.product(*linspace))

    # Generate grid-search array
    for variation in iterations:
        none_index = 0
        temp = inputs[:]
        for i, v in enumerate(inputs):
            if v is None:
                temp[i] = variation[none_index]
                none_index += 1
        gridsearch.append(temp)

    gridsearch = np.asarray(gridsearch)  # modify data type

    return gridsearch

if __name__ == '__main__':
    constraints = [None, None, 397.5, 9.76, 1.67, 2847.0, 488.7, 281.28, 520.4]  # Float
    constraints = [None, None, 0.21, 5.3, 5, 650, 280]  # Smelt
    opt_in, opt_out = max_prod('smelt', constraints)

