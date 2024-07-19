import numpy as np
import random
import matplotlib.pyplot as plt

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
    
def SAW_Diamonlattice(pol_length_diamond):
    point_latest_diamond = np.array([0.0] * 3)
    track_list_diamond = []
    track_list_diamond.append(point_latest_diamond[:].tolist()) # Wenn direkt als Listenelement/ohne append -> Error
    track_list_dir_diamond = []
    steps_diamond = 0

    moveset_grid = [
        [0.25, 0.25, 0.25],
        [-0.25, -0.25, 0.25],
        [-0.25, 0.25, -0.25],
        [0.25, -0.25, -0.25]
    ]
    moveset_fcc = [
        [-0.25, -0.25, 0.25],
        [0.25, 0.25, 0.25],
        [0.25, -0.25, -0.25],
        [-0.25, 0.25, -0.25]
    ]
    moveset_inter = [
        [-0.25, -0.25, -0.25],
        [0.25, 0.25, -0.25],
        [0.25, -0.25, 0.25],
        [-0.25, 0.25, 0.25]
    ]

    while True:

        point_latest_diamond = track_list_diamond[-1]
        if Atom_ident(point_latest_diamond) == 1:
            current_moveset = moveset_grid
        elif Atom_ident(point_latest_diamond) == 2:
            current_moveset = moveset_fcc
        elif Atom_ident(point_latest_diamond) == 3:
            current_moveset = moveset_inter
        else:
            print("Wat?")
            return 


        # Verhindern von backtracking
        if len(track_list_dir_diamond) >= 1:
            last_move = np.array(track_list_dir_diamond[-1])
            inverse_last_move = -last_move
            available_moves = [move for move in current_moveset if not np.array_equal(move, inverse_last_move)]
        else:
            available_moves = current_moveset

        if not available_moves:
            break

        dim_choice = random.choice(available_moves)
        track_list_dir_diamond.append(dim_choice[:])
        point_latest_diamond += np.array(dim_choice)
        point_latest_diamond_list = point_latest_diamond.tolist()

        # Walk abbrechen / Walkbreak
        if point_latest_diamond_list not in track_list_diamond:
            track_list_diamond.append(point_latest_diamond_list[:])
        else:
            break
      
        steps_diamond += 1
        # Polymerlänge
        if isinstance(pol_length_diamond, int) and steps_diamond >= pol_length_diamond:
            break
        elif isinstance(pol_length_diamond, str) and pol_length_diamond == "inf":
            continue # Bei 'inf' wird der Walk fortgeführt bis Walkbreak
      
    # Für Experiment mit unterschiedlichen Nucleationsites nicht geeignet
    calced_REE = np.linalg.norm(point_latest_diamond)
    # Bei Poly_Call auskommentieren der prints empfohlen.
    print(track_list_diamond)
    print(f"REE: {calced_REE}")
    imp_length = len(track_list_diamond)
    print(f"Walklänge: {imp_length}")
    print(track_list_dir_diamond)
    return calced_REE, imp_length
    
SAW_Diamonlattice("inf")

def Rnd_Pol(mean, std_dev, num):
    
    normal_floats = np.random.normal(mean, std_dev, num)
    normal_integers = np.round(normal_floats).astype(int)
    abs_integers = abs(normal_integers)
    normal_integers_list = abs_integers.tolist()

    return normal_integers_list

imp_size = 400
polymer_lengths = Rnd_Pol(65, 2.5, imp_size)

def PolyCallSimpleDiamond(pol_length_diamond, itter_diamond: int, dist_diamond: bool):
    ree_list_diamond = []
    length_list_diamond = []
    # Liste für tatsächliche Funktion anpassen
    for i in range(itter_diamond):
        if dist_diamond:
            pol_length_diamond = polymer_lengths[i]
        else:
            pass
        # Funktion callen, Fehler auslassen
        ree, length = SAW_Diamonlattice(pol_length_diamond)
        if ree is not None and length is not None:
            ree_list_diamond.append(ree)
            length_list_diamond.append(length)
    # REE
    mean_ree_diamond = np.mean(ree_list_diamond)
    std_dev_ree_diamond = np.std(ree_list_diamond)
    median_ree_diamond = np.median(ree_list_diamond)
    # Walklänge
    mean_length_diamond = np.mean(length_list_diamond)
    std_dev_length_diamond = np.std(length_list_diamond)
    median_length_diamond = np.median(length_list_diamond)

    print(f"REE - Mittelwert: {mean_ree_diamond}, Standardabweichung: {std_dev_ree_diamond}, Median: {median_ree_diamond}")
    print(f"Walklänge - Mittelwert: {mean_length_diamond}, Standardabweichung: {std_dev_length_diamond}, Median: {median_length_diamond}")

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    axs[0].hist(ree_list_diamond, bins=10, edgecolor='black')
    axs[0].set_xlabel('REE')
    axs[0].set_ylabel('Anzahl')
    axs[1].hist(length_list_diamond, bins=10, edgecolor='black')
    axs[1].set_xlabel('Walklänge')
    axs[1].set_ylabel('Anzahl')

    plt.show()

    return ree_list_diamond, length_list_diamond