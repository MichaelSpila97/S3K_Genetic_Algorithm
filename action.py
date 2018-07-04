import keyboard
import time
from enum import Enum

import gdv
# ______________________________________________________________________________
#   Action is an object that represent a single action executed by the computer
# during a session of Sonic 3 and Knukles
# Each Action have the following attributes to them:
#   action:      the string or list of strings, from the enumerated action_name
#                class, that contain the buttons need when executing an
#                action_name
#
#   delay:       The time that is required in between pressing and releasing
#                the button for an action to be preformed. Also can be used to
#                represent the time need to execute a particular action
#
#   ring_count:  The ring_count that is recorded during the execution of the
#                action
#
#   score_count: The score_count that is recorded during the execution of the
#                action
#
#   lives_count: The lives_count that is recorded during the execution of the
#                action
#
#   act:         The act that is recorded during the execution of the action
#
#   mutation:    The rate in which an action will change to a diffrent action
#                during the repoduction phase
# ______________________________________________________________________________


class action_name(Enum):
    move_left = 'left'
    move_right = 'right'
    press_down = 'down'
    press_up = 'up'
    jump_up = 'a'
    jump_right = ['right', 'a']
    jump_left = ['left', 'a']
    wait = ''
    spindash = ['down', 'a']
    jump_shield = ['a', 'a']


class Action:
    # __________________________________________________________________________
    def __init__(self, action, delay, mutation=0.5):
        self.action = action
        self.delay = delay
        self.mutation = mutation

        self.ring_count = 0
        self.score_count = 0
        self.lives_count = 0
        self.act = ''

    # __________________________________________________________________________
    def __str__(self):
        return f"""
        Action:                       {self.action}
        Action delay:                 {self.delay}
        Ring count during execution:  {self.ring_count}
        Score count during execution: {self.score_count}
        Lives count during execution: {self.lives_count}
        Act during execution:         {self.act}
        Mutation Chance:              {self.mutation}"""

    # __________________________________________________________________________
    # Function for setting the core stats of the action object during execution
    def set_core_stats(self):
        self.ring_count = gdv.curr_rings
        self.score_count = gdv.curr_score
        self.lives_count = gdv.curr_lives
        self.act = gdv.curr_act

    # __________________________________________________________________________
    # The Function that execute the action through keyboard presses
    def execute_action(self):

        # Execution instructions for waiting
        if self.action == action_name.wait:
            time.sleep(self.delay)

        # Execution instructions for spindash
        elif self.action == action_name.spindash:
            keyboard.press(self.action.value[0])
            time.sleep(self.delay)

            for x in range(0, 3):
                keyboard.press(self.action.value[1])
                time.sleep(0.3)
                keyboard.release(self.action.value[1])
                time.sleep(0.1)

            keyboard.release(self.action.value[0])

        # Execution instructions for jump_shield
        elif self.action == action_name.jump_shield:

            keyboard.press(self.action.value[0])
            time.sleep(self.delay)
            keyboard.release(self.action.value[0])
            time.sleep(0.1)
            keyboard.press(self.action.value[1])
            time.sleep(0.1)
            keyboard.release(self.action.value[1])

        # Execution instructions for jump_right and jump_left
        elif isinstance(self.action.value, list):
            keyboard.press(self.action.value[0])
            time.sleep(0.2)
            keyboard.press(self.action.value[1])
            time.sleep(self.delay)
            keyboard.release(self.action.value[1])
            keyboard.release(self.action.value[0])

        # Execution instructions for every other action
        else:

            keyboard.press(self.action.value)
            time.sleep(self.delay)
            keyboard.release(self.action.value)

        # Set stats after execution is complete
        self.set_core_stats()

# ______________________________________________________________________________
# --------------------Getter methods for Action attributes---------------------
    def getAction(self):
        return self.action

    def getDelay(self):
        return self.delay

    def getRingCount(self):
        return self.ring_count

    def getScoreCount(self):
        return self.score_count

    def getLivesCount(self):
        return self.lives_count

    def getAct(self):
        return self.act

    def getMutation(self):
        return self.mutation

# -------------------Setter methods for Action attributes----------------------
    def setAction(self, action):
        self.action = action

    def setDelay(self, delay):
        self.delay = delay

    def setRingCount(self, ring):
        self.ring_count = ring

    def setScoreCount(self, score):
        self.score_count = score

    def setLivesCount(self, lives):
        self.lives_count = lives

    def setAct(self, act):
        self.act = act

    def setMutation(self, mutation):
        self.mutation = mutation
