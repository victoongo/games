# Example file showing a circle moving on screen
import pygame
import random

# test
# pygame setup
pygame.init()
window_width = 1280
window_height = 720
paddle_width = 30
paddle_height = 250
paddle_dist_from_wall = 0
ball_radius = 30
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0

player_speed = 1000
randomness = 4
begin_random = (10, 20)

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_velocity = pygame.Vector2(random.choice([-1, 1])*random.randint(begin_random[0], begin_random[1]), \
                               random.choice([-1, 1])*random.randint(begin_random[0], begin_random[1]))
left_paddle_pos = pygame.Vector2(paddle_dist_from_wall, (window_height-paddle_height)/2)
right_paddle_pos = pygame.Vector2(window_width-paddle_dist_from_wall-paddle_width, (window_height-paddle_height)/2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # draw all the objects
    pygame.draw.circle(screen, "red", ball_pos, ball_radius)
    pygame.draw.rect(screen, "blue", (left_paddle_pos.x, left_paddle_pos.y, paddle_width, paddle_height))
    pygame.draw.rect(screen, "blue", (right_paddle_pos.x, right_paddle_pos.y, paddle_width, paddle_height))

    # keybinds
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        left_paddle_pos.y -= player_speed * dt
        if left_paddle_pos.y < 0:
            left_paddle_pos.y = 0
    if keys[pygame.K_a]:
        left_paddle_pos.y += player_speed * dt
        if left_paddle_pos.y > window_height-paddle_height:
            left_paddle_pos.y = window_height-paddle_height
    if keys[pygame.K_o]:
        right_paddle_pos.y -= player_speed * dt
        if right_paddle_pos.y < 0:
            right_paddle_pos.y = 0
    if keys[pygame.K_l]:
        right_paddle_pos.y += player_speed * dt
        if right_paddle_pos.y > window_height-paddle_height:
            right_paddle_pos.y = window_height-paddle_height
    
    # ball movement
    if ball_pos.y - ball_radius < 0:
        ball_velocity.y = -ball_velocity.y
    if ball_pos.y + ball_radius > window_height:
        ball_velocity.y = -ball_velocity.y
    if ball_pos.x - ball_radius < left_paddle_pos.x + paddle_width \
                    and left_paddle_pos.y + paddle_height + ball_radius > ball_pos.y > left_paddle_pos.y - ball_radius:
        ball_velocity.x = -ball_velocity.x #+ random.randint(-randomness, randomness)
        # if ball_velocity >= 25:
        #     ball_velocity -= random.randint(-3, -1)
        # elif ball_velocity <= 10:
        #     ball_velocity += random.randint(1, 3)
        # else:
    if ball_pos.x + ball_radius > right_paddle_pos.x \
                    and right_paddle_pos.y + paddle_height + ball_radius > ball_pos.y > right_paddle_pos.y - ball_radius:
        ball_velocity.x = -ball_velocity.x #+ random.randint(-randomness, randomness)

    ball_pos.x += ball_velocity.x
    ball_pos.y += ball_velocity.y



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()