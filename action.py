import keyboard
import time
import random
import brain
import eyes
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

        self.ring_count = 0
        self.score_count = 0
        self.lives_count = 0
        self.act = ''

        self.mutation = 0.50

    def __str__(self):
        return f"""
        Action:                       {self.action}
        Action delay:                 {self.delay}
        Ring count during execution:  {self.ring_count}
        Score count during execution: {self.score_count}
        Lives count during execution: {self.lives_count}
        Act during execution:         {self.act}
        Mutation Chance:              {self.mutation}"""

    def set_core_stats(self):
        self.ring_count = brain.curr_rings
        self.score_count = brain.curr_score
        self.lives_count = brain.curr_lives
        self.act = brain.curr_act


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
