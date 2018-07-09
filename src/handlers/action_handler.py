
import random
from copy import deepcopy

from ..enumval import ActionName
from ..classes import action

ng = random.Random()

# _______________________________________________________________________________________________________________________________
# Function responsible for generating random action
def generate_action():
    return ng.choice(list(ActionName))

# _______________________________________________________________________________________________________________________________
# Function responsible for generating random delay
def generate_delay():
    return ng.random()

# _______________________________________________________________________________________________________________________________
# Function responsible for checking weather an entity died
# Passes:
#       entity:     an Entity object
#       list_place: index value representing which action is being executed
def check_status(entity, list_place):
    if list_place > 0:

        entity_curr_lives = entity.action_list[list_place].lives_count
        entity_prev_lives = entity.action_list[list_place - 1].lives_count

        if entity_curr_lives < entity_prev_lives:
            entity.died()

# _______________________________________________________________________________________________________________________________
#   Function that controls the execution of an entities actions
# from its action list
# Passes:
#       entity: an Entity Object
def master_driver(master_entity):

    # If entity has already actions in its action list

    print('The master entity has actions to play out')

    for list_place, actions in enumerate(master_entity.getActionList()):
            actions.execute_action()
            check_status(list_place, master_entity.getActionList())


def generate_driver(entity):
    print('Generatiing new actions')
    for list_place in range(entity.getDNACap()):

        ng.seed()

        # Generates and execute new action
        new_action = action.Action(generate_action(), 1)
        new_action.execute_action()

        # Adds new action to entities action list
        entity.action_list.append(deepcopy(new_action))

        new_action = None

        # Checks status of entity
        check_status(entity, list_place)
        list_place += 1
        print(list_place)

def replay_driver(entity):

    for listplace, actions in enumerate(entity.getActionList()):

        actions.execute_action()

        check_status(entity, listplace)

        if not entity.isAlive():
            return

# _______________________________________________________________________________________________________________________________
