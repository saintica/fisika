import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("1D Wave Simulation")

# Colors
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Wave parameters
n = 200  # Number of points in the grid
c = 1  # Wave speed
dx = 1  # Grid spacing
dt = 0.1  # Time step
damping = 0.99  # Damping factor to prevent infinite oscillations
k = 0.1  # Spring constant (Hooke's law)

# Create the wave grids for each string
num_strings = 6
u = [np.zeros(n) for _ in range(num_strings)]  # Current wave amplitude for each string
u_prev = [np.zeros(n) for _ in range(num_strings)]  # Previous wave amplitude for each string
u_next = [np.zeros(n) for _ in range(num_strings)]  # Next wave amplitude for each string

# Variables to track mouse interaction
mouse_held = False
mouse_pos = (0, 0)

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

    # Get mouse position
    if mouse_held:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        string_index = int(mouse_y / (height / num_strings))
        string_index = max(0, min(num_strings - 1, string_index))  # Clamp to valid range
        mouse_pos = int(mouse_x / (width / n))
        u[string_index][mouse_pos] = (mouse_y - height / 2) / 100  # Scale mouse y to wave amplitude

    # Apply the 1D wave equation with Hooke's law to each string
    for s in range(num_strings):
        for i in range(1, n - 1):
            u_next[s][i] = (2 * u[s][i] - u_prev[s][i] +
                            k * (u[s][i + 1] + u[s][i - 1] - 2 * u[s][i]) +
                            c ** 2 * dt ** 2 / dx ** 2 *
                            (u[s][i + 1] + u[s][i - 1] - 2 * u[s][i]))

        # Apply damping
        u_next[s] *= damping

        # Update the wave grids
        u_prev[s], u[s], u_next[s] = u[s], u_next[s], u_prev[s]

    # Draw the waves
    screen.fill(black)
    for s in range(num_strings):
        color = colors[s]
        y_offset = (s + 1) * (height / (num_strings + 1))
        for i in range(n - 1):
            x1 = int(i * (width / n))
            y1 = int(y_offset + u[s][i] * 100)
            x2 = int((i + 1) * (width / n))
            y2 = int(y_offset + u[s][i + 1] * 100)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

    pygame.display.flip()

pygame.quit()
