import pygame
import random

# colors for reference
red = (255, 0, 0)
orange = (210, 90, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (200, 0, 255)
pink = (210, 0, 100)
white = (255, 255, 255)
black = (0, 0, 0)
eh = (200, 50, 100)

# variables (all of them can be edited to produce some GOOFY variations!)
auto_restart = False
fps = 60
bg_color = orange
player_speed = 800

window_width = 1280
window_height = 720

paddle_width = 30
paddle_height = 250
paddle_dist_from_wall = 0

ball_radius = 30
ball_speed_variation = (1, 2)
beginning_ball_speed = (4, 6)

ball_color = red
left_paddle_color = blue
right_paddle_color = purple

loser_text = "Press [P] to play again!"
loser_font = "freesansbold.ttf"
losertextcolor1 = pink
losertextcolor2 = green

points = [0, 0]
score_font = "freesansbold.ttf"
scoretextcolor1 = green
scoretextcolor2 = blue

# pygame setup, variable definitions
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
bounced = None
game_on = True

# collision engine variable setup
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

# game loop
while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keybind list
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

    # stops the game if someone loses, and the score updater
    if game_on:
        if ball_pos.x > window_width + ball_radius + 20:
            game_on = False
            points[0] += 1
        elif ball_pos.x < -ball_radius - 20:
            game_on = False
            points[1] += 1

    # text - text when someone loses plus the score
    loser_text_obj = pygame.font.Font(loser_font, 100).render(
        loser_text, True, losertextcolor1, losertextcolor2
    )
    score_text_obj = pygame.font.Font(score_font, 50).render(
        str(points), True, scoretextcolor1, scoretextcolor2
    )
    loser_text_rect = loser_text_obj.get_rect()
    score_text_rect = score_text_obj.get_rect()
    loser_text_rect.center = (window_width // 2, window_height // 2)
    score_text_rect.center = (window_width // 2, 50)

    if not auto_restart:
        screen.blit(loser_text_obj, loser_text_rect)
    screen.blit(score_text_obj, score_text_rect)

    if game_on:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(bg_color)

        # draw all the objects
        screen.blit(score_text_obj, score_text_rect)
        pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
        pygame.draw.rect(
            screen,
            left_paddle_color,
            (left_paddle_pos.x, left_paddle_pos.y, paddle_width, paddle_height),
        )
        pygame.draw.rect(
            screen,
            right_paddle_color,
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

        # ball bounce off walls:
        # top wall
        # ball movement
        if ball_pos.y - ball_radius < 0:
            ball_velocity.y = -ball_velocity.y
        # bottom wall
        if ball_pos.y + ball_radius > window_height:
            ball_velocity.y = -ball_velocity.y

        # ball bounce off left paddle:
        # front face
        if (
            ball_pos.x - ball_radius < left_paddle_pos.x + paddle_width
            and left_paddle_pos.y + paddle_height + ball_radius
            > ball_pos.y
            > left_paddle_pos.y - ball_radius
        ):
            ball_velocity.x *= -1
            bounced = True
        # top face
        if (
            ball_pos.y - ball_radius < left_paddle_pos.y + paddle_height
            and left_paddle_pos.x + paddle_width + ball_radius
            > ball_pos.x
            > left_paddle_pos.x - ball_radius
        ):
            ball_velocity.y *= -1
        # bottom face
        if (
            ball_pos.y - ball_radius < left_paddle_pos.y + paddle_height
            and left_paddle_pos.x + paddle_width + ball_radius
            > ball_pos.x
            > left_paddle_pos.x - ball_radius
        ):
            ball_velocity.y *= -1
            print("yay!")

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

    # prass P to start a new game and keep the score
    if (keys[pygame.K_p] or auto_restart) and not game_on:
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
    dt = clock.tick(fps) / 1000

pygame.quit()
