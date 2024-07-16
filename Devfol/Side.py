import random
import numpy as np
import matplotlib.pyplot as plt

def SAW_D_dim(D, pol_length, lin_stiff):
    point_latest = [0] * D
    track_list = []
    track_list.append(point_latest[:])
    track_list_dim = []
    track_list_dir = []
    steps = 0

    if not (isinstance(pol_length, int) or (isinstance(pol_length, str) and pol_length == "inf")):
        print("Kein valider Input für Polymerlänge")
        return None
    if D == 1 and (isinstance(pol_length, str) and pol_length == "inf"):
        print("Obacht!")
        return None
    if lin_stiff == 1 and not pol_length != "inf":
        print("REE = inf")
        return None
    if D == 1 and lin_stiff == 0:
        print("Geht net")
        return None

    while True:
        if lin_stiff == "None":
            rand_int = random.randint(0, D-1)
            track_list_dim.append(rand_int)
            if len(track_list_dim) > 1 and track_list_dim[-1] == track_list_dim[-2]:
                part_rand_dir = track_list_dir[-1]
            else:
                part_rand_dir = random.choice([-1, 1])
            track_list_dir.append(part_rand_dir)
            point_latest[rand_int] += part_rand_dir
        else:
            y_n = round(random.random(), 2)
            if steps > 0 and y_n < lin_stiff:
                rand_dim = track_list_dim[-1]
                part_rand_dir = track_list_dir[-1]
            else:
                rand_dim = random.randint(0, D-1)
                if lin_stiff == 0 and steps > 0:
                    available_dims = [dim for dim in range(D) if dim != track_list_dim[-1]]
                    rand_dim = random.choice(available_dims)
                else:
                    rand_dim = random.randint(0, D-1)
                if len(track_list_dim) > 0 and rand_dim == track_list_dim[-1]:
                    part_rand_dir = track_list_dir[-1]
                else:
                    part_rand_dir = random.choice([-1, 1])
            track_list_dim.append(rand_dim)
            track_list_dir.append(part_rand_dir)
            point_latest[rand_dim] += part_rand_dir

        if point_latest not in track_list:
            track_list.append(point_latest[:])
        else:
            break

        steps += 1
        if isinstance(pol_length, int) and steps >= pol_length:
            break
        elif isinstance(pol_length, str) and pol_length == "inf":
            continue

    calced_REE = np.linalg.norm(point_latest)
    imp_length = len(track_list)
    return calced_REE

def PolyCallSimple(D, pol_length, lin_stiff, itter):
    stat_list = []
    for i in range(itter):
        result = SAW_D_dim(D, pol_length, lin_stiff)
        if result is not None:
            stat_list.append(result)

    # Calculate statistics
    mean_val = np.mean(stat_list)
    std_dev = np.std(stat_list)
    median_val = np.median(stat_list)

    # Print statistics
    print(f"Mean (Mittelwert): {mean_val}")
    print(f"Standard Deviation (Standardabweichung): {std_dev}")
    print(f"Median: {median_val}")

    # Plot histogram
    plt.hist(stat_list, bins=30, edgecolor='black')
    plt.xlabel('REE')
    plt.ylabel('Frequency')
    plt.title('Histogram of REE values')
    plt.show()

# Manuelles Callen der Funktionen
PolyCallSimple(5, 20, "None", 500)
