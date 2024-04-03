# Example file showing a circle moving on screen
import pygame
import random

# variables
player_speed = 1000
window_width = 1280
window_height = 720
paddle_width = 30
paddle_height = 250
paddle_dist_from_wall = 0
ball_radius = 30
ball_speed_variation = (1, 3)
beginning_ball_speed = (10, 15)
ball_color = "red"
paddle_color = "blue"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
bounced = None
game_on = True
points = [0, 0]


ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_velocity = pygame.Vector2(
    random.choice([-1, 1])
    * random.randint(beginning_ball_speed[0], beginning_ball_speed[1]),
    random.choice([-1, 1])
    * random.randint(beginning_ball_speed[0], beginning_ball_speed[1]),
)
left_paddle_pos = pygame.Vector2(
    paddle_dist_from_wall, (window_height - paddle_height) / 2
)
right_paddle_pos = pygame.Vector2(
    window_width - paddle_dist_from_wall - paddle_width,
    (window_height - paddle_height) / 2,
)

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

font = pygame.font.Font("freesansbold.ttf", 32)

# create a text surface object,
# on which text is drawn on it.
text = font.render("GeeksForGeeks", True, green, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# set the center of the rectangular object.
textRect.center = (window_width // 2, window_height // 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    screen.blit(text, textRect)

    # draw all the objects
    pygame.draw.circle(screen, "red", ball_pos, ball_radius)
    pygame.draw.rect(
        screen,
        "blue",
        (left_paddle_pos.x, left_paddle_pos.y, paddle_width, paddle_height),
    )
    pygame.draw.rect(
        screen,
        "blue",
        (right_paddle_pos.x, right_paddle_pos.y, paddle_width, paddle_height),
    )

    # keybinds
    keys = pygame.key.get_pressed()

    if game_on:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw all the objects
        pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
        pygame.draw.rect(
            screen,
            paddle_color,
            (left_paddle_pos.x, left_paddle_pos.y, paddle_width, paddle_height),
        )
        pygame.draw.rect(
            screen,
            paddle_color,
            (right_paddle_pos.x, right_paddle_pos.y, paddle_width, paddle_height),
        )

        # keybinds
        if keys[pygame.K_w]:
            left_paddle_pos.y -= player_speed * dt
            if left_paddle_pos.y < 0:
                left_paddle_pos.y = 0
        if keys[pygame.K_s]:
            left_paddle_pos.y += player_speed * dt
            if left_paddle_pos.y > window_height - paddle_height:
                left_paddle_pos.y = window_height - paddle_height
        if keys[pygame.K_UP]:
            right_paddle_pos.y -= player_speed * dt
            if right_paddle_pos.y < 0:
                right_paddle_pos.y = 0
        if keys[pygame.K_DOWN]:
            right_paddle_pos.y += player_speed * dt
            if right_paddle_pos.y > window_height - paddle_height:
                right_paddle_pos.y = window_height - paddle_height

        # ball movement
        if ball_pos.y - ball_radius < 0:
            ball_velocity.y = -ball_velocity.y
        if ball_pos.y + ball_radius > window_height:
            ball_velocity.y = -ball_velocity.y
        if (
            ball_pos.x - ball_radius < left_paddle_pos.x + paddle_width
            and left_paddle_pos.y + paddle_height + ball_radius
            > ball_pos.y
            > left_paddle_pos.y - ball_radius
        ):
            ball_velocity.x *= -1
            bounced = True
        if (
            ball_pos.x + ball_radius > right_paddle_pos.x
            and right_paddle_pos.y + paddle_height + ball_radius
            > ball_pos.y
            > right_paddle_pos.y - ball_radius
        ):
            ball_velocity.x *= -1
            bounced = True

        # ball movement randomization
        if bounced:
            if ball_velocity.x >= 25:
                ball_velocity.x -= random.randint(
                    ball_speed_variation[0], ball_speed_variation[1]
                )
            elif ball_velocity.x <= 10:
                ball_velocity.x += random.randint(
                    ball_speed_variation[0], ball_speed_variation[1]
                )
            else:
                ball_velocity.x += random.randint(
                    -ball_speed_variation[1], ball_speed_variation[1]
                )
            bounced = False

        # managing the velocity and position
        ball_pos.x += ball_velocity.x
        ball_pos.y += ball_velocity.y

    # stops the game if someone loses
    if ball_pos.x > window_width + ball_radius + 20:
        game_on = False
        points[0] += 1
    elif ball_pos.x < -ball_radius - 20:
        game_on = False
        points[1] += 1

    # prass P to start a new game and keep the score
    if keys[pygame.K_p] and not game_on:
        game_on = True
        ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        ball_velocity = pygame.Vector2(
            random.choice([-1, 1])
            * random.randint(beginning_ball_speed[0], beginning_ball_speed[1]),
            random.choice([-1, 1])
            * random.randint(beginning_ball_speed[0], beginning_ball_speed[1]),
        )

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
