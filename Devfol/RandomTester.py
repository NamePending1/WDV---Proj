import numpy as np
import matplotlib.pyplot as plt

mu = 6
sigma = 2

def gauschs(sigma, mu, x):
    return 500 * (1 / np.sqrt(2 * np.pi * sigma**2) * (np.e ** (-0.5 * (((x - mu)/ sigma) ** 2))))


xval = np.linspace(0, 150, 1000)
yval = gauschs(5, 50, xval)

plt.plot(xval, yval, linestyle='-', color='red')
#plt.ylim(0, 0.11)
#plt.xlim(-100, 100)
plt.show()