import keyboard
import time
import random
import brain
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
        self.score = 0

        self.ring_count = 0
        self.score_count = 0
        self.lives_count = 0
        self.mutation = 0.50

    def __str__(self):
        return f"""
        \033[0;32;40mAction:                       \033[0;36;40m{self.action}
        \033[0;32;40mAction delay:                 \033[0;36;40m{self.delay}
        \033[0;32;40mPoints assigned to action:    \033[0;36;40m{self.score}
        \033[0;32;40mRing count during execution:  \033[0;36;40m{self.ring_count}
        \033[0;32;40mScore count during execution: \033[0;36;40m{self.score_count}
        \033[0;32;40mLives count during execution: \033[0;36;40m{self.lives_count}
        \033[0;32;40mMutation Rate:                \033[0;36;40m{self.mutation}"""

    def set_core_stats(self):
        self.ring_count = brain.curr_rings
        self.score_count = brain.curr_score
        self.lives_count = brain.curr_lives
        

    def execute_action(self):

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

        self.set_core_stats()
