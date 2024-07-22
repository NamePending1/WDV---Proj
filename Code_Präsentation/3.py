import random
import numpy as np

# Eingabe unnütz für eigentliches Ausführen des Codes, nur zum testen/troubleshooten da
#####################################################
#####################################################
D = 5
lambda_a = 2 # Bei universellem Skalar sinnlos.
pol_length = 20
#####################################################
#####################################################

def SAW_D_dim(D, pol_length):
    # Listen initiieren
    point_latest = [0] * D
    track_list = []
    track_list.append(point_latest[:]) # Wenn direkt als Listenelement/ohne append -> Error
    track_list_dim = []
    track_list_dir = []
    steps = 0

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
    
    # Walken
    while True:
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
    print(track_list)
    print(calced_REE)
    print(len(track_list))
    #print(track_list_dir)
    #print(track_list_dim)


SAW_D_dim(2, "inf") # Da der Walk nicht zurück kann, ist bei unendlicher Polymerlänge und einer Dimension Obacht zu geben

### TODOS

    ### Wichtig

        ##### D-Dimentional Walk
            ### Lineare Steifigkeit für Walks (Funktionsvariable)
            ### Loops über Funktion für Statistik
                ## Histogramme und Plots für die Statistik
                ## GUI mit html/css siehe BikePlot für Funktionsloop / Klassenloop
                    # Auswahlmöglichkeiten zwischen: Diamantgitter und D-Dimensional sowohl für Loop als auch single
                ## Warscheinlichkeitsverteilte Polymerlängen im Funktionsloop / Klassenloop
        ##### Diamondlattice walk
            ### 3d Diamantgitter
            ### Plot für Diamantgitter

    ### Wenn Bock und Zeit
        ### Animationsplots für erste drei Dimensionen, visualisierung des Walks
        ### Experiment mit Unterschiedlichen Anfangspukten / mehreren "Nukleationspunkten"
        ### Timingvariable für Geschwindigkeit der animationen
    
    ### Fertig
        ### basic SAW
        ### Simple exclusion für backwalking
        ### Inf's und D1 Fehler




    