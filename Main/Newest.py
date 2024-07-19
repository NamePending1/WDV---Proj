import random
import numpy as np
import matplotlib.pyplot as plt


# Eingabe unnütz für eigentliches Ausführen des Codes, nur zum testen/troubleshooten da
#####################################################
#####################################################
D = 5
lambda_a = 2 # Bei universellem Skalar sinnlos.
lin_stiff = 0 # 0 -> 100% Dimensionswechsel, 0.01-0.99 ->1-99% Gewichtung für Dimensionswechsel, 1 -> Computer sagt nein
pol_length = 20
itter = 50
#####################################################
#####################################################

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
        return None, None
    # Bei Unendlichem Walk in einer Dimension (ergo einer Richtung) Fehler werfen
    if D == 1 and (isinstance(pol_length, str) and pol_length == "inf"):
        print("Obacht!")
        # raise ValueError("Obacht!") # statt print und return
        return None, None
    # Bei unendlichem Walk und 100% Stiffness
    if lin_stiff == 1 and not pol_length != "inf":
        print("REE = inf")
        # raise ValueError("Wieso?") # statt print und return
        return None, None
    # Bei 1 Dimension und 0% Stiffness
    if D == 1 and lin_stiff == 0:
        print("Geht net")
        # raise ValueError("Geht net") # statt print und return
        return None, None
    
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
            return None, None


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
    
# Normalverteilte Polymerlängen
def Rnd_Pol(mean, std_dev, num):
    
    normal_floats = np.random.normal(mean, std_dev, num)
    normal_integers = np.round(normal_floats).astype(int)
    abs_integers = abs(normal_integers)
    normal_integers_list = abs_integers.tolist()

    return normal_integers_list

# Statistik bei festen Werten
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
        ree, length = SAW_D_dim(D, pol_length, lin_stiff)
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

# Vergleich von 10 Walks in unterschiedlichen Dimensionen
def Deca_Comp_DIM(D_Start, pol_length, lin_stiff, itter, dist):
    if D_Start <= 1:
        print("Minimaler Wert für Dimensionen ist 2")
        return
    d_comp_list = [i for i in range(D_Start, D_Start + 10)] # Anzahl an Vergleichen kann angepasst werden, aber subplots müssen gefittet werden
    comp_list_return_ree = []
    comp_list_return_length = []
    for D in d_comp_list:
        ree, length = PolyCallSimple(D, pol_length, lin_stiff, itter, dist)
        comp_list_return_ree.append(ree)
        comp_list_return_length.append(length)
    
    # Plotten der REE Listen
    fig_ree, axs_ree = plt.subplots(2, 5, figsize=(20, 10))
    fig_ree.suptitle("Vergleich REE")
    for i in range(2):
        for j in range(5):
            matrix_index = i * 5 + j
            axs_ree[i, j].hist(comp_list_return_ree[matrix_index], bins=10, edgecolor="black")
            axs_ree[i, j].set_title(f"D = {d_comp_list[matrix_index]}")
            axs_ree[i, j].set_xlabel("REE")
            axs_ree[i, j].set_ylabel("Anzahl")
    plt.tight_layout()
    #plt.show() # Auskommentieren um beide Plots gleichzeitig zu zeigen

    # Plotten der Walklängen-Listen
    fig_length, axs_length = plt.subplots(2, 5, figsize=(20, 10))
    fig_length.suptitle("Vergleich Längen")
    for i in range(2):
        for j in range(5):
            matrix_index = i * 5 + j
            axs_length[i, j].hist(comp_list_return_length[matrix_index], bins=10, edgecolor="black")
            axs_length[i, j].set_title(f"D = {d_comp_list[matrix_index]}")
            axs_length[i, j].set_xlabel("Walklänge")
            axs_length[i, j].set_ylabel("Anzahl")
    plt.tight_layout()
    plt.show()

# Vergleich von 10 Walks in unterschiedlichen Steifen
def Hendeca_Comp_Stiff(D, pol_length, itter, dist):
    temp_stiff_comp_list = np.arange(0, 1, 0.1).tolist()
    stiff_comp_list = [round(i, 1) for i in temp_stiff_comp_list]
    comp_list_return_ree2 = []
    comp_list_return_length2 = []
    for lin_stiff in stiff_comp_list:
        ree, length = PolyCallSimple(D, pol_length, lin_stiff, itter, dist)
        comp_list_return_ree2.append(ree)
        comp_list_return_length2.append(length)
    
    # Plotten der REE Listen
    fig_ree, axs_ree = plt.subplots(2, 5, figsize=(20, 10))
    fig_ree.suptitle("Vergleich REE")
    for i in range(2):
        for j in range(5):
            matrix_index = i * 5 + j
            axs_ree[i, j].hist(comp_list_return_ree2[matrix_index], bins=10, edgecolor="black")
            axs_ree[i, j].set_title(f"lin_stiff = {stiff_comp_list[matrix_index]}")
            axs_ree[i, j].set_xlabel("REE")
            axs_ree[i, j].set_ylabel("Anzahl")
    plt.tight_layout()
    #plt.show() # Auskommentieren um beide Plots gleichzeitig zu zeigen

    # Plotten der Walklängen-Listen
    fig_length, axs_length = plt.subplots(2, 5, figsize=(20, 10))
    fig_length.suptitle("Vergleich Längen")
    for i in range(2):
        for j in range(5):
            matrix_index = i * 5 + j
            axs_length[i, j].hist(comp_list_return_length2[matrix_index], bins=10, edgecolor="black")
            axs_length[i, j].set_title(f"lin_stiff = {stiff_comp_list[matrix_index]}")
            axs_length[i, j].set_xlabel("Walklänge")
            axs_length[i, j].set_ylabel("Anzahl")
    plt.tight_layout()
    plt.show()
    

# Manuelles Callen der Funktionen
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
######
# Ausführen der Codes. !!! Es sollte immer nur eine Funktion gleichzeitig Ausgeführt werden!!!
# Grundsätzlich geht auch mehrfache Ausführung aber ist hauptsächlich aufgrund von Rechenaufwand nicht empfohlen
# True = Ausführen, False = Nicht Ausführen

# Können/sollen auch einzeln ausgeführt werden, prints und plots müssen wieder abkommentiert werden
Einzel_D_DIM = False # Muss für die Multi_Calls auf True sein
Multi_D_DIM = False # Muss für Vergleiche auf True sein

Multi_Vergleich_D_DIM_DIM = False      ## 
Multi_Vergleich_D_DIM_STIFF = False   ## Hier nur eine der zwei ausführen


Einzel_Diamant = True # Gleiches wie oben
Multi_Diamant = True

original_SAW_D_dim = SAW_D_dim
original_PolyCallSimple = PolyCallSimple
original_Deca_Comp_DIM = Deca_Comp_DIM
original_Hendeca_Comp_Stiff = Hendeca_Comp_Stiff
SAW_D_dim = lambda *args, **kwargs: None if not Einzel_D_DIM else original_SAW_D_dim(*args, **kwargs)
PolyCallSimple = lambda *args, **kwargs: None if not Multi_D_DIM else original_PolyCallSimple(*args, **kwargs)
Deca_Comp_DIM = lambda *args, **kwargs: None if not Multi_Vergleich_D_DIM_DIM else original_Deca_Comp_DIM(*args, **kwargs)
Hendeca_Comp_Stiff = lambda *args, **kwargs: None if not Multi_Vergleich_D_DIM_STIFF else original_Hendeca_Comp_Stiff(*args, **kwargs)

original_SAW_Diamonlattice = SAW_Diamonlattice
original_PolyCallSimpleDiamond = PolyCallSimpleDiamond
SAW_Diamonlattice = lambda *args, **kwargs: None if not Einzel_Diamant else original_SAW_Diamonlattice(*args, **kwargs)
PolyCallSimpleDiamond = lambda *args, **kwargs: None if not Multi_Diamant else original_PolyCallSimpleDiamond(*args, **kwargs)

## pol_length: "inf" ## lin_stiff: "None" / polymer_lengths
# pol_length: Unison(int, str)
# lin_stiff: Unison(int, str, List[int])

# Einzel_D_DIM
SAW_D_dim(5, 20, 1) # Bei lin_stiff > 1 passiert das gleiche wie bei lin_stiff == 1
# SAW_D_dim(D: int, pol_length: (int, str), lin_stiff: (float, str))

# Multi_D_DIM
#////\\\\#
imp_size = 400
polymer_lengths = Rnd_Pol(65, 2.5, imp_size)
# Rnd_Pol(mean: float, std_dev: float, num: int) -> list:
# Ex: PolyCallSimple(5, polymer_lengths, 0.8, imp_size, True) 
#\\\\////#
PolyCallSimple(3, "inf", "None", 400, True) # Argument vier entspricht der Anzahl an Itterationen -> dtype: int, Argument 5 fragt ob die maximalen Polymerlängen gleich oder Normalverteilt sein sollen, die drei ersten sind identisch zum Einfachen Walk
# PolyCallSimple(D: int, pol_length, lin_stiff: float, itter: int, dist: bool)

Deca_Comp_DIM(3, "inf", "None", 100, False) # Itterationen werden hier praktisch mit 10 multipliziert
#Deca_Comp_DIM(D_Start: int, pol_length, lin_stiff: float, itter: int, dist: bool)

Hendeca_Comp_Stiff(3, 100, 200, False)
#Hendeca_Comp_Stiff(D: int, pol_length, itter: int, dist: bool)

SAW_Diamonlattice("inf")
#SAW_Diamonlattice(pol_length: Unison(int, str)) # str exception: "inf"

PolyCallSimpleDiamond("inf", 200, False)
# PolyCallSimpleDiamond(pol_length_diamond, itter_diamond: int, dist_diamond: bool):

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

print("Code went through without error") # Bei langsamen Rechnern manchmal sinnvoll um Rechenaufwand "einzuschätzen" (Nach Berechnung können die Plots noch ewig laden -> Nachricht)

### TODOS

    ### Wichtig

        ##### Diamondlattice walk
            ### 3d Diamantgitter
            ### Mehrfaches Ausführen siehe Simple_Poly_Call

    ### Wenn Zeit
        ### Animationsplots für erste drei Dimensionen, visualisierung des Walks
            ### Timingvariable für Geschwindigkeit der animationen
            ### Plot für Diamantgitter

    ### Wenn sehr viel Zeit
        ### Experiment mit Unterschiedlichen Anfangspukten / mehreren "Nukleationspunkten"
        ## GUI mit html/css siehe BikePlot für Funktionsloop
            # Auswahlmöglichkeiten zwischen: Diamantgitter und D-Dimensional sowohl für Loop als auch single
    
    ### Fertig
        ### basic SAW
        ### Simple exclusion für backwalking
        ### Inf's und D1 Fehler
        ### Lineare Steifigkeit für Walks (Funktionsvariable)
        ### Loops über Funktion für Statistik
        ## Histogramme und Plots für die Statistik
        ## Warscheinlichkeitsverteilte Polymerlängen
        ##### D-Dimentional Walk
        ### Dimensionsvergleiche und Steifigkeitsverglieche bei sonst gleichen Argumenten

