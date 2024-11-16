import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quick Pygame Example")

# Rectangle settings
rect_x, rect_y = WIDTH // 2, HEIGHT // 2
rect_width, rect_height = 50, 50
rect_speed = 5

# Clock for frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move rectangle with arrow keys
    if keys[pygame.K_UP]:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN]:
        rect_y += rect_speed
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed

    # Keep rectangle within screen boundaries
    rect_x = max(0, min(WIDTH - rect_width, rect_x))
    rect_y = max(0, min(HEIGHT - rect_height, rect_y))

    # Drawing
    screen.fill(WHITE)  # Clear screen
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))  # Draw rectangle

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)


