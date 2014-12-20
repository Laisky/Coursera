# Mini-project # 3 - "Stopwatch: The Game"

import simplegui


IS_RUNNING = False
SUCCESS_STOP = 0
TOTAL_STOP = 0
SECONDS = 0


def format(n_sec):
    """
    param n_sec: int, seconds * 10
    """
    minutes = n_sec // 600
    seconds = n_sec % 600 // 10
    millisec = n_sec % 10

    return '%d:%02d.%d' % (minutes, seconds, millisec)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global IS_RUNNING

    IS_RUNNING = True
    timer.start()


def stop_handler():
    global TOTAL_STOP, SUCCESS_STOP, IS_RUNNING

    timer.stop()

    if not IS_RUNNING:
        return

    TOTAL_STOP += 1
    if SECONDS % 100 == 0:
        SUCCESS_STOP += 1

    IS_RUNNING = False


def reset_handler():
    global SECONDS, TOTAL_STOP, SUCCESS_STOP, IS_RUNNING

    IS_RUNNING = False
    timer.stop()

    SECONDS = TOTAL_STOP = SUCCESS_STOP = 0


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global SECONDS

    SECONDS += 1


# define draw handler
def draw_handler(canvas):
    _score = '%s/%s' % (TOTAL_STOP, SUCCESS_STOP)

    canvas.draw_text(format(SECONDS), (120, 150), 30, 'White')
    canvas.draw_text(_score, [250, 20], 20, 'Yellow')


# create frame
frame = simplegui.create_frame("MyApp", 300, 300)

# register event handlers
frame.add_button("Start", start_handler, 150)
frame.add_button("Stop", stop_handler, 150)
frame.add_button("Reset", reset_handler, 150)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)


# start frame
frame.start()
