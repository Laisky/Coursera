# Mini-project # 2 - "Guess the number" game"

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
from math import log, ceil
import simplegui


SECRET_NUMBER = 0
SECRET_NUMBER_RANGE = (0, 100)
NUMBER_TO_TRY = 0


# helper function to start and restart the game
def new_game():
    global SECRET_NUMBER, NUMBER_TO_TRY
    SECRET_NUMBER = random.randrange(*SECRET_NUMBER_RANGE)

    print('\nNew game. Range is from %s to %s' % SECRET_NUMBER_RANGE)

    # calculate number to try
    # 2 ** n >= high - low + 1
    NUMBER_TO_TRY = int(ceil(
        log(SECRET_NUMBER_RANGE[1] - SECRET_NUMBER_RANGE[0] + 1) / log(2)
    ))
    print('Number of remaining guesses is %s' % NUMBER_TO_TRY)


# define event handlers for control panel
def range100():
    global SECRET_NUMBER_RANGE
    SECRET_NUMBER_RANGE = (0, 100)
    new_game()


def range1000():
    global SECRET_NUMBER_RANGE
    SECRET_NUMBER_RANGE = (0, 1000)
    new_game()


def input_guess(guess):
    global NUMBER_TO_TRY

    guess = int(guess)
    print('\nGuess was %s' % guess)

    NUMBER_TO_TRY -= 1
    print('Number of remaining guesses is %s' % NUMBER_TO_TRY)
    if NUMBER_TO_TRY == 0:
        print('You ran out of guesses.  The number was %s' % SECRET_NUMBER)
        new_game()
        return

    # compair
    if guess == SECRET_NUMBER:
        answer = 'Correct!'
    else:
        answer = 'Higher' if guess > SECRET_NUMBER else 'Lower'

    print(answer)


# create frame
frame = simplegui.create_frame("MyApp", 300, 300)
frame.add_input("Enter", input_guess, 150)
frame.add_button("Range: 0 - 100", range100, 150)
frame.add_button("Range: 0 - 1000", range1000, 150)

new_game()
