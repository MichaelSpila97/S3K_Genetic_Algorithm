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

def check_status(entity, list_place = None):

    if list_place == None:
        if entity.action_list[len(entity.action_list) - 1].lives_count < entity.action_list[len(entity.action_list) - 2].lives_count:
            entity.died()
    else:
        if list_place > 0:
            if entity.action_list[list_place].lives_count < entity.action_list[list_place - 1].lives_count:
                entity.died()

def action_driver(entity):

    if entity.action_list:
        list_place = 0
        for x in entity.action_list:

            if not entity.isAlive:
                print('Entity died while replaying actions')
                break

            else:
                 x.execute_action()

            check_status(entity, list_place)
            ++list_place

    while entity.isAlive():
        ng.seed()
        new_action = action.Action(generate_action(), generate_delay())

        new_action.execute_action()

        entity.action_list.append(new_action)
        check_status(entity)
