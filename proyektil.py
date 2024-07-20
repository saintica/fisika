import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define constants
g = 9.81  # acceleration due to gravity (m/s^2)
v0 = 50   # initial velocity (m/s)
angle = 45  # launch angle (degrees)
t_max = 2 * v0 * np.sin(np.radians(angle)) / g  # total time of flight

# Calculate the initial velocity components
v0x = v0 * np.cos(np.radians(angle))
v0y = v0 * np.sin(np.radians(angle))

# Time array
t = np.linspace(0, t_max, num=500)

# Equations of motion
x = v0x * t
y = v0y * t - 0.5 * g * t**2

# Velocity components
vx = v0x
vy = v0y - g * t

# Set up the figure, axis, and plot element for animation
fig, ax = plt.subplots()
ax.set_xlim(0, np.max(x) * 1.1)
ax.set_ylim(0, np.max(y) * 1.1)
ax.set_aspect('equal')

line, = ax.plot([], [],'g-.', lw=1, label='Projectile Path')
point, = ax.plot([], [], 'go')
x_projection, = ax.plot([], [], 'r--', lw=1, label='X Projection')
y_projection, = ax.plot([], [], 'b--', lw=1, label='Y Projection')
scale = 2
velocity_vector = ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy', scale=scale, color='blue', label='Velocity')
acceleration_vector = ax.quiver([0], [0], [0], [0], angles='xy', scale_units='xy', scale=scale, color='red', label='Acceleration')

# Initialization function to plot the background of each frame
def init():
    line.set_data([], [])
    point.set_data([], [])
    x_projection.set_data([], [])
    y_projection.set_data([], [])
    velocity_vector.set_UVC([0], [0])
    acceleration_vector.set_UVC([0], [0])
    return line, point, x_projection, y_projection, velocity_vector, acceleration_vector

# Animation function which updates figure data
def animate(i):
    line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    x_projection.set_data([0, x[i]], [y[i], y[i]])
    y_projection.set_data([x[i], x[i]], [0, y[i]])
    velocity_vector.set_offsets([x[i], y[i]])
    velocity_vector.set_UVC([vx], [vy[i]])
    acceleration_vector.set_offsets([x[i], y[i]])
    acceleration_vector.set_UVC([0], [-g])
    return line, point, x_projection, y_projection, velocity_vector, acceleration_vector

# Call the animator
ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(t), interval=20, blit=True)

# Save the animation as a GIF
ani.save('projectile.gif', writer='pillow', fps=20)

# Display the animation
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion with Projections and Vectors')
plt.grid(True)
plt.legend()
plt.show()
