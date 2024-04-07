import pygame as pg
import math
import random

WIDTH = 1200
HEIGHT = 900
score = 0
lives = 3
time = 0
started = False


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float("inf")
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = pg.image.load("rice_rocks/assets/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = pg.image.load("rice_rocks/assets/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = pg.image.load("rice_rocks/assets/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = pg.image.load("rice_rocks/assets/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = pg.image.load("rice_rocks/assets/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = pg.image.load("rice_rocks/assets/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = pg.image.load("rice_rocks/assets/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
pg.mixer.init()
pg.mixer.music.set_volume(0.5)
soundtrack = pg.mixer.music.load("rice_rocks/assets/soundtrack.mp3")
missile_sound = pg.mixer.music.load("rice_rocks/assets/missile.mp3")
ship_thrust_sound = pg.mixer.music.load("rice_rocks/assets/thrust.mp3")
explosion_sound = pg.mixer.music.load("rice_rocks/assets/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(
                self.image,
                [self.image_center[0] + self.image_size[0], self.image_center[1]],
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )
        else:
            canvas.draw_image(
                self.image,
                self.image_center,
                self.image_size,
                self.pos,
                self.image_size,
                self.angle,
            )
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * 0.1
            self.vel[1] += acc[1] * 0.1

        self.vel[0] *= 0.99
        self.vel[1] *= 0.99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += 0.05

    def decrement_angle_vel(self):
        self.angle_vel -= 0.05

    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [
            self.pos[0] + self.radius * forward[0],
            self.pos[1] + self.radius * forward[1],
        ]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(
            Sprite(
                missile_pos,
                missile_vel,
                self.angle,
                0,
                missile_image,
                missile_info,
                missile_sound,
            )
        )

    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.pos


# Sprite class
class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        super().__init__()
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(
            self.image,
            self.image_center,
            self.image_size,
            self.pos,
            self.image_size,
            self.angle,
        )

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.age += 1

        if self.age > self.lifespan:
            # print("T")
            return True
        else:
            # print("F")
            return False

    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.pos

    def get_lifespan(self):
        return self.lifespan

    def get_age(self):
        return self.age

    def collide(self, other_object):
        dist = math.sqrt(
            (self.pos[0] - other_object.get_position()[0]) ** 2
            + (self.pos[1] - other_object.get_position()[1]) ** 2
        )
        cdist = self.radius + other_object.get_radius()
        if dist < cdist:
            return True
        else:
            return False


def group_collide(group, single):
    collide = 0
    for rock in list(group):
        if rock.collide(single):
            group.remove(rock)
            collide = 1
    if collide == 1:
        return True
    else:
        return False


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True


def draw(canvas):
    global time, started, score, lives

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(
        nebula_image,
        nebula_info.get_center(),
        nebula_info.get_size(),
        [WIDTH / 2, HEIGHT / 2],
        [WIDTH, HEIGHT],
    )
    canvas.draw_image(
        debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT)
    )
    canvas.draw_image(
        debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT)
    )

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    for rock in rock_group:
        rock.draw(canvas)
    for missile in missile_group:
        missile.draw(canvas)
        print(missile.get_lifespan())
        print(missile.get_age())

    # update ship and sprites
    my_ship.update()
    for rock in rock_group:
        rock.update()
    for missile in list(missile_group):
        print("T")
        if missile.update():
            print("T")
            missile_group.remove(missile)

    # collide
    if group_collide(rock_group, my_ship):
        lives -= 1

    # draw splash screen if not started
    if not started:
        canvas.draw_image(
            splash_image,
            splash_info.get_center(),
            splash_info.get_size(),
            [WIDTH / 2, HEIGHT / 2],
            splash_info.get_size(),
        )


# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3]
    rock_avel = random.random() * 0.2 - 0.1
    if len(rock_group) <= 12:
        rock_group.add(
            Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        )


# initialize stuff
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = pg.sprite.Group()
missile_group = pg.sprite.Group()
# Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    # key handlers to control ship
    if keys[pg.K_LEFT]:
        my_ship.decrement_angle_vel()
    elif keys[pg.K_RIGHT]:
        my_ship.increment_angle_vel()
    elif keys[pg.K_UP]:
        my_ship.set_thrust(True)
    elif keys[pg.K_SPACE]:
        my_ship.shoot()

    clock.tick(60)
