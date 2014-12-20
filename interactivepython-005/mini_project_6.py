# Mini-project # 6 - Blackjack

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_IMAGES = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png"
)

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
CARD_BACK = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png"
)

# initialize some useful global variables
in_play = False
outcome = "You can HIT or STAND"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
            raise ValueError

        self.is_hidden = False

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, is_hidden=False):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if is_hidden:
            canvas.draw_image(
                CARD_BACK, CARD_CENTER, CARD_BACK_SIZE,
                [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                CARD_SIZE
            )
            return

        canvas.draw_image(CARD_IMAGES, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self._cards = []
        self._hidden = []

    def __str__(self):
        pass    # return a string representation of a hand

    def add_card(self, card, is_hidden=False):
        if is_hidden:
            self._hidden.append(card)

        self._cards.append(card)

    def return_cards(self):
        cards = self._cards
        self._cards = []
        self._hidden = []
        return cards

    def get_cards(self):
        return list(self._cards)

    def draw(self, canvas, pos):
        for i, card in enumerate(self._cards):
            _pos = (pos[0] + i * CARD_SIZE[0], pos[1])
            is_hidden = True if card in self._hidden else False
            card.draw(canvas, _pos, is_hidden=is_hidden)


# define deck class
class Deck:
    def __init__(self):
        self._cards = []
        self._players = set([])

        for suit in SUITS:
            for rank in RANKS:
                self._cards.append(Card(suit, rank))

    def shuffle(self):
        for player in self._players:
            self._cards.extend(player.return_cards())

    def get_card(self, player, is_hidden=False):
        self._players.add(player)

        card = self._cards.pop(random.randrange(len(self._cards)))
        player.add_card(card, is_hidden=is_hidden)

    def __str__(self):
        pass    # return a string representing the deck


#define event handlers for buttons
def deal():
    global outcome, in_play

    outcome = "You can HIT or STAND"
    deck.shuffle()

    deck.get_card(player)
    deck.get_card(dealer, is_hidden=True)
    deck.get_card(player)
    deck.get_card(dealer)

    in_play = True


def hit():
    global in_play, player, score, outcome

    if not in_play:
        return

    deck.get_card(player)

    # check
    points = compute_points(player)
    if points > 21:
        score -= 1
        outcome = 'Player Busted!'
        in_play = False
    elif points == 21:
        score += 1
        outcome = 'Player Win!'
        in_play = False


def stand():
    global outcome, score, in_play

    if not in_play:
        return

    # check dealer
    while compute_points(dealer) < 17:
        deck.get_card(dealer)

    player_points = compute_points(player)
    dealer_points = compute_points(dealer)
    dealer._hidden = []

    if dealer_points > 21:
        outcome = 'Dealer Busted!'
        score += 1
    elif dealer_points > player_points or dealer_points == 21:
        outcome = 'Dealer Win!'
        score -= 1
    else:
        outcome = 'Player Win!'
        score += 1

    in_play = False


def compute_points(hand):
    cards = hand.get_cards()
    points = n_a = 0
    for card in cards:
        if card.rank == 'A':
            n_a += 1
        points += VALUES[card.rank]

    if points > 21:
        return points

    for _ in range(n_a):
        if points + 10 > 21:
            break

        points += 10

    return points


# draw handler
def draw(canvas):
    canvas.draw_text('Blackjack', (10, 20), 20, 'Black')
    canvas.draw_text('score: %s' % score, (30, 50), 20, 'Red')
    canvas.draw_text(outcome, (300, 20), 20, 'Yellow')

    dealer.draw(canvas, [100, 100])
    player.draw(canvas, [10, 400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deck = Deck()
player = Hand()
dealer = Hand()
deal()
frame.start()
