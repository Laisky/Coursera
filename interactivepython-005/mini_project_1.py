

# Rock-paper-scissors-lizard-Spock template
from random import randrange

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# Why not support collections.namedtuple ?!!!
rock = ('rock', 0)
Spock = ('Spock', 1)
paper = ('paper', 2)
lizard = ('lizard', 3)
scissors = ('scissors', 4)

CHOCIE = (rock, Spock, paper, lizard, scissors)

# helper functions


def name_to_number(name):
    # delete the following pass statement and fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    for choice in CHOCIE:
        if choice[0] == name:
            return choice[1]


def number_to_name(number):
    # delete the following pass statement and fill in your code below

    # convert number to a name using if/elif/else
    # don't forget to return the result!
    for choice in CHOCIE:
        if choice[1] == number:
            return choice[0]


def rpsls(player_choice):
    # delete the following pass statement and fill in your code below

    # print a blank line to separate consecutive games
    print('')

    # print out the message for the player's choice
    print(player_choice)

    # convert the player's choice to player_number
    # using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)

    # print out the message for computer's choice
    # why not support format?!!!
    print('Computer chooses %s' % comp_choice)

    # compute difference of comp_number and player_number modulo five
    difference = comp_number - player_number
    difference = difference if difference >= 0 else difference + 5

    # use if/elif/else to determine winner, print winner message
    if 1 <= difference <= 2:
        print('Computer wins!')
    elif difference == 0:
        print('Player and computer tie!')
    else:
        print('Player wins!')


# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
