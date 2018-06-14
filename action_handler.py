import keyboard
import brain
from enum import Enum

import time
import action
import random
import copy
ng = random.Random()


def generate_action():

    return ng.choice(list(action.action_name))

def generate_delay():

    return ng.random()

def check_status(entity, list_place):

    if list_place > 0:
        if entity.action_list[list_place].lives_count < entity.action_list[list_place - 1].lives_count:
            entity.died()

def action_driver(entity):

    if entity.action_list == True:
        #print('has action to replay')
        list_place = 0
        for x in entity.action_list:

            if not entity.isAlive:
                print('Entity died while replaying actions')
                break

            else:
                 x.execute_action()

            check_status(entity, list_place)
            list_place += 1

    while entity.isAlive():
        #print('Either has no action to replay or is done replaying action and is still alive')
        list_place = len(entity.action_list) - 1

        ng.seed()
        new_action = action.Action(generate_action(), generate_delay())

        new_action.execute_action()

        entity.action_list.append(copy.deepcopy(new_action))

        new_action = None
        check_status(entity, list_place)
