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
        return
    # Bei Walk in einer Dimension (ergo einer Richtung) Fehler werfen
    if D == 1 and (isinstance(pol_length, str) and pol_length == "inf"):
        print("Obacht!")
        # raise ValueError("Obacht!") # statt print und return
        return
    if lin_stiff == 1 and not pol_length != "inf":
        print("REE = inf")
        # raise ValueError("Wieso?") # statt print und return
        return
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
                    # Exclude the previous dimension
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
    #print(track_list)
    #print(calced_REE)
    imp_length = len(track_list)
    #print(imp_length)
    #print(track_list_dir)
    #print(track_list_dim)
    return calced_REE, imp_length

# Normalverteilte Polymerlängen
def Rnd_Pol(mean, std_dev, num):
    
    normal_floats = np.random.normal(mean, std_dev, num)
    normal_integers = np.round(normal_floats).astype(int)
    abs_integers = abs(normal_integers)
    normal_integers_list = abs_integers.tolist()

    return normal_integers_list

def PolyCallSimple(D, pol_length, lin_stiff, itter):
    ree_list = []
    length_list = []
    for i in range(itter):
        pol_length = polymer_lengths[i]
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
    print(f"REE - Mittelwert: {mean_ree}, Standardabweichung: {std_dev_ree}, Median: {median_ree}")
    print(f"Walklänge - Mittelwert: {mean_length}, Standardabweichung: {std_dev_length}, Median: {median_length}")

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    axs[0].hist(ree_list, bins=10, edgecolor='black')
    axs[0].set_xlabel('REE')
    axs[0].set_ylabel('Anzahl')
    axs[1].hist(length_list, bins=10, edgecolor='black')
    axs[1].set_xlabel('Walklänge')
    axs[1].set_ylabel('Anzahl')

    plt.show()
    

# Manuelles Callen der Funktionen
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

#SAW_D_dim(5, 20, 1) #<------------------------------
# SAW_D_dim(D: int, pol_length: (int, str), lin_stiff: (float, str))
    ## pol_length: "inf" ## lin_stiff: "None"

#////\\\\# #<--------------------
imp_size = 400
polymer_lengths = Rnd_Pol(20, 1.5, imp_size)
# Rnd_Pol(mean: float, std_dev: float, num: int) -> list:
PolyCallSimple(5, polymer_lengths, 0.8, imp_size) 
#\\\\////#

#PolyCallSimple(5, "inf", 0.8, 400) # Argument vier entspricht der Anzahl an Itterationen -> dtype: int, die drei ersten sind identisch zum Einfachen Walk #<------------------------------

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
 #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-


### TODOS

    ### Wichtig

        ##### D-Dimentional Walk
            ### Dimensionsvergleiche und Steifigkeitsverglieche bei sonst gleichen Argumenten
        ##### Diamondlattice walk
            ### 3d Diamantgitter
            ### Plot für Diamantgitter

    ### Wenn Zeit
        ### Animationsplots für erste drei Dimensionen, visualisierung des Walks
            ### Timingvariable für Geschwindigkeit der animationen
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

