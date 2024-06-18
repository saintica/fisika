import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox
from scipy.integrate import solve_ivp

# Define initial system parameters
initial_params = {
    "mass": 1.0,
    "spring_constant": 10.0,
    "damping_coefficient": 0.5,
    "initial_position": 1.0,
    "initial_velocity": 0.0,
}

# Function to solve the spring-mass-damper system
def solve_system(params, t_span, t_eval):
    m = params["mass"]
    k = params["spring_constant"]
    c = params["damping_coefficient"]

    def spring_mass_damper(t, y):
        position, velocity = y
        dydt = [velocity, -k/m * position - c/m * velocity]
        return dydt

    y0 = [params["initial_position"], params["initial_velocity"]]
    sol = solve_ivp(spring_mass_damper, t_span, y0, t_eval=t_eval)
    return sol.y[0], sol.y[1]

# Function to draw a coiled spring
def draw_spring(ax, y0, y1, n_coils=20, spring_width=0.1):
    if y1 < y0:
        y1 = y0
    t = np.linspace(0, 2 * np.pi * n_coils, 1000)
    y = np.linspace(y0, y1, t.size)
    x = spring_width * np.sin(t)
    spring_line.set_data(x, y)

# Initialize the figure and axis for the animation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle("Spring-Mass-Damper System")

# Left side: Mass, spring, and damper motion
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.grid()

# Right side: Position vs Time and Velocity vs Time
ax2.set_xlim(0, 10)
ax2.set_ylim(-2, 2)
ax2.grid()
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Position / Velocity')

line_position, = ax2.plot([], [], 'b-', label='Position (m)')
line_velocity, = ax2.plot([], [], 'r-', label='Velocity (m/s)')
ax2.legend()

# Initialize the mass, spring, and damper on the left side
mass, = ax1.plot([], [], 'ks', markersize=15)
spring_line, = ax1.plot([], [], 'k-', lw=2)

# Add TextBoxes for interactive parameter input
axbox_mass = plt.axes([0.1, 0.02, 0.2, 0.05])
text_mass = TextBox(axbox_mass, 'Mass (kg)', initial=str(initial_params["mass"]))

axbox_k = plt.axes([0.4, 0.02, 0.2, 0.05])
text_k = TextBox(axbox_k, 'Spring constant (N/m)', initial=str(initial_params["spring_constant"]))

axbox_c = plt.axes([0.7, 0.02, 0.2, 0.05])
text_c = TextBox(axbox_c, 'Damping coeff. (N·s/m)', initial=str(initial_params["damping_coefficient"]))

# Function to initialize the animation
def init():
    line_position.set_data([], [])
    line_velocity.set_data([], [])
    mass.set_data([], [])
    spring_line.set_data([], [])
    return line_position, line_velocity, mass, spring_line

# Function to update the animation
def update(frame):
    time = t_eval[frame]
    x = position[frame]
    v = velocity[frame]

    # Update the lines for position and velocity
    line_position.set_data(t_eval[:frame], position[:frame])
    line_velocity.set_data(t_eval[:frame], velocity[:frame])

    # Update the mass and spring positions
    mass.set_data([0], [x])
    draw_spring(ax1, 0, x)  # Draw new spring

    return line_position, line_velocity, mass, spring_line

# Function to update parameters and redraw the animation
def update_params(label):
    params["mass"] = float(text_mass.text)
    params["spring_constant"] = float(text_k.text)
    params["damping_coefficient"] = float(text_c.text)
    
    global position, velocity, t_span, t_eval
    position, velocity = solve_system(params, t_span, t_eval)
    
    # Adjust the y-limits for the right plot
    max_position = max(abs(position))
    max_velocity = max(abs(velocity))
    ax2.set_ylim(-max(max_position, max_velocity) * 1.1, max(max_position, max_velocity) * 1.1)
    
    ani.event_source.stop()
    ani.new_frame_seq()
    ani.event_source.start()

# Initialize parameters
params = initial_params.copy()
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 1000)
position, velocity = solve_system(params, t_span, t_eval)

# Create the animation
ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True)

# Connect TextBox events
text_mass.on_submit(update_params)
text_k.on_submit(update_params)
text_c.on_submit(update_params)

plt.tight_layout(rect=[0, 0.1, 1, 0.95])  # Adjust for title and textboxes
plt.show()
