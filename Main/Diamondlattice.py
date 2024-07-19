import numpy as np
import random

def SAW_Diamonlattice(pol_length):
    point_latest = [0] * 3
    track_list = []
    track_list.append(point_latest[:]) # Wenn direkt als Listenelement/ohne append -> Error
    track_list_dim = []
    track_list_dir = []
    steps = 0
    moveset_grid = [1,2,3,4] # Moveset für Gitteratome
    moveset_fcc = [1,2,3,4] # Moveset für FCC-Atome
    moveset_inter = [1,2,3,4] # Moveset für Interstetielle-Atome

    while True:

        point_latest = track_list[-1]
        if Atom_ident(point_latest) == 1:
            point_latest += random.choice(moveset_grid)
        elif Atom_ident(point_latest) == 2:
            point_latest += random.choice(moveset_fcc)
        elif Atom_ident(point_latest) == 3:
            point_latest += random.choice(moveset_inter)

        track_list.append(point_latest)
        
        rand_int = random.randint(0, D-1)
        track_list_dim.append(rand_int)
      
        # Verhindern von backtracking
        if len(track_list_dim) > 1 and track_list_dim[-1] == track_list_dim[-2]:
            # Wenn die gleiche Dimension wie letztes mal gewählt wurde, muss der walk weiter in die Richtung laufen, da der SAW nicht rückwärts laufen soll -> unendlicher Walk in D1 bei "inf"
            part_rand_dir = track_list_dir[-1] # Doch keine random direction
        else:
            part_rand_dir = random.choice([-1, 1]) # Hier aber random direction
        track_list_dir.append(part_rand_dir)
        point_latest[rand_int] += part_rand_dir
      
        # Walk abbrechen / Walkbreak
        if point_latest not in track_list:
            track_list.append(point_latest[:])
        else:
            break
      
        steps += 1
        # Polymerlänge
        if isinstance(pol_length, int) and steps >= pol_length:
            break
        elif isinstance(pol_length, str) and pol_length == "inf":
            continue # Bei 'inf' wird der Walk fortgeführt bis Walkbreak
      
        # Für Experiment mit unterschiedlichen Nucleationsites nicht geeignet
        calced_REE = np.linalg.norm(point_latest)
        # Bei Poly_Call auskommentieren der prints empfohlen.
        print(track_list)
        print(f"REE: {calced_REE}")
        imp_length = len(track_list)
        print(f"Walklänge: {imp_length}")
        print(track_list_dir)
        print(track_list_dim)
        return calced_REE, imp_length
    
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
    