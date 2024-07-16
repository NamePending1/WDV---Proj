import numpy as np
import matplotlib.pyplot as plt

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