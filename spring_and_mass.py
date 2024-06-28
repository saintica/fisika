import pygame
import pygame_gui
import math
import collections

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spring-Mass System with Sinusoidal Chart")

# Set up GUI manager
manager = pygame_gui.UIManager((width, height))

# Add sliders for mass and spring constant
mass_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, height - 100), (200, 30)),
    start_value=1.0,
    value_range=(0.1, 10.0),
    manager=manager
)

k_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((300, height - 100), (200, 30)),
    start_value=0.1,
    value_range=(0.01, 1.0),
    manager=manager
)

# Add buttons to start and restart the animation
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((550, height - 100), (100, 30)),
    text='Start',
    manager=manager
)

restart_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((700, height - 100), (100, 30)),
    text='Restart',
    manager=manager
)

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (192, 192, 192)
blue = (0, 0, 255)

# Spring properties
mass = 1.0
spring_length = 200
k = 0.1  # Spring constant
damping = 0.01

# Spring drawing properties
num_coils = 20
coil_width = 10
mass_radius = 20

# Top base properties
base_width = 80
base_height = 20

# Chart properties
chart_width = 400
chart_height = 300
chart_margin = 50
data_points = collections.deque(maxlen=chart_width)

# Font for labels
font = pygame.font.SysFont(None, 24)

# Main loop
running = True
time = 0
mass_dragging = False
initial_displacement = 0
initial_phase = 0
animation_running = False  # Flag to control whether the animation is running

while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == mass_slider:
                mass = mass_slider.get_current_value()
            elif event.ui_element == k_slider:
                k = k_slider.get_current_value()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                animation_running = True
            if event.ui_element == restart_button:
                time = 0
                data_points.clear()
                initial_displacement = 0  # Reset initial displacement
                initial_phase = 0
                animation_running = False  # Stop the animation initially
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mass_pos_x, mass_pos_y = (width // 2 - chart_width // 2, 50 + base_height + spring_length + initial_displacement)
            if math.sqrt((mouse_x - mass_pos_x)**2 + (mouse_y - mass_pos_y)**2) <= mass_radius:
                mass_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if mass_dragging:
                initial_displacement = event.pos[1] - (50 + base_height + spring_length)
                initial_phase = math.acos(initial_displacement / initial_displacement) if initial_displacement != 0 else 0
                time = 0  # Reset time to start the new oscillation from the initial position
                mass_dragging = False
        if event.type == pygame.MOUSEMOTION and mass_dragging:
            initial_displacement = event.pos[1] - (50 + base_height + spring_length)
            data_points.appendleft(initial_displacement)

        manager.process_events(event)

    # Update GUI manager
    manager.update(time_delta)

    # Clear the screen
    window.fill(black)

    if not mass_dragging and animation_running:
        # Calculate displacement using Hooke's Law (F = -kx) and damping
        omega = math.sqrt(k / mass)
        displacement = initial_displacement * math.exp(-damping * time) * math.cos(omega * time + initial_phase)
        data_points.appendleft(displacement)
    else:
        displacement = initial_displacement

    # Draw top base
    base_top_left = (width // 2 - base_width // 2 - chart_width // 2, 50)
    base_rect = pygame.Rect(base_top_left[0], base_top_left[1], base_width, base_height)
    pygame.draw.rect(window, grey, base_rect)

    # Draw spring
    spring_top = (width // 2 - chart_width // 2, 50 + base_height)
    spring_bottom = (width // 2 - chart_width // 2, 50 + base_height + spring_length + displacement)

    # Calculate spring segments
    segment_length = (spring_bottom[1] - spring_top[1]) / num_coils
    points = []
    for i in range(num_coils + 1):
        x = width // 2 - chart_width // 2 + (coil_width if i % 2 == 0 else -coil_width)
        y = spring_top[1] + i * segment_length
        points.append((x, y))
    points[0] = spring_top  # Ensure start point is correct
    points[-1] = spring_bottom  # Ensure end point is correct

    pygame.draw.lines(window, white, False, points, 2)

    # Draw mass
    mass_pos = (width // 2 - chart_width // 2, 50 + base_height + spring_length + displacement)
    pygame.draw.circle(window, red, mass_pos, mass_radius)

    # Draw chart box
    chart_top_left = (width // 2 + chart_margin, 50)
    chart_rect = pygame.Rect(chart_top_left[0], chart_top_left[1], chart_width, chart_height)
    pygame.draw.rect(window, grey, chart_rect, 1)

    # Draw ticks and labels on the x-axis (time)
    num_ticks_x = 5
    time_per_tick = len(data_points) / num_ticks_x
    for i in range(num_ticks_x):
        x = chart_top_left[0] + i * (chart_width // (num_ticks_x - 1))
        y = chart_top_left[1] + chart_height
        pygame.draw.line(window, white, (x, y), (x, y + 5), 2)
        label = font.render(f'{int(i * time_per_tick)}', True, white)
        window.blit(label, (x - label.get_width() // 2, y + 8))

    # Draw ticks and labels on the y-axis (mass position)
    num_ticks_y = 5
    for i in range(num_ticks_y):
        x = chart_top_left[0]
        y = chart_top_left[1] + i * (chart_height // (num_ticks_y - 1))
        pygame.draw.line(window, white, (x - 5, y), (x, y), 2)
        label = font.render(f'{(num_ticks_y - i - 1) * 2 - 4}', True, white)  # Assuming each tick represents 2 units of displacement
        window.blit(label, (x - label.get_width() - 10, y - label.get_height() // 2))

    # Plot the displacement data inside the chart box
    for i in range(1, len(data_points)):
        pygame.draw.line(
            window, blue,
            (chart_top_left[0] + i - 1, chart_top_left[1] + chart_height // 2 - int(data_points[i - 1])),
            (chart_top_left[0] + i, chart_top_left[1] + chart_height // 2 - int(data_points[i])),
            2
        )

    # Draw dashed line connecting mass to chart
    if len(data_points) > 0:
        line_start = mass_pos
        line_end = (chart_top_left[0], chart_top_left[1] + chart_height // 2 - int(data_points[0]))
        num_dashes = 20
        for i in range(num_dashes):
            start_x = line_start[0] + (line_end[0] - line_start[0]) * i / num_dashes
            start_y = line_start[1] + (line_end[1] - line_start[1]) * i / num_dashes
            end_x = line_start[0] + (line_end[0] - line_start[0]) * (i + 0.5) / num_dashes
            end_y = line_start[1] + (line_end[1] - line_start[1]) * (i + 0.5) / num_dashes
            pygame.draw.line(window, white, (start_x, start_y), (end_x, end_y), 1)

    # Draw GUI elements
    manager.draw_ui(window)

    # Update the display
    pygame.display.flip()

    # Increment time if animation is running and not dragging
    if animation_running and not mass_dragging:
        time += 0.1

# Quit Pygame
pygame.quit()
