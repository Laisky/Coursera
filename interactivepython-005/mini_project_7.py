# Mini-project # 7 - Spaceship

# program template for Spaceship
import simplegui
import math
import random
import time as systime


# globals for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = 0.02
score = 0
lives = 3
time = 0.5
a_missile = None


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None,
                 animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
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


# art assets created by Kim Lathrop,
# may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png,
# debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png,
# debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/debris2_blue.png"
)

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/nebula_blue.f2014.png"
)

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/splash.png"
)

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com"
    "/codeskulptor-assets/lathrop/double_ship.png"
)

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 5)
missile_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/shot2.png"
)

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/asteroid_blue.png"
)

# animated explosion - explosion_orange.png, explosion_blue.png,
# explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/lathrop/explosion_alpha.png"
)

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/sounddogs/soundtrack.mp3"
)
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/sounddogs/missile.mp3"
)
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/sounddogs/thrust.mp3"
)
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/"
    "codeskulptor-assets/sounddogs/explosion.mp3"
)


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def movement(pos, vel, canvas_layout):
    for dimension in (0, 1):
        pos[dimension] += vel[dimension]

        if pos[dimension] > canvas_layout[dimension]:
            pos[dimension] = 0
        elif pos[dimension] < 0:
            pos[dimension] = canvas_layout[dimension]


def fire():
    global a_missile

    foward = angle_to_vector(my_ship.angle)
    tmppos = [my_ship.pos[0] + 45 * foward[0], my_ship.pos[1] + 45 * foward[1]]
    tmpvel = [my_ship.vel[0] + foward[0] * 3, my_ship.vel[1] + foward[1] * 3]
    a_missile = Sprite(tmppos, tmpvel, 0, 0, missile_image,
                       missile_info, missile_sound)
    missile_sound.play()


def keydown(key):
    if key == simplegui.KEY_MAP['space']:
        fire()

    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True

    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = -0.1
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0.1


def keyup(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False

    if key == simplegui.KEY_MAP['left']\
            or key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0


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
            self.image_center[0] = 135
        else:
            self.image_center[0] = 45

        canvas.draw_image(self.image,
                          self.image_center, self.image_size,
                          self.pos, self.image_size,
                          self.angle)

    def update(self):
        if self.thrust:
            ship_thrust_sound.play()
            vel = angle_to_vector(self.angle)
            ship_xvel = self.vel[0] + vel[0]
            ship_yvel = self.vel[1] + vel[1]
            if ship_xvel ** 2 + ship_yvel ** 2 < 15:
                self.vel[0] = ship_xvel
                self.vel[1] = ship_yvel
        else:
            ship_thrust_sound.rewind()

        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)
        movement(self.pos, self.vel, (WIDTH, HEIGHT))
        self.angle += self.angle_vel


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
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
        self.created_at = systime.time()
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image,
                          self.image_center, self.image_size,
                          self.pos, self.image_size,
                          self.angle)

    def update(self):
        if systime.time() - self.created_at > self.lifespan:
            self.pos[0] = WIDTH + 1
            return

        movement(self.pos, self.vel, (WIDTH, HEIGHT))
        self.angle += self.angle_vel


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text('lives: %s' % lives, (50, 50), 24, "Yellow")
    canvas.draw_text('score: %s' % score, (50, 100), 24, "Yellow")

    if a_missile:
        a_missile.draw(canvas)
        a_missile.update()

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()


# timer handler that spawns a rock
def rock_spawner():
    global a_rock

    a_rock = Sprite([random.random() * WIDTH, random.random() * HEIGHT],
                    [random.random(), random.random()],
                    random.random() * 2 * math.pi, random.random() * 0.1,
                    asteroid_image, asteroid_info)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# initialize ship and two sprites
# pos, vel, ang, ang_vel, image, info, sound=None
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3],
                [random.choice(range(1, 5)), random.choice(range(1, 5))],
                0, 0.1,
                asteroid_image, asteroid_info)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
