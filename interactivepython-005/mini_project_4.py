# Mini-project # 4 - "Pong"

# Implementation of classic arcade game Pong

import simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
BALL_POSITION = []
BALL_VELOCITY = []
PADDLE1_POS = [PAD_WIDTH / 2, HEIGHT / 2]
PADDLE2_POS = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
PADDLE1_VEL = [0, 0]
PADDLE2_VEL = [0, 0]
SCORE_LEFT = SCORE_RIGHT = '00'


# initialize ball_pos and BALL_VELOCITY for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global BALL_POSITION, BALL_VELOCITY

    BALL_POSITION = [WIDTH / 2, HEIGHT / 2]
    BALL_VELOCITY = [1 if 'RIGHT' == direction else -1, -1]


# define event handlers
def new_game():
    global PADDLE1_POS, PADDLE2_POS, PADDLE1_VEL, PADDLE2_VEL, \
        SCORE_LEFT, SCORE_RIGHT

    SCORE_LEFT = SCORE_RIGHT = '00'

    spawn_ball(random.choice(('RIGHT', 'LEFT')))


def accelarator():
    global BALL_VELOCITY

    BALL_VELOCITY[0] += 0.1 if BALL_VELOCITY[0] > 0 else -0.1
    BALL_VELOCITY[1] += 0.1 if BALL_VELOCITY[1] > 0 else -0.1


def collapse_check():
    global SCORE_RIGHT, SCORE_LEFT

    # left collapse
    if BALL_POSITION[0] - BALL_RADIUS <= PAD_WIDTH:
        if BALL_POSITION[1] + BALL_RADIUS < PADDLE1_POS[1] - HALF_PAD_HEIGHT \
                or BALL_POSITION[1] - BALL_RADIUS > PADDLE1_POS[1] + HALF_PAD_HEIGHT:
            SCORE_RIGHT = '%02d' % (int(SCORE_RIGHT) + 1)
            spawn_ball('RIGHT')
        else:
            BALL_VELOCITY[0] = -BALL_VELOCITY[0]

    # right collapse
    if BALL_POSITION[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if BALL_POSITION[1] + BALL_RADIUS < PADDLE2_POS[1] - HALF_PAD_HEIGHT \
                or BALL_POSITION[1] - BALL_RADIUS > PADDLE2_POS[1] + HALF_PAD_HEIGHT:
            SCORE_LEFT = '%02d' % (int(SCORE_LEFT) + 1)
            spawn_ball('LEFT')
        else:
            BALL_VELOCITY[0] = -BALL_VELOCITY[0]

    # height collapse
    if BALL_POSITION[1] + BALL_RADIUS >= HEIGHT \
            or BALL_POSITION[1] - BALL_RADIUS <= 0:
        BALL_VELOCITY[1] = -BALL_VELOCITY[1]


def draw(canvas):
    global SCORE_LEFT, SCORE_RIGHT, PADDLE1_POS, PADDLE2_POS, \
        BALL_POSITION, BALL_VELOCITY

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT],
                     1, "White")

    # update ball
    BALL_POSITION[0] += BALL_VELOCITY[0]
    BALL_POSITION[1] += BALL_VELOCITY[1]

    collapse_check()

    # draw ball
    canvas.draw_circle(BALL_POSITION, BALL_RADIUS, 1, 'White', 'White')

    # update paddle's vertical position, keep paddle on the screen
    if PADDLE1_POS[1] + HALF_PAD_HEIGHT < HEIGHT \
            and PADDLE1_VEL[1] > 0:
        PADDLE1_POS[1] += PADDLE1_VEL[1]

    if PADDLE1_POS[1] - HALF_PAD_HEIGHT > 0 \
            and PADDLE1_VEL[1] < 0:
        PADDLE1_POS[1] += PADDLE1_VEL[1]

    if PADDLE2_POS[1] + HALF_PAD_HEIGHT < HEIGHT \
            and PADDLE2_VEL[1] > 0:
        PADDLE2_POS[1] += PADDLE2_VEL[1]

    if PADDLE2_POS[1] - HALF_PAD_HEIGHT > 0 \
            and PADDLE2_VEL[1] < 0:
        PADDLE2_POS[1] += PADDLE2_VEL[1]

    # draw paddles
    canvas.draw_polygon(_get_paddle_axis(PADDLE1_POS), 1, 'White', 'White')
    canvas.draw_polygon(_get_paddle_axis(PADDLE2_POS), 1, 'White', 'White')

    # draw scores
    margin = 20
    canvas.draw_text(SCORE_LEFT, [WIDTH/2 - 2*margin, margin], 20, 'Yellow')
    canvas.draw_text(SCORE_RIGHT, [WIDTH/2 + margin, margin], 20, 'Yellow')


def _get_paddle_axis(center):
    p1 = [center[0] - HALF_PAD_WIDTH, center[1] - HALF_PAD_HEIGHT]
    p2 = [center[0] - HALF_PAD_WIDTH, center[1] + HALF_PAD_HEIGHT]
    p3 = [center[0] + HALF_PAD_WIDTH, center[1] + HALF_PAD_HEIGHT]
    p4 = [center[0] + HALF_PAD_WIDTH, center[1] - HALF_PAD_HEIGHT]

    return [p1, p2, p3, p4]


def keydown(key):
    global PADDLE1_VEL, PADDLE2_VEL

    if key == simplegui.KEY_MAP['up']:
        PADDLE2_VEL[1] = -3
    elif key == simplegui.KEY_MAP['down']:
        PADDLE2_VEL[1] = 3

    if key == simplegui.KEY_MAP['w']:
        PADDLE1_VEL[1] = -3
    elif key == simplegui.KEY_MAP['s']:
        PADDLE1_VEL[1] = 3


def keyup(key):
    global PADDLE1_VEL, PADDLE2_VEL

    PADDLE1_VEL = [0, 0]
    PADDLE2_VEL = [0, 0]


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("New Game", new_game, 150)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# accelarator
timer = simplegui.create_timer(1000, accelarator)

# start frame
new_game()
frame.start()
timer.start()
