import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

# Parameters
length = 4.0  # Length of the bar (meters)
width = 0.1  # Width of the bar (meters)
weight = 8.0  # Weight of the bar (kg)
theta_initial = np.radians(120)  # Initial angle with the horizontal (60 degrees)
g = 9.81  # Acceleration due to gravity (m/s^2)
mu_static_wall = 0.1
mu_dynamic_wall = 0.05
mu_static_floor = 0.15
mu_dynamic_floor = 0.04
dt = 0.05  # Time step (seconds)
num_frames = 300  # Number of frames for the animation

# Calculate the initial forces
normal_force_wall = weight * g * np.cos(theta_initial)
friction_force_wall = mu_static_wall * normal_force_wall
normal_force_floor = weight * g * np.sin(theta_initial)
friction_force_floor = mu_static_floor * normal_force_floor

# Initialize figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_xlabel('x')
ax.set_ylabel('y')

# Add a rectangle to represent the bar
bar = Rectangle((0, 0), length, width, angle=np.degrees(theta_initial), color='blue')
ax.add_patch(bar)

# Animation initialization function
x_0 = length * np.cos(theta_initial)
y_0 = length * np.sin(theta_initial)

def init():
    bar.set_xy([x_0, y_0])
    bar.angle = np.degrees(theta_initial)
    return bar,

# Animation update function
def update(frame):
    global theta_initial, normal_force_wall, friction_force_wall, normal_force_floor, friction_force_floor

    # Calculate forces at current angle
    t = frame * dt
    theta = theta_initial - (t / (num_frames * dt)) * theta_initial  # Linearly decreasing angle for simplicity

    # Friction force adjustments for dynamic friction if the bar starts sliding
    if friction_force_wall > mu_static_wall * normal_force_wall:
        friction_force_wall = mu_dynamic_wall * normal_force_wall

    if friction_force_floor > mu_static_floor * normal_force_floor:
        friction_force_floor = mu_dynamic_floor * normal_force_floor

    # Calculate new positions based on forces
    normal_force_wall = weight * g * np.cos(theta)
    normal_force_floor = weight * g * np.sin(theta)
    
    x0, y0 = 0, length * np.sin(theta)
    x1, y1 = length * np.cos(theta), 0
    
    bar.set_xy([x1, y1])
    bar.angle = np.degrees(theta)

    return bar,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=10)

# Display the animation
plt.axhline(0, color='black', lw=2)  # Floor line
plt.axvline(0, color='black', lw=2)  # Wall line
plt.show()
