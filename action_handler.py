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

def set_core_stats(action, entity, action_list):

    action.set_live(brain.curr_lives , entity, action_list)
    action.set_rings(brain.curr_rings)
    action.set_score(brain.curr_score)

def non_gen_action_driver(entity):

    for x in entity.action_list:

        x.execute_action()

        set_core_stats(entity.new_action , entity, entity.action_list)

        if not entity.isAlive():
            break

    if entity.isAlive():
        gen_action_driver(entity)


def gen_action_driver(entity):

    while entity.isAlive():

        gaction = generate_action()
        delay = generate_delay()
        ng.seed()

        new_action = action.Action(gaction, delay)

        new_action.execute_action()
        set_core_stats(new_action , entity, entity.action_list)

        entity.action_list.append(new_action)
