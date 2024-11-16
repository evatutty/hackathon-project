import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Ball settings
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5  # Ball speed in the X direction
ball_dy = 5  # Ball speed in the Y direction

# Paddle settings
paddle_width = 100
paddle_height = 20
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 10

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)

# Clock for frame rate
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys pressed for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball bounce off walls
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_dx = -ball_dx
    if ball_y - ball_radius <= 0:
        ball_dy = -ball_dy

    # Ball bounce off paddle
    if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and paddle_x <= ball_x <= paddle_x + paddle_width:
        ball_dy = -ball_dy
        score += 1

    # Game over if the ball hits the bottom
    if ball_y + ball_radius >= HEIGHT:
        print("Game Over! Your score:", score)
        pygame.quit()
        sys.exit()

    # Fill screen with black
    screen.fill(BLACK)

    # Draw ball and paddle
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)