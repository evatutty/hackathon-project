import pygame
import math
import sys
import random

# Initialize Pygame
pygame.init()

# Window Settings
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coriolis Effect Simulator")

# Simulation Settings
RADIUS = 300  # Earth radius in pixels
CENTER = (WIDTH // 2, HEIGHT // 2)  # Center of the screen
ROTATION_SPEED = 0.5  # How fast the Earth rotates (degrees per frame)
PARTICLE_SPEED = 2  # Initial particle speed
VELOCITY_CHANGE = 0.2  # How much arrow keys change velocity

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TITLE_COLOR = (200, 40, 10)

def create_stars():
    """Create a list of random star positions"""
    return [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) 
            for _ in range(200)]

def draw_stars(screen, stars):
    """Draw all stars as small white circles"""
    for position in stars:
        pygame.draw.circle(screen, WHITE, position, 2)

class Particle:
    """Represents a particle affected by the Coriolis effect"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, PARTICLE_SPEED]  # [x_speed, y_speed]
        self.trail = []  # Stores previous positions
        
    def update(self, rotation_angle, is_northern_hemisphere):
        # Save current position for trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 100:  # Limit trail length
            self.trail.pop(0)
            
        # Calculate Coriolis effect (direction depends on hemisphere)
        angular_velocity = math.radians(ROTATION_SPEED)
        hemisphere_multiplier = -1 if is_northern_hemisphere else 1
        coriolis_x = 2 * angular_velocity * self.velocity[1] * hemisphere_multiplier
        coriolis_y = -2 * angular_velocity * self.velocity[0] * hemisphere_multiplier
        
        # Update velocity and position
        self.velocity[0] += coriolis_x
        self.velocity[1] += coriolis_y
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Check if particle is outside the Earth
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        return math.sqrt(dx*dx + dy*dy) > RADIUS

    def adjust_velocity(self, dx, dy):
        """Change particle velocity using arrow keys"""
        self.velocity[0] += dx
        self.velocity[1] += dy

def draw_earth_grid(surface, angle, is_northern_hemisphere):
    """Draw the Earth with grid lines, labels, and markers"""
    # Draw main Earth circle
    pygame.draw.circle(surface, BLUE, CENTER, RADIUS)
    
    # Draw latitude circles
    latitudes = [RADIUS, int(RADIUS * 0.8), int(RADIUS * 0.6), 
                int(RADIUS * 0.4), int(RADIUS * 0.2)]
    
    for radius in latitudes:
        color = RED if radius == RADIUS else GRAY  # Equator in red
        thickness = 3 if radius == RADIUS else 1  # Equator thicker
        pygame.draw.circle(surface, color, CENTER, radius, thickness)
    
    # Draw longitude lines
    for i in range(24):  # 24 longitude lines
        angle_rad = math.radians(i * 15 + angle)  # 360/24 = 15 degrees
        end_x = CENTER[0] + RADIUS * math.cos(angle_rad)
        end_y = CENTER[1] + RADIUS * math.sin(angle_rad)
        pygame.draw.line(surface, GRAY, CENTER, (end_x, end_y), 1)
    
    # Draw labels
    title_font = pygame.font.Font(None, 80)
    label_font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 20)
    
    # Draw title based on hemisphere
    hemisphere_text = 'Northern Hemisphere' if is_northern_hemisphere else 'Southern Hemisphere'
    title = title_font.render(hemisphere_text, True, TITLE_COLOR, BLACK)
    screen.blit(title, title.get_rect(center=(400, 50)))
    
    # Draw "Equator" label
    equator = label_font.render('Equator', True, RED)
    screen.blit(equator, equator.get_rect(center=(600, 700)))
    
    # Draw pole label and marker based on hemisphere
    pole_text = 'North Pole' if is_northern_hemisphere else 'South Pole'
    pole = small_font.render(pole_text, True, WHITE)
    screen.blit(pole, pole.get_rect(center=(400, 390)))
    pygame.draw.circle(surface, WHITE, CENTER, 5)  # Pole dot
    pygame.draw.circle(surface, BLACK, CENTER, 5, 1)  # Pole outline

    # Draw toggle instruction
    toggle_font = pygame.font.Font(None, 25)
    toggle_text = toggle_font.render('Press H to toggle hemisphere', True, WHITE, BLACK)
    toggle_rect = toggle_text.get_rect()
    toggle_rect.bottomright = (WIDTH - 20, HEIGHT - 20)
    screen.blit(toggle_text, toggle_rect)

def main():
    clock = pygame.time.Clock()
    stars = create_stars()
    rotation_angle = 0
    particle = None
    running = True
    is_northern_hemisphere = False  # Start with Southern hemisphere
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #2create particle on click
                x, y = pygame.mouse.get_pos()
                dx = x - CENTER[0]
                dy = y - CENTER[1]
                if math.sqrt(dx*dx + dy*dy) <= RADIUS:
                    particle = Particle(x, y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Toggle hemisphere
                    is_northern_hemisphere = not is_northern_hemisphere
                    particle = None  # Reset particle when switching hemispheres
        
        # Handle keyboard input
        if particle:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: particle.adjust_velocity(-VELOCITY_CHANGE, 0)
            if keys[pygame.K_RIGHT]: particle.adjust_velocity(VELOCITY_CHANGE, 0)
            if keys[pygame.K_UP]: particle.adjust_velocity(0, -VELOCITY_CHANGE)
            if keys[pygame.K_DOWN]: particle.adjust_velocity(0, VELOCITY_CHANGE)
        
        # Clear screen and draw background
        screen.fill(BLACK)
        draw_stars(screen, stars)
        
        # Draw Earth and grid
        draw_earth_grid(screen, rotation_angle, is_northern_hemisphere)
        rotation_angle += ROTATION_SPEED
        
        # Update and draw particle
        if particle:
            if particle.update(rotation_angle, is_northern_hemisphere):
                particle = None  # Reset if outside Earth
            else:
                # Draw trail and particle
                if len(particle.trail) > 1:
                    pygame.draw.lines(screen, RED, False, particle.trail, 2)
                pygame.draw.circle(screen, RED, (int(particle.x), int(particle.y)), 5)
<<<<<<< HEAD
                x = int(particle.x)
                y = int(particle.y)
                
                # Displaying coordinates and instructions
                font = pygame.font.Font(None, 25)
                text = font.render(f'Y Position: {y}', True, WHITE, BLACK)
                textRect = text.get_rect()
                textRect.center = (100, 700)
                screen.blit(text, textRect)
                
                text2 = font.render(f'X position: {x}', True, WHITE, BLACK)
                textRect2 = text2.get_rect()
                textRect2.center = (100, 650)
                screen.blit(text2, textRect2)
                
                text3 = font.render('Use arrows to change velocity', True, WHITE, BLACK)
                textRect3 = text3.get_rect()
                textRect3.center = (150, 750)
                screen.blit(text3, textRect3)
=======
                x=int(particle.x)
                y=int(particle.y)
                #displaying latitude
                font = pygame.font.Font(None,25)
                text3=font.render('Use arrows to change velocity',True, WHITE, BLACK)
                textRect3=text3.get_rect()
                textRect3.center=(150,750)
                screen.blit(text3,textRect3)
                
                
                distance =math.sqrt(((particle.x - (WIDTH//2))**2) + ((particle.y - (HEIGHT//2))**2))
                font = pygame.font.Font(None,25)
                text4=font.render(f'Distance from pole: {distance:.2f}', True, WHITE, BLACK)
                textRect4=text4.get_rect()
                textRect4.center=(150,700)
                screen.blit(text4,textRect4)


                pygame.display.update()
            
>>>>>>> b15626cd68e3a66f713a1e5d9fa08f7f0023f7c9
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()