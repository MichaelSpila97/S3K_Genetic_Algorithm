import keyboard
import time
from enum import Enum

class action_name(Enum):
    move_left = 'left'
    move_right = 'right'
    press_down = 'down'
    press_up = 'up'
    jump_up = 'a'
    jump_right = ['right','a']
    jump_left = ['left', 'a']
    wait = ''
    spindash = ['down', 'a']
    jump_shield = ['a','a']


class Action:

    def generate_action():
        return action_name.jump_shield.value

    def generate_delay():
        return 0.1

    def __init__(self, action = generate_action(),delay = generate_delay()):
        self.action = action
        self.delay = delay

    def execute_action(self):
        if(self.action != 'wait'):

                if(isinstance(self.action, list)):
                    keyboard.press(self.action[0])
                    time.sleep(self.delay)
                    keyboard.release(self.action[0])

                    time.sleep(self.delay)
                    keyboard.press(self.action[1])
                    keyboard.release(self.action[1])

                else:
                    keyboard.press(self.action)
                    time.sleep(self.delay)
                    keyboard.release(self.action)
