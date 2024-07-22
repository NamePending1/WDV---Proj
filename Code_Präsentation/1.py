import random
import numpy as np

# Eingabe unnütz für eigentliches Ausführen des Codes, nur zum testen/troubleshooten da
#####################################################
#####################################################
D = 5
a = 2 # Muss anders gehandelt werden, 2x - 1 läuft nur für a = 1, sowieso sinnlos
pol_length = 20
#####################################################
#####################################################

def SAW_D_dim(D, pol_length):
    # Listen initiieren
    point_latest = [0] * D
    track_list = []
    track_list.append(point_latest[:])
    # Walken
    while pol_length > 0:
        rand_int = random.randint(0, D-1)
        rand_dir = random.randint(0, 1)
        point_latest[rand_int] = point_latest[rand_int] + 2*(rand_dir) - 1
        # Walk abbrechen
        if point_latest not in track_list:
            track_list.append(point_latest[:])
        else:
            break
        pol_length -= 1 # Kann auskommentiert werden für theoretisch unendlich walks
    calced_REE = np.linalg.norm(point_latest)
    print(track_list)
    print(calced_REE)
    print(len(track_list))

SAW_D_dim(5, 20)

### TODOS
 # Simple exclusion für backwalking
 # MAYBE: Plots für erste drei Dimensionen, MAYBEMAYBE: Timingvariable für Geschwindigkeit der plots
 # Lineare Steifigkeit für Walks
 # Loops über Funktion für Statistik
 # Histogramme und Plots für die Statistik
 # GUI mit html/css siehe BikePlot
 # Warscheinlichkeitsverteilte Polymerlängen im Klassenloop
 # 3d Diamantgitter
 # Plot für Diamantgitter