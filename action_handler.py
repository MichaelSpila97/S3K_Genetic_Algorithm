import keyboard
import brain
from enum import Enum

import time
import action

def main():
    new_action = action.Action()

    keyboard.wait('esc')
    new_action.execute_action()


if __name__ == '__main__':
    main()
