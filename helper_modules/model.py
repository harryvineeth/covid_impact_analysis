from helper_modules.imports import *
from copy import deepcopy

def compute_gaussian(mu_x, mu_y, x, y, var):
    numer = (mu_x-x)**2 + (mu_y-y)**2
    denom = 4*var

    return np.exp(-numer/denom)

# def create_mesh(rows, cols):
#     mesh = np.ndarray(shape=(rows, cols), dtype=tuple)
#     for i in range(rows):
#         for j in range(cols):
#             mesh[i, j] = (i,j)
#     return mesh

def get_gaussian_map(x, y, t, rows, cols, variance, strength, gamma, alpha):

    mask = np.zeros((rows, cols))
    # print(mesh)

    for i in range(rows):
        for j in range(cols):
            mask[i, j] = compute_gaussian(x, y, i, j, variance*alpha**(t-1))
    
    mask *= strength*(gamma**(t-1))

    return mask


def run_model(state_input):
    states_map_location = np.array([["WA","MT","ND","MN","WI","MI","..","NY","VT","NH","ME","..","..",".."],
["OR","ID","WY","SD","IA","IL","IN","OH","PA","NJ","CT","RI","MA",".."],
["CA","NV","UT","CO","NE","KS","MO","KY","WV","VA","MD","DE","..",".."],
["..","AZ","NM","TX","OK","AR","TN","NC","..","..","..","..","..",".."],
["..","..","..","..","LA","MS","AL","GA","FL","SC","..","..","..",".."]])
    # Initialize this as the value to multiply the Gaussian mask with 
    # (proportional to the general scale of cases seen) 
    strength = 0.25
    # strength variation across timesteps (value in range: [0, 1]), change this according to the 
    gamma = 0.8

    # variance decides the spread... decide this based on the visualization
    # variance is increased, according to this scale (alpha > 1)
    variance = 2.0
    alpha = 1.25

    rows = 5
    cols = 14
    cases = pd.read_csv('cleaned/model__saved-data-nov.csv')
    cases_dict = {}
    for i,row in cases.iterrows():
        # print(row)
        cases_dict[row['state_code']] = row['cases']
    cases_dict['..'] = 0
    
    index_to_state = {v: k for k, v in states_to_index.items()}

    location_of_state_in_gmap = states_to_index[state_input]

    list_cases_dict = []

    print(cases_dict, '\n\n')

    T = 6
    for t in range(1,T+1):
        gaussian_map = get_gaussian_map(*location_of_state_in_gmap, t, rows, cols, variance, strength, gamma, alpha)
        next_state_cases = {}
        for i in range(rows):
            for j in range(cols):
                if (i,j) in index_to_state:
                    state = index_to_state[(i,j)]
                else:
                    state = '..'
                next_state_cases[state] = (1 + gaussian_map[i, j]) * cases_dict[state]
        list_cases_dict.append(next_state_cases)
        cases_dict = next_state_cases

    df = pd.DataFrame(list_cases_dict)
    
    return df
