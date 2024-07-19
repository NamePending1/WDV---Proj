import numpy as np
import random

def Atom_ident(atom_coords):
    var_track = 0
    for i in range(3):
        number_str = f"{atom_coords[i]:.10g}"
        if '.' in number_str:
            number_str = number_str.rstrip('0').rstrip('.')
        sign_dig_len = len(number_str.replace('.', '').replace('-', ''))
        var_track += sign_dig_len
    if var_track == 3: # bei drei Gitteratompunkten 3
        return 1
    elif var_track == 5: # Bei drei fcc 5
        return 2
    elif var_track == 9: # Bei drei interstetiellen 9
        return 3
    else:
        print("Uhm...?")
        return 0
    
def SAW_Diamonlattice(pol_length_diamond):
    point_latest_diamond = np.array([0.0] * 3)
    track_list_diamond = [point_latest_diamond[:].tolist()]
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

        if point_latest_diamond_list not in track_list_diamond:
            track_list_diamond.append(point_latest_diamond_list)
        else:
            break

        steps_diamond += 1
        if isinstance(pol_length_diamond, int) and steps_diamond >= pol_length_diamond:
            break
        elif isinstance(pol_length_diamond, str) and pol_length_diamond == "inf":
            continue  # Infinite walk until a loop is formed

    calced_REE = np.linalg.norm(point_latest_diamond)
    print(track_list_diamond)
    print(f"REE: {calced_REE}")
    imp_length = len(track_list_diamond)
    print(f"Walk length: {imp_length}")
    print(track_list_dir_diamond)
    return calced_REE, imp_length

# Run the simulation with infinite polymer length
SAW_Diamonlattice("inf")
