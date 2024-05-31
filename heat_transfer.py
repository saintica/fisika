import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Ensure the correct backend is used
import matplotlib
matplotlib.use('TkAgg')  # Use 'Agg' for headless environments

# Constants
alpha = 1.172e-5  # Thermal diffusivity of steel (m^2/s)
R = 0.10  # Radius in meters
L = 0.50  # Length of the cylinder in meters
T_center = 1000  # Temperature at the center in °C
T_ends = 25  # Temperature at the ends in °C
dx = 0.005  # Spatial step in meters
dt = 0.1  # Time step in seconds
time_steps = 2000  # Number of time steps for the simulation

# Discretization
nx = int(R / dx) + 1
ny = int(L / dx) + 1
x = np.linspace(0, R, nx)
y = np.linspace(0, L, ny)

# Initial temperature distribution
T = np.full((nx, ny), T_ends)
T[int(nx / 2), :] = T_center  # Middle of the cylinder is kept at 1000°C

# Update temperature function using Runge-Kutta method
def update_temperature(T, alpha, dx, dt):
    T_new = T.copy()
    
    def dTdt(T):
        d2T_dx2 = (np.roll(T, -1, axis=0) - 2 * T + np.roll(T, 1, axis=0)) / dx**2
        d2T_dy2 = (np.roll(T, -1, axis=1) - 2 * T + np.roll(T, 1, axis=1)) / dx**2
        dTdt = alpha * (d2T_dx2 + d2T_dy2)
        return dTdt
    
    k1 = dTdt(T)
    k2 = dTdt(T + 0.5 * dt * k1)
    k3 = dTdt(T + 0.5 * dt * k2)
    k4 = dTdt(T + dt * k3)
    
    T_new = T_new + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)
    
    # Enforce boundary conditions (middle stays at 1000°C)
    T_new[int(nx / 2), :] = T_center
    
    return T_new

# Set up the figure and axis
fig, ax = plt.subplots()
cax = ax.imshow(T, cmap='hot', interpolation='nearest', origin='lower', extent=[0, R, 0, L])
fig.colorbar(cax, ax=ax, label='Temperature (°C)')
ax.set_title('Heat Transfer in a Steel Cylinder')
ax.set_xlabel('Radius (m)')
ax.set_ylabel('Length (m)')

# Animation update function
def animate(frame):
    global T
    T = update_temperature(T, alpha, dx, dt)
    cax.set_array(T)
    return [cax]

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=time_steps, interval=20, blit=True)

ani.save(filename="heat_transfer.gif", writer='pillow', fps=60)
# Show the animation
plt.show()
