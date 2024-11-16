import pygame
import math
import sys
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 800
RADIUS = 300
CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.5  # degrees per frame
PARTICLE_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Southern Hemisphere Coriolis Effect Simulator")

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initial_x = x - CENTER[0]
        self.initial_y = y - CENTER[1]
        self.angle = 0
        self.trail = []
        self.velocity = [0, PARTICLE_SPEED]  # Initial velocity (moving straight down)
        
    def update(self, rotation_angle):
        # Store current position in trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 100:  # Limit trail length
            self.trail.pop(0)
            
        # Calculate Coriolis effect
        # In Southern Hemisphere, deflection is to the left
        angular_velocity = math.radians(ROTATION_SPEED)
        coriolis_acceleration_x = 2 * angular_velocity * self.velocity[1]
        coriolis_acceleration_y = -2 * angular_velocity * self.velocity[0]
        
        # Update velocity with Coriolis effect
        self.velocity[0] += coriolis_acceleration_x
        self.velocity[1] += coriolis_acceleration_y
        
        # Update position
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Check if particle is outside the circle
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        if math.sqrt(dx*dx + dy*dy) > RADIUS:
            return True
        return False

def draw_grid(surface, angle):
    # Draw latitude lines
    for i in range(30, RADIUS, 60):
        pygame.draw.circle(surface, GRAY, CENTER, i, 1)
    
    # Draw longitude lines
    for i in range(12):
        rot_angle = math.radians(i * 30 + angle)
        end_x = CENTER[0] + RADIUS * math.cos(rot_angle)
        end_y = CENTER[1] + RADIUS * math.sin(rot_angle)
        pygame.draw.line(surface, GRAY, CENTER, (end_x, end_y), 1)

def main():
    clock = pygame.time.Clock()
    rotation_angle = 0
    particle = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create new particle at mouse click position
                x, y = pygame.mouse.get_pos()
                dx = x - CENTER[0]
                dy = y - CENTER[1]
                # Only create particle if click is inside the circle
                if math.sqrt(dx*dx + dy*dy) <= RADIUS:
                    particle = Particle(x, y)
        
        screen.fill(BLACK)
        
        # Draw rotating Earth (Southern Hemisphere)
        pygame.draw.circle(screen, BLUE, CENTER, RADIUS)
        draw_grid(screen, rotation_angle)
        
        # Update rotation
        rotation_angle += ROTATION_SPEED
        
        # Update and draw particle
        if particle:
            if particle.update(rotation_angle):
                particle = None  # Reset particle if it goes outside the circle
            else:
                # Draw trail
                if len(particle.trail) > 1:
                    pygame.draw.lines(screen, RED, False, particle.trail, 2)
                # Draw particle
                pygame.draw.circle(screen, RED, (int(particle.x), int(particle.y)), 5)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()