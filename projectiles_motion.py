import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Define initial parameters
initial_v0 = 40
initial_theta0 = 1.09
initial_sx0 = -0.35
initial_sy0 = 10
initial_g = 10
interv = 2

# Define the position functions
def sx(t, sx0, v0, theta0):
    return sx0 + v0 * np.cos(theta0) * t

def sy(t, sy0, v0, theta0, g):
    return sy0 + v0 * np.sin(theta0) * t - 0.5 * g * t**2

# Define the velocity functions
def vx(v0, theta0):
    return v0 * np.cos(theta0)

def vy(t, v0, theta0, g):
    return v0 * np.sin(theta0) - g * t

# Determine the time of flight t1
def calc_t1(sy0, v0, theta0, g):
    discriminant = (v0 * np.sin(theta0))**2 - 4 * (-0.5 * g) * sy0
    return (-v0 * np.sin(theta0) - np.sqrt(discriminant)) / (2 * (-0.5 * g))

# Create the plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)
line, = ax.plot([], [], 'b-', label='Trajectory')
point, = ax.plot([], [], 'ro')
time_template = 'Time = %.2fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
sx0_line = ax.axvline(x=initial_sx0,lw=1, color='k', linestyle='--', label='$s_{x0}$')
sy0_line = ax.axhline(y=initial_sy0,lw=1, color='k', linestyle='--', label='$s_{y0}$')
x_projection, = ax.plot([], [], 'r--', lw=1, label='X Projection')
y_projection, = ax.plot([], [], 'b--', lw=1, label='Y Projection')

# Set plot limits
ax.set_xlim(-10, 50)
ax.set_ylim(0, 50)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()

# Initialization function for the animation
def init():
    line.set_data([], [])
    point.set_data([], [])
    time_text.set_text('')
    x_projection.set_data([], [])
    y_projection.set_data([], [])
    return line, point, x_projection, y_projection, time_text, sx0_line, sy0_line

# Animation function
def animate(i, t, sx0, sy0, v0, theta0, g):
    x = sx(t, sx0, v0, theta0)
    y = sy(t, sy0, v0, theta0, g)
    line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])
    x_projection.set_data([sx0, x[i]], [y[i], y[i]])
    y_projection.set_data([x[i], x[i]], [sy0, y[i]])
    vx_i = vx(v0, theta0)
    vy_i = vy(t[i], v0, theta0, g)
    time_text.set_text(time_template % (i * t1 / len(t)))
    sx0_line.set_xdata([sx0])
    sy0_line.set_ydata([sy0])
    v = ax.quiver(x[i], y[i], vx_i, vy_i, angles='xy', scale_units='xy', scale=1, color='b', label='v')
    vxi = ax.quiver(x[i], y[i], vx_i, 0, angles='xy', scale_units='xy', scale=1, color='r', label='v')
    vyi = ax.quiver(x[i], y[i], 0, vy_i, angles='xy', scale_units='xy', scale=1, color='g', label='v')
    
    return line, point, v, vxi, vyi, x_projection, y_projection, time_text, sx0_line, sy0_line

# Slider update function
def update(val):
    global t1, t, ani
    v0 = v0_slider.val
    theta0 = theta0_slider.val
    sx0 = sx0_slider.val
    sy0 = sy0_slider.val
    g = g_slider.val
    t1 = calc_t1(sy0, v0, theta0, g)
    t = np.linspace(0, t1, num=500)
    x = sx(t, sx0, v0, theta0)
    y = sy(t, sy0, v0, theta0, g)
    ax.set_xlim(np.min(x) - 10, np.max(x) + 10)
    ax.set_ylim(0, np.max(y) + 10)
    sx0_line.set_xdata([sx0])
    sy0_line.set_ydata([sy0])
    ani.event_source.stop()
    ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=interv,
                                  init_func=init, fargs=(t, sx0, sy0, v0, theta0, g), blit=True)
    ani.event_source.start()

# Create sliders
axcolor = 'lightgoldenrodyellow'
ax_v0 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_theta0 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_sx0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_sy0 = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_g = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)

v0_slider = Slider(ax_v0, 'v0', 1, 100, valinit=initial_v0)
theta0_slider = Slider(ax_theta0, 'theta0', 0, np.pi/2, valinit=initial_theta0)
sx0_slider = Slider(ax_sx0, 'sx0', -10, 10, valinit=initial_sx0)
sy0_slider = Slider(ax_sy0, 'sy0', 0, 50, valinit=initial_sy0)
g_slider = Slider(ax_g, 'g', 1, 20, valinit=initial_g)

v0_slider.on_changed(update)
theta0_slider.on_changed(update)
sx0_slider.on_changed(update)
sy0_slider.on_changed(update)
g_slider.on_changed(update)

# Initial calculation and animation
t1 = calc_t1(initial_sy0, initial_v0, initial_theta0, initial_g)
t = np.linspace(0, t1, num=500)
x = sx(t, initial_sx0, initial_v0, initial_theta0)
y = sy(t, initial_sy0, initial_v0, initial_theta0, initial_g)
ax.set_xlim(np.min(x) - 10, np.max(x) + 10)
ax.set_ylim(0, np.max(y) + 10)
ani = animation.FuncAnimation(fig, animate, frames=len(t), interval=interv,
                              init_func=init, fargs=(t, initial_sx0, initial_sy0, initial_v0, initial_theta0, initial_g), blit=True)

plt.show()
