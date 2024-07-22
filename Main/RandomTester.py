import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import math


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
            return None, None, None


        # Verhindern von backtracking
        if len(track_list_dir_diamond) >= 1:
            last_move = np.array(track_list_dir_diamond[-1])
            inverse_last_move = -last_move
            available_moves = [move for move in current_moveset if not np.array_equal(move, inverse_last_move)]
        else:
            available_moves = current_moveset

        #if not available_moves:
         #   break

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
    #print(track_list_diamond)
    #print(f"REE: {calced_REE}")
    imp_length = len(track_list_diamond)
    #print(f"Walklänge: {imp_length}")
    #print(track_list_dir_diamond)
    return calced_REE, imp_length, track_list_diamond

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
        ree, length, track_list_diamond = SAW_Diamonlattice(pol_length_diamond)
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

def Flory_Diamond(pol_length_diamond, itter_diamond: int, dist_diamond: bool):
    ree_list_diamond, length_list_diamond = PolyCallSimpleDiamond(pol_length_diamond, itter_diamond, dist_diamond)
    mean_ree_diamond = np.mean(ree_list_diamond)
    median_ree_diamond = np.median(ree_list_diamond)
    mean_length_diamond = np.mean(length_list_diamond)
    median_length_diamond = np.median(length_list_diamond)
    log_flory_1_Diamond = math.log(mean_ree_diamond) / math.log(mean_length_diamond)
    log_flory_2_Diamond = math.log(median_ree_diamond) / math.log(median_length_diamond)
    print(f"Mittlerer Exponent: {log_flory_1_Diamond}, Medianexponent: {log_flory_2_Diamond}")

Flory_Diamond("inf", 1000, False)

exit(1)

def SAW_D_dim(D, pol_length, lin_stiff):
    # Listen initiieren
    point_latest = [0] * D
    track_list = []
    track_list.append(point_latest[:]) # Wenn direkt als Listenelement/ohne append -> Error
    track_list_dim = []
    track_list_dir = []
    steps = 0

            # Verhindern von unendlichen Walks bei ungünstigen Eingaben oder Schleifenfehlern
######--------------------------------------------------------------------------------------------------######
    # Prüfen ob die Polymerlänge valid ist
    if not (isinstance(pol_length, int) or (isinstance(pol_length, str) and pol_length == "inf")):
        print("Kein valider Input für Polymerlänge")
        # raise ValueError("Kein valider Input für Polymerlänge") # statt print und return
        return None, None, None
    # Bei Unendlichem Walk in einer Dimension (ergo einer Richtung) Fehler werfen
    if D == 1 and (isinstance(pol_length, str) and pol_length == "inf"):
        print("Obacht!")
        # raise ValueError("Obacht!") # statt print und return
        return None, None, None
    # Bei unendlichem Walk und 100% Stiffness
    if lin_stiff == 1 and not pol_length != "inf":
        print("REE = inf")
        # raise ValueError("Wieso?") # statt print und return
        return None, None, None
    # Bei 1 Dimension und 0% Stiffness
    if D == 1 and lin_stiff == 0:
        print("Geht net")
        # raise ValueError("Geht net") # statt print und return
        return None, None, None
    
######--------------------------------------------------------------------------------------------------######

    # Walken
    while True:

        if lin_stiff == "None":
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

        else:
            y_n = round(random.random(), 2)
            # Bei 0.01-0.99
            if steps > 0 and y_n < lin_stiff:
                # Walk geht in gleicher Richtung weiter
                rand_dim = track_list_dim[-1]
                part_rand_dir = track_list_dir[-1]
            else:
                # Geht nicht geradeaus weiter
                rand_dim = random.randint(0, D-1)
    
                # Bei 0.00
                if lin_stiff == 0 and steps > 0:
                    # Neue Wahl ohne letzte Dimension
                    available_dims = [dim for dim in range(D) if dim != track_list_dim[-1]]
                    rand_dim = random.choice(available_dims)
                else:
                    rand_dim = random.randint(0, D-1)
                
                if len(track_list_dim) > 0 and rand_dim == track_list_dim[-1]:
                    part_rand_dir = track_list_dir[-1] # Doch keine random direction
                else:
                    part_rand_dir = random.choice([-1, 1]) # hier aber random direction
    
            track_list_dim.append(rand_dim)
            track_list_dir.append(part_rand_dir)
            point_latest[rand_dim] += part_rand_dir

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
    #print(track_list)
    #print(f"REE: {calced_REE}")
    imp_length = len(track_list)
    #print(f"Walklänge: {imp_length}")
    #print(track_list_dir)
    #print(track_list_dim)
    return calced_REE, imp_length, track_list

def Rnd_Pol(mean, std_dev, num):
    
    normal_floats = np.random.normal(mean, std_dev, num)
    normal_integers = np.round(normal_floats).astype(int)
    abs_integers = abs(normal_integers)
    normal_integers_list = abs_integers.tolist()

    return normal_integers_list

imp_size = 400
polymer_lengths = Rnd_Pol(65, 2.5, imp_size)

def PolyCallSimple(D: int, pol_length, lin_stiff: float, itter: int, dist: bool):
    ree_list = []
    length_list = []
    # Liste für tatsächliche Funktion anpassen
    for i in range(itter):
        if dist:
            pol_length = polymer_lengths[i]
        else:
            pass
        # Funktion callen, Fehler auslassen
        ree, length, track_list = SAW_D_dim(D, pol_length, lin_stiff)
        if ree is not None and length is not None:
            ree_list.append(ree)
            length_list.append(length)
    # REE
    mean_ree = np.mean(ree_list)
    std_dev_ree = np.std(ree_list)
    median_ree = np.median(ree_list)
    # Walklänge
    mean_length = np.mean(length_list)
    std_dev_length = np.std(length_list)
    median_length = np.median(length_list)

    # Für Comps auskommentieren
    #print(f"REE - Mittelwert: {mean_ree}, Standardabweichung: {std_dev_ree}, Median: {median_ree}")
    #print(f"Walklänge - Mittelwert: {mean_length}, Standardabweichung: {std_dev_length}, Median: {median_length}")

    # Für Comps auskommentieren
    #fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    #axs[0].hist(ree_list, bins=10, edgecolor='black')
    #axs[0].set_xlabel('REE')
    #axs[0].set_ylabel('Anzahl')
    #axs[1].hist(length_list, bins=10, edgecolor='black')
    #axs[1].set_xlabel('Walklänge')
    #axs[1].set_ylabel('Anzahl')

    #plt.show()

    return ree_list, length_list


#PolyCallSimple(3, "inf", "None", 1000, False)

def Flory_D_DIM(D: int, pol_length, lin_stiff: float, itter: int, dist: bool):
    ree_list, length_list = PolyCallSimple(D, pol_length, lin_stiff, itter, dist)
    mean_ree = np.mean(ree_list)
    median_ree = np.median(ree_list)
    mean_length = np.mean(length_list)
    median_length = np.median(length_list)
    log_flory_1_D = math.log(mean_ree) / math.log(mean_length)
    log_flory_2_D = math.log(median_ree) / math.log(median_length)
    print(f"Mittlerer Exponent: {log_flory_1_D}, Medianexponent: {log_flory_2_D}")

Flory_D_DIM(20, "inf", 0.01, 100, False)



# Define the FCC lattice vectors
a1 = np.array([0.5, 0.5, 0])
a2 = np.array([0.5, 0, 0.5])
a3 = np.array([0, 0.5, 0.5])
basis = np.array([[0, 0, 0], [0.25, 0.25, 0.25]])

def generate_diamond_lattice(n):
    points = []
    for i in range(-n, n+1):
        for j in range(-n, n+1):
            for k in range(-n, n+1):
                for b in basis:
                    point = i*a1 + j*a2 + k*a3 + b
                    points.append(point)
    return np.array(points)

def plot_diamond_lattice(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot lattice points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=20, c='b', marker='o')

    # Connect each point to its 4 nearest neighbors
    for point in points:
        distances = np.linalg.norm(points - point, axis=1)
        nearest_indices = np.argsort(distances)[1:5]  # Skip the first one because it's the point itself
        for idx in nearest_indices:
            ax.plot([point[0], points[idx][0]], [point[1], points[idx][1]], [point[2], points[idx][2]], 'k-', lw=0.5)

    plt.show()

# Parameters
n = 1  # Size of the lattice (increase for more points)

# Generate and plot the lattice
points = generate_diamond_lattice(n)
plot_diamond_lattice(points)

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
            return None, None, None


        # Verhindern von backtracking
        if len(track_list_dir_diamond) >= 1:
            last_move = np.array(track_list_dir_diamond[-1])
            inverse_last_move = -last_move
            available_moves = [move for move in current_moveset if not np.array_equal(move, inverse_last_move)]
        else:
            available_moves = current_moveset

        #if not available_moves:
         #   break

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
    #print(track_list_diamond)
    #print(f"REE: {calced_REE}")
    imp_length = len(track_list_diamond)
    #print(f"Walklänge: {imp_length}")
    #print(track_list_dir_diamond)
    return calced_REE, imp_length, track_list_diamond

def update_graph(num, data, line):
    # update the data
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])
    return line,

def Visualize_Diamondlattice_Walk_3D(pol_length_diamond):
    calced_REE, imp_length, track_list = SAW_Diamonlattice(pol_length_diamond)
    
    data = np.array(track_list).T  # Transpose to separate x, y, z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Creating a line which we will update
    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], 'r-')

    # Setting the labels
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    
    # Setting the limits
    ax.set_xlim([0, max(data[0])])
    ax.set_ylim([0, max(data[1])])
    ax.set_zlim([0, max(data[2])])

    # Creating the animation
    ani = FuncAnimation(fig, update_graph, frames=range(1, len(track_list)),
                        fargs=(data, line), blit=False, interval=100)  # interval in ms

    plt.show()

# Example usage of the function
Visualize_Diamondlattice_Walk_3D(20)

Visualize_Diamondlattice_Walk_3D("inf")

def SAW_D_dim(D, pol_length, lin_stiff):
    # Listen initiieren
    point_latest = [0] * D
    track_list = []
    track_list.append(point_latest[:]) # Wenn direkt als Listenelement/ohne append -> Error
    track_list_dim = []
    track_list_dir = []
    steps = 0

            # Verhindern von unendlichen Walks bei ungünstigen Eingaben oder Schleifenfehlern
######--------------------------------------------------------------------------------------------------######
    # Prüfen ob die Polymerlänge valid ist
    if not (isinstance(pol_length, int) or (isinstance(pol_length, str) and pol_length == "inf")):
        print("Kein valider Input für Polymerlänge")
        # raise ValueError("Kein valider Input für Polymerlänge") # statt print und return
        return
    # Bei Unendlichem Walk in einer Dimension (ergo einer Richtung) Fehler werfen
    if D == 1 and (isinstance(pol_length, str) and pol_length == "inf"):
        print("Obacht!")
        # raise ValueError("Obacht!") # statt print und return
        return
    # Bei unendlichem Walk und 100% Stiffness
    if lin_stiff == 1 and not pol_length != "inf":
        print("REE = inf")
        # raise ValueError("Wieso?") # statt print und return
        return
    # Bei 1 Dimension und 0% Stiffness
    if D == 1 and lin_stiff == 0:
        print("Geht net")
        # raise ValueError("Geht net") # statt print und return
        return
######--------------------------------------------------------------------------------------------------######

    # Walken
    while True:

        if lin_stiff == "None":
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

        else:
            y_n = round(random.random(), 2)
            # Bei 0.01-0.99
            if steps > 0 and y_n < lin_stiff:
                # Walk geht in gleicher Richtung weiter
                rand_dim = track_list_dim[-1]
                part_rand_dir = track_list_dir[-1]
            else:
                # Geht nicht geradeaus weiter
                rand_dim = random.randint(0, D-1)
    
                # Bei 0.00
                if lin_stiff == 0 and steps > 0:
                    # Neue Wahl ohne letzte Dimension
                    available_dims = [dim for dim in range(D) if dim != track_list_dim[-1]]
                    rand_dim = random.choice(available_dims)
                else:
                    rand_dim = random.randint(0, D-1)
                
                if len(track_list_dim) > 0 and rand_dim == track_list_dim[-1]:
                    part_rand_dir = track_list_dir[-1] # Doch keine random direction
                else:
                    part_rand_dir = random.choice([-1, 1]) # hier aber random direction
    
            track_list_dim.append(rand_dim)
            track_list_dir.append(part_rand_dir)
            point_latest[rand_dim] += part_rand_dir

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
    #print(f"REE: {calced_REE}")
    imp_length = len(track_list)
    #print(f"Walklänge: {imp_length}")
    #print(track_list_dir)
    #print(track_list_dim)
    return calced_REE, imp_length, track_list

def Visualize_Walk_3D(pol_length_diamond, lin_stiff):
    calced_REE, imp_length, track_list = SAW_D_dim(3, pol_length_diamond, lin_stiff)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_coords = [point[0] for point in track_list]
    y_coords = [point[1] for point in track_list]
    z_coords = [point[2] for point in track_list]

    ax.plot(x_coords, y_coords, z_coords)
    #ax.set_xlim([-2, 2])
    #ax.set_ylim([-2, 2])
    #ax.set_zlim([-2, 2])
    ax.set_xlabel('X-Axe')
    ax.set_ylabel('Y-Axe')
    ax.set_zlabel('Z-Axe')

    plt.show()

def Visualize_Walk_2D(pol_length_diamond, lin_stiff):
    calced_REE, imp_length, track_list = SAW_D_dim(2, pol_length_diamond, lin_stiff)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    x_coords = [point[0] for point in track_list]
    y_coords = [point[1] for point in track_list]
    ax.plot(x_coords, y_coords, marker='o')
    
    #ax.set_xlim([-2, 2])
    #ax.set_ylim([-2, 2])
    ax.set_xlabel('X-Axe')
    ax.set_ylabel('Y-Axe')

    plt.show()
    
Visualize_Walk_2D(500, "None")
#Visualize_Walk_3D(500, "None")

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