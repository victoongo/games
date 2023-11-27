# Example file showing a circle moving on screen
import pygame

# test
# pygame setup
pygame.init()
window_width = 1280
window_height = 720
paddle_width = 30
paddle_height = 250
paddle_dist_from_wall = 50
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 300

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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
    pygame.draw.circle(screen, "red", ball_pos, 30)
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

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()