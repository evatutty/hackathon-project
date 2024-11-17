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
YELLOW = (255, 255, 0)  # For the equator
POLE_COLOR = (255, 255, 255)  # White for the pole marker

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coriolis Effect Simulator")

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

def get_latitude_positions(num_lines=10):
    """Calculate latitude line positions with perspective effect"""
    positions = []
    for i in range(num_lines):
        # Use inverse cosine function to create perspective effect
        angle = (i / (num_lines - 1)) * math.pi / 2
        distance = RADIUS * math.sin(angle)
        positions.append(int(distance))
    return positions

def create_stars(num_stars=200):
    import random
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, 800)  # Random x position
        y = random.randint(0, 600)  # Random y position
        stars.append((x, y))  # Store the (x, y) coordinates of each star
    return stars

def draw_stars(screen, stars):
    for (x, y) in stars:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

def draw_grid(surface, angle):
    # Draw latitude lines with perspective effect
    latitude_positions = get_latitude_positions()
    for radius in latitude_positions:
        # Draw equator (first latitude line) thicker and in yellow
        if radius == latitude_positions[0]:  # The equator is the outermost circle
            pygame.draw.circle(surface, YELLOW, CENTER, radius, 100)  # Thicker line for equator
        else:
            pygame.draw.circle(surface, GRAY, CENTER, radius, 1)
    
    # Draw longitude lines with varying spacing
    num_lines = 24  # Increase number of longitude lines
    for i in range(num_lines):
        rot_angle = math.radians(i * (360 / num_lines) + angle)
        end_x = CENTER[0] + RADIUS * math.cos(rot_angle)
        end_y = CENTER[1] + RADIUS * math.sin(rot_angle)
        pygame.draw.line(surface, GRAY, CENTER, (end_x, end_y), 1)
  # Set up the fonts with different sizes
    equator_font = pygame.font.Font(None, 50)  # Font size 74 for Equator
    south_pole_font = pygame.font.Font(None, 20)  # Font size 48 for South Pole

# Render the text for "Equator"
    equator_text = equator_font.render('Equator', True, (255, 0, 0))  # White text color
    equator_rect = equator_text.get_rect(center=(600, 700))  # Position Equator text at (400, 200)

# Render the text for "South Pole"
    south_pole_text = south_pole_font.render('South Pole', True, (255, 255, 255))  # White text color
    south_pole_rect = south_pole_text.get_rect(center=(400, 390))  # Position South Pole text at (400, 400)

# In your game loop or wherever appropriate, draw the texts
    screen.blit(equator_text, equator_rect)  # Draw Equator text
    screen.blit(south_pole_text, south_pole_rect)

# In your game loop or wherever appropriate, draw the texts
    screen.blit(equator_text, equator_rect)  # Draw Equator text
    screen.blit(south_pole_text, south_pole_rect)  # Draw South Pole text)
    # Draw South Pole marker
    pygame.draw.circle(surface, POLE_COLOR, CENTER, 5)  # White dot for South Pole
    # Add a small black outline to make the pole more visible
    pygame.draw.circle(surface, BLACK, CENTER, 5, 1)

def main():
    clock = pygame.time.Clock()
    rotation_angle = 0
    particle = None
    running = True
    stars = create_stars(num_stars=200)
    
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
        draw_stars(screen, stars)
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
                x=int(particle.x)
                y=int(particle.y)
                #displaying latitude
                font = pygame.font.Font(None,25)
                text=font.render(f'Y Position: {y}',True, WHITE, BLACK)
                textRect=text.get_rect()
                textRect.center=(100,750)
                screen.blit(text,textRect)
                text2=font.render(f'X position: {x}',True, WHITE, BLACK)
                textRect2=text2.get_rect()
                textRect2.center=(100,700)
                screen.blit(text2,textRect2)

                pygame.display.update()


    




        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


