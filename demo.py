import pygame
import numpy as np
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Constants
WIDTH, HEIGHT = 800, 800  # Screen dimensions
EARTH_RADIUS = 300  # Earth radius in pixels
EARTH_ROTATION_SPEED = 0.05  # Earth rotation speed in radians per frame
HURRICANE_ROTATION_SPEED = 2  # Hurricane rotation speed in degrees per frame
FPS = 60  # Frames per second
SOUTHERN_HEMISPHERE = "Southern"
NORTHERN_HEMISPHERE = "Northern"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hurricane Simulation")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# User Inputs
hemisphere = input("Enter hemisphere (Northern or Southern): ").strip()
latitude = float(input("Enter latitude in radians (0 to π/2 for N, -π/2 to 0 for S): "))
hurricane_radius = int(input("Enter hurricane radius in kilometers: ")) * 1e3

# Hurricane Initial Position and Velocity
lon = 0  # Longitude in radians
velocity = np.array([0.0, 200.0])  # Initial velocity (latitudinal, longitudinal) in m/s
rotation_angle = 0  # Rotation angle for hurricane texture
path_points = []  # To store the trajectory

# Scaling for visualization
VISUAL_SCALE = EARTH_RADIUS / (6371e3)  # Convert kilometers to pixels
hurricane_radius_pixels = int(hurricane_radius * VISUAL_SCALE)

# Functions
def calculate_coriolis(lat, velocity):
    """Calculate the Coriolis force based on latitude and velocity."""
    coriolis_strength = 2 * 7.2921e-5 * velocity[1] * np.sin(lat)
    return np.array([0, coriolis_strength])


def update_hurricane_position(lat, lon, velocity, coriolis, time_step):
    """Update the hurricane's position based on velocity, Coriolis force, and Earth's rotation."""
    velocity += coriolis * time_step
    d_lat = velocity[0] * time_step / (EARTH_RADIUS / VISUAL_SCALE)
    d_lon = velocity[1] * time_step / (EARTH_RADIUS / VISUAL_SCALE * np.cos(lat))
    lat += d_lat
    lon = (lon + d_lon + EARTH_ROTATION_SPEED * time_step) % (2 * np.pi)
    return lat, lon, velocity


def lat_lon_to_screen(lat, lon):
    """Convert latitude and longitude to screen coordinates."""
    x = WIDTH // 2 + EARTH_RADIUS * np.cos(lat) * np.cos(lon)
    y = HEIGHT // 2 + EARTH_RADIUS * np.cos(lat) * np.sin(lon)
    return int(x), int(y)


# Main Game Loop
running = True
earth_rotation = 0  # Angle of Earth rotation
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Update Earth rotation
    earth_rotation = (earth_rotation + EARTH_ROTATION_SPEED) % (2 * np.pi)

    # Draw Earth
    pygame.draw.circle(screen, BLUE, (WIDTH // 2, HEIGHT // 2), EARTH_RADIUS, 1)

    # Update Hurricane Position
    coriolis = calculate_coriolis(latitude, velocity)
    latitude, lon, velocity = update_hurricane_position(latitude, lon, velocity, coriolis, 1 / FPS)

    # Get Hurricane Screen Coordinates
    hurricane_x, hurricane_y = lat_lon_to_screen(latitude, lon)

    # Draw Hurricane Path
    path_points.append((hurricane_x, hurricane_y))
    if len(path_points) > 1:
        pygame.draw.lines(screen, GREEN, False, path_points, 2)

    # Draw Hurricane
    pygame.draw.circle(screen, RED, (hurricane_x, hurricane_y), hurricane_radius_pixels, 0)

    # Rotate and Draw Hurricane Texture
    rotation_angle += HURRICANE_ROTATION_SPEED if hemisphere == NORTHERN_HEMISPHERE else -HURRICANE_ROTATION_SPEED
    pygame.draw.circle(screen, WHITE, (hurricane_x, hurricane_y), hurricane_radius_pixels // 2, 0)

    # Update Display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
