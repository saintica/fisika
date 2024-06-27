import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Balls Simulation")

# Colors
black = (0, 0, 0)

# Ball parameters
num_balls = 10
balls = []

class Ball:
    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.coefficient_of_restitution = 0.9
        self.selected = False

    def update(self):
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Check collisions with walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -self.coefficient_of_restitution
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx *= -self.coefficient_of_restitution

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -self.coefficient_of_restitution
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.vy *= -self.coefficient_of_restitution

        # Check collisions with other balls
        for other in balls:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= self.radius + other.radius:
                    angle = math.atan2(dy, dx)
                    overlap = (self.radius + other.radius) - distance
                    self.x -= overlap * math.cos(angle)
                    self.y -= overlap * math.sin(angle)
                    angle_normal = math.atan2(dy, dx)

                    # Calculate velocities using elastic collision equations
                    self_vx, self_vy = self.vx, self.vy
                    other_vx, other_vy = other.vx, other.vy

                    self.vx = (self_vx * (self.mass - other.mass) + (2 * other.mass * other_vx)) / (self.mass + other.mass)
                    self.vy = (self_vy * (self.mass - other.mass) + (2 * other.mass * other_vy)) / (self.mass + other.mass)

                    other.vx = (other_vx * (other.mass - self.mass) + (2 * self.mass * self_vx)) / (self.mass + other.mass)
                    other.vy = (other_vy * (other.mass - self.mass) + (2 * self.mass * self_vy)) / (self.mass + other.mass)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Create random balls
for _ in range(num_balls):
    x = random.randint(50, width - 50)
    y = random.randint(50, height - 50)
    radius = random.randint(10, 30)
    mass = radius ** 2  # Mass proportional to the square of the radius
    balls.append(Ball(x, y, radius, mass))

# Simulation loop
running = True
selected_ball = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for ball in balls:
                if math.sqrt((mouse_x - ball.x)**2 + (mouse_y - ball.y)**2) <= ball.radius:
                    ball.selected = True
                    selected_ball = ball
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_ball:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_ball.vx = (mouse_x - selected_ball.x) / 5
                selected_ball.vy = (mouse_y - selected_ball.y) / 5
                selected_ball.selected = False
                selected_ball = None

    # Update balls
    for ball in balls:
        ball.update()

    # Draw background
    screen.fill(black)

    # Draw balls
    for ball in balls:
        ball.draw()

    # Update display
    pygame.display.flip()

pygame.quit()
