import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Game settings
ball_radius = 20
gravity = 0.8
friction = 0.9
jump_strength = -15
obstacle_speed = 5
level = 1

# Ball settings
ball_x = screen_width // 2
ball_y = screen_height - ball_radius
ball_speed_x = 0
ball_speed_y = 0

# Platform settings
platform_width = 100
platform_height = 10
platform_x = (screen_width - platform_width) // 2
platform_y = screen_height - 50

# Collectibles settings
collectibles = []
for i in range(5):
    collectibles.append(pygame.Rect(random.randint(0, screen_width-20), random.randint(0, screen_height-200), 20, 20))

# Obstacle settings
obstacles = [pygame.Rect(random.randint(0, screen_width-50), random.randint(100, screen_height-200), 50, 10)]
obstacle_speed = 5

# Score
score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_speed_x = -8
    elif keys[pygame.K_RIGHT]:
        ball_speed_x = 8
    else:
        ball_speed_x = 0

    if keys[pygame.K_SPACE] and ball_y + ball_radius >= platform_y:
        ball_speed_y = jump_strength

    # Apply gravity
    ball_speed_y += gravity
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with screen borders
    if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_width:
        ball_speed_x = -ball_speed_x * friction
    if ball_y + ball_radius > screen_height:
        ball_speed_y = -ball_speed_y * friction
        ball_y = screen_height - ball_radius

    # Collision with platform
    if platform_y < ball_y + ball_radius < platform_y + platform_height and \
            platform_x < ball_x < platform_x + platform_width:
        ball_speed_y = -ball_speed_y * friction

    # Collision with collectibles
    for collectible in collectibles[:]:
        if collectible.colliderect(ball_x - ball_radius, ball_y - ball_radius, ball_radius*2, ball_radius*2):
            collectibles.remove(collectible)
            score += 10

    # Move and check collision with obstacles
    for obstacle in obstacles:
        obstacle.x += obstacle_speed
        if obstacle.x <= 0 or obstacle.x >= screen_width - obstacle.width:
            obstacle_speed = -obstacle_speed

        if obstacle.colliderect(ball_x - ball_radius, ball_y - ball_radius, ball_radius*2, ball_radius*2):
            score -= 5

    # Add new obstacles and increase difficulty at level progression
    if len(collectibles) == 0:
        level += 1
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        gravity *= 1.1
        platform_width = max(50, platform_width - 10)
        for _ in range(level + 2):
            obstacles.append(pygame.Rect(random.randint(0, screen_width-50), random.randint(100, screen_height-200), 50, 10))
        collectibles = []
        for i in range(5 + level):
            collectibles.append(pygame.Rect(random.randint(0, screen_width-20), random.randint(0, screen_height-200), 20, 20))

    # Draw the platform
    pygame.draw.rect(screen, red, [platform_x, platform_y, platform_width, platform_height])

    # Draw the ball
    pygame.draw.circle(screen, black, (int(ball_x), int(ball_y)), ball_radius)

    # Draw collectibles
    for collectible in collectibles:
        pygame.draw.rect(screen, yellow, collectible)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, blue, obstacle)

    # Draw score and level
    score_text = font.render(f'Score: {score}', True, green)
    level_text = font.render(f'Level: {level}', True, green)
    screen.blit(score_text, [10, 10])
    screen.blit(level_text, [10, 50])

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
