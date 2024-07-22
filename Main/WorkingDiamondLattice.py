import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

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
