import keyboard
import time
import random

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


    def __init__(self, action, delay):
        self.action = action
        self.delay = delay


    def execute_action(self):

        print(f' action name: {self.action}')
        print(f' action delay: {self.delay}')

        if  self.action == action_name.wait:
            time.sleep(self.delay)

        elif self.action == action_name.spindash:
            keyboard.press(self.action.value[0])
            time.sleep(self.delay)

            for x in range(0,3):
                keyboard.press(self.action.value[1])
                time.sleep(0.3)
                keyboard.release(self.action.value[1])
                time.sleep(0.1)

            keyboard.release(self.action.value[0])


        elif self.action == action_name.jump_shield:

            keyboard.press(self.action.value[0])
            time.sleep(self.delay)
            keyboard.release(self.action.value[0])
            time.sleep(0.1)
            keyboard.press(self.action.value[1])
            time.sleep(0.1)
            keyboard.release(self.action.value[1])

        elif isinstance(self.action.value, list):
            keyboard.press(self.action.value[0])
            time.sleep(0.2)
            keyboard.press(self.action.value[1])
            time.sleep(self.delay)
            keyboard.release(self.action.value[1])
            keyboard.release(self.action.value[0])
            
        else:

            keyboard.press(self.action.value)
            time.sleep(self.delay)
            keyboard.release(self.action.value)
