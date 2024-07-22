import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
radius = 5.0
num_steps = 1000
dt = 0.04
g = 9.81  # Acceleration due to gravity

class Ball:
    def __init__(self, position, velocity, radius):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radius = radius
        self.positions = [self.position.copy()]
        
    def check_collision(self):
        if np.linalg.norm(self.position) >= self.radius:
            normal = self.position / np.linalg.norm(self.position)
            self.velocity = self.velocity - 2 * np.dot(self.velocity, normal) * normal

    def update(self):
        # Update position
        self.position += self.velocity * dt
        # Update velocity with gravitational acceleration
        self.velocity[1] -= g * dt
        # Check for collisions and update velocity accordingly
        self.check_collision()
        # Store the new position
        self.positions.append(self.position.copy())

# Initialize balls
ball1 = Ball(position=[1.0, 1.0], velocity=[0.1, 0.2], radius=radius)
ball2 = Ball(position=[-2.0, 1.5], velocity=[-0.2, 0.1], radius=radius)
balls = [ball1, ball2]

# Simulation loop
for _ in range(num_steps):
    for ball in balls:
        ball.update()

# Set up the figure and axis
fig, ax = plt.subplots()
circle = plt.Circle((0, 0), radius, color='b', fill=False)
ax.add_artist(circle)
ax.set_aspect('equal', 'box')
ax.set_xlim(-radius-1, radius+1)
ax.set_ylim(-radius-1, radius+1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Balls Bouncing Inside a Circle with Gravity')

# Ball plot objects for different colors
colors = ['ro', 'bo']
balls_plot = [ax.plot([], [], color)[0] for color in colors]

# Initialization function
def init():
    for ball_plot in balls_plot:
        ball_plot.set_data([], [])
    return balls_plot

# Animation function
def animate(i):
    for ball_plot, ball in zip(balls_plot, balls):
        ball_plot.set_data([ball.positions[i][0]], [ball.positions[i][1]])
    return balls_plot

# Create the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=num_steps, interval=20, blit=True)

plt.show()
