import numpy as np
import matplotlib.pyplot as plt
import random

point_latest = np.array([0.0] * 3)
track_list = []
def Atom_ident(atom_coords):

    var_track = 0

    for i in range(3):
        number_str = f"{atom_coords[i]:.10g}"
            
        if '.' in number_str:
            number_str = number_str.rstrip('0').rstrip('.')
    
        sign_dig_len = len(number_str.replace('.', '').replace('-', ''))
        var_track += sign_dig_len
    
    if var_track == 3: # bei drei Gitteratompunkten 3
        #print("Gitteratom")
        return 1
    elif var_track == 5: # Bei drei fcc 5
        #print("FCC-Atom")
        return 2
    elif var_track == 9: # Bei drei interstetiellen 9
        #print("Interstetielles-Atom")
        return 3
    else:
        print("Uhm...?")
        return 0



moveset_grid = [
        [0.25, 0.25, 0.25],
        [-0.25, -0.25, 0.25],
        [-0.25, 0.25, -0.25],
        [0.25, -0.25, -0.25]
    ]

#point_latest = track_list[-1]
if Atom_ident(point_latest) == 1:
    dim_choice = random.choice(moveset_grid)
    point_latest += np.array(dim_choice)
elif Atom_ident(point_latest) == 2:
    print("we dead")
elif Atom_ident(point_latest) == 3:
    print("we dead")

track_list.append(point_latest)
print(track_list)

exit(1)
def Deca_Comp_DIM(D_Start):
    if D_Start == 0:
        print("Minimaler Wert für Dimensionen ist 1")
        return
    d_comp_list = [i for i in range(D_Start, D_Start + 10)]
    print(d_comp_list)
comp_list_return = [0] * 10
hanspeter = np.arange(0, 1.1, 0.1).tolist()
roundhanspeter = [round(i, 1) for i in hanspeter]
print(roundhanspeter)
print(comp_list_return)
Deca_Comp_DIM(19)

def Rnd_Pol(mean, std_dev, num):

    normal_floats = np.random.normal(mean, std_dev, num)
    normal_integers = np.round(normal_floats).astype(int)
    abs_integers = abs(normal_integers)
    normal_integers_list = abs_integers.tolist()
    print(normal_integers_list)

    return normal_integers_list

mean = 0       # Mean of the distribution
std_dev = 1    # Standard deviation of the distribution
num = 1000    # Number of samples

Rnd_Pol(40, 1.5, 400)