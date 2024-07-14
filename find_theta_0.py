#Projectile motion
import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox

# Define the function y(theta)
def y(theta, v0, g, y0):
    if y0 == 0:
        term1 = (v0**2 / g) * np.cos(2 * theta)
        term2 = (v0 * np.sin(theta) * np.sqrt(v0**2 * np.sin(theta)**2)) / g
        term3 = (v0**3 * np.cos(theta) * np.sin(2 * theta)) / (2 * g * np.sqrt(v0**2 * np.sin(theta)**2))
    else:
        term1 = (v0**2 / g) * np.cos(2 * theta)
        term2 = (v0 / g) * np.sin(theta) * np.sqrt(v0**2 * np.sin(theta)**2 + 2 * g * y0)
        term3 = (v0**3 * np.cos(theta) * np.sin(2 * theta)) / (2 * g * np.sqrt(v0**2 * (np.sin(theta))**2 + 2 * g * y0))
    return term1 - term2 + term3

# Function to find the root and update the label
def update_root(val):
    v0 = slider_v0.val
    g = slider_g.val
    y0 = slider_y0.val
    theta_min = 0
    theta_max = np.pi / 2
    sol = root_scalar(y, args=(v0, g, y0), bracket=[theta_min, theta_max])
    if sol.converged:
        root_label.set_text(f"The root theta is: {sol.root:.4f} radians")
    else:
        root_label.set_text("Root finding did not converge")
    plt.draw()

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)

# Create the labels
root_label = plt.text(0.5, 0.8, '', transform=plt.gcf().transFigure, horizontalalignment='center', fontsize=12)

# Define sliders
axcolor = 'lightgoldenrodyellow'
ax_v0 = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_g = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_y0 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

slider_v0 = Slider(ax_v0, 'v0', 1, 50, valinit=10, valstep=0.1)
slider_g = Slider(ax_g, 'g', 1, 20, valinit=9.81, valstep=0.1)
slider_y0 = Slider(ax_y0, 'y0', 0.001, 100, valinit=5, valstep=0.1)

# Update the root when sliders are changed
slider_v0.on_changed(update_root)
slider_g.on_changed(update_root)
slider_y0.on_changed(update_root)

# Initial calculation
update_root(None)

plt.show()
