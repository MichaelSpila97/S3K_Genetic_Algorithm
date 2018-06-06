import keyboard
import brain
from enum import Enum

import time
import action
import random

ng = random.Random()




def generate_action():

    return ng.choice(list(action.action_name))

def generate_delay():

    return ng.random()

def main():

    keyboard.wait('esc')

    while True:

        gaction = generate_action()
        delay = generate_delay()

        ng.seed()

        new_action = action.Action(gaction, delay)

        new_action.execute_action()





if __name__ == '__main__':
    main()
