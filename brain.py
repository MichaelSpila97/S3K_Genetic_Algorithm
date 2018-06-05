from tkinter import *
from enum import Enum

import eyes
import time
import keyboard

class Keyboard_inputs(Enum):
    move_left = 'left'
    move_right = 'right'
    move_up = 'up'
    move_down = 'down'

    jump = 'a'
    spin_dash = 'down, down, down, a'


def main():
    print(keyboard.record())
    #root = Tk()

    #frame = Frame(root, width=100, height=50)
    #frame.pack()

    #score_L = Label(root, text= "The Game Has not Started Yet")
    #score_L.pack()

    #ring_L = Label(root, text ='')
    #ring_L.pack()

    #labels = [score_L, ring_L]
    #root.after('500', update_core_stats, root, labels)
    #root.mainloop()




def update_core_stats(root, labels):
    playGame()
    if gameStarted():
        playGame()
        updated_score = eyes.score_grab()
        updated_rings = eyes.ring_grab()

        labels[0].configure (text = 'Current Score: ' + str(validate_score(updated_score)))
        labels[1].configure (text = 'Current Rings: ' + str(validate_rings(updated_rings)))

    ##root.after('500', update_core_stats,root, labels)


curr_rings = 0
curr_score = 0

def validate_score(score):
    global curr_score

    if score == 'Could not obtain score':
        return curr_score
    elif int(score)%100 != 0 or int(score) == 0:
        return curr_score
    elif int(score) < int(curr_score):
        return curr_score
    else:
        curr_score = int(score)
        return curr_score

def validate_rings(rings):
    global curr_rings
    if rings == 'Could not obtain ring count':
        return curr_rings
    elif int(rings) < curr_rings and int(rings) != 0:
        return curr_rings
    elif int(rings) > 999:
        return curr_rings
    else:
        curr_rings = int(rings)
        return curr_rings


game_started = False

def gameStarted():

    global game_started

    if game_started == False:

        if eyes.score_grab() != 'Could not obtain score' and eyes.ring_grab() != 'Could not obtain ring count':

            game_started = True

    return game_started

def playGame():


    print(keyboard.record())


if __name__ == '__main__':
    main()
