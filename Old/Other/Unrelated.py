import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data
x = np.arange(1, 10)  # Example x values
y = np.power(2, x)    # Corresponding y values (2^x)

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b', label='2^x')

# Set logarithmic scale for the x-axis
plt.xscale('log', base=2)

# Add labels and title
plt.xlabel('x')
plt.ylabel('2^x')
plt.title('Plot with Logarithmic x-axis and Linear y-axis')

# Show legend
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
