# Mini-project # 5 - Memory

# implementation of card game - Memory

import simplegui
import random


WIDTH, HEIGHT = 800, 100
N_CARDS = 16
CARD_WIDTH = WIDTH / N_CARDS
CARDS = []
N_TURNS = 0


class Card():
    def __init__(self, number, width_range, height_range):
        self.number = number
        self.is_exposed = False
        self.is_confirmed = False
        self.width_range = width_range
        self.height_range = height_range

    def is_clicked(self, pos):
        x, y = pos
        if self.width_range[0] < x <= self.width_range[1]:
            return True

        return False

    def clicked(self):
        self.is_exposed = True

    def get_text(self):
        if self.is_exposed:
            return str(self.number)

        return ''


# helper function to initialize globals
def new_game():
    global CARDS, N_TURNS

    CARDS = []
    N_TURNS = 0
    numbers = list(range(N_CARDS / 2)) * 2
    random.shuffle(numbers)
    for width in range(0, WIDTH, WIDTH / N_CARDS):
        card = Card(number=numbers.pop(),
                    width_range=(width, width + CARD_WIDTH),
                    height_range=(0, HEIGHT))
        CARDS.append(card)

    hidden_cards()


# define event handlers
def mouseclick(pos):
    # add game state logic here
    for card in CARDS:
        if card.is_clicked(pos):
            if card.is_exposed:
                return

            card.clicked()
            card_check(card)
            return


def card_check(this):
    n_exposed = 0
    for card in CARDS:
        if not card.is_exposed or card.is_confirmed:
            continue

        if card is this:
            continue

        n_exposed += 1
        if n_exposed == 2:
            hidden_cards(this)
            return

    for card in CARDS:
        if not card.is_exposed or card.is_confirmed:
            continue

        if card is not this and card.number == this.number:
            card.is_confirmed = True
            this.is_confirmed = True
            return


def hidden_cards(this=None):
    global N_TURNS

    if this:
        N_TURNS += 1
    label.set_text('Turns = %s' % N_TURNS)

    for card in CARDS:
        if not card.is_confirmed and card is not this:
            card.is_exposed = False


# cards are logically 50x100 pixels in size
def draw(canvas):
    for card in CARDS:
        canvas.draw_line((card.width_range[1], 0),
                         (card.width_range[1], HEIGHT),
                         1, 'White')
        card_text = card.get_text()
        canvas.draw_text(
            card_text,
            (card.width_range[0] + CARD_WIDTH / 2 - 5, HEIGHT / 2),
            20,
            'White'
        )


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
