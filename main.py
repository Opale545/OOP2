import pygame


# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Red Ball Game")

# Set up the clock
clock = pygame.time.Clock()

"""
# Set up the red ball
ball_radius = 25
ball_x = 320
ball_y = 400
ball_speed = 5
ball_color = (255, 0, 0)
ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

# Set up the jump variables
jump_height = 100
jump_speed = 10
is_jumping = False
jump_counter = 0
"""

# Set up the gravity variables
gravity = 5
is_falling = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed
    if keys[pygame.K_UP] and not is_jumping and not is_falling:
        is_jumping = True
        is_falling = False

    # Update the red ball
    if is_jumping:
        if jump_counter < jump_height:
            ball_y -= jump_speed
            jump_counter += jump_speed
        else:
            is_jumping = False
            is_falling = True
            jump_counter = 0
    elif is_falling:
        if ball_y < 400:
            ball_y += gravity
        else:
            is_falling = False

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1



    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

    # Draw the screen
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

