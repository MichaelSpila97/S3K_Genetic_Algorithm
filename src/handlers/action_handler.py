
import random
import time

from copy import deepcopy

from ..enumval import ActionName
from ..classes import action

ng = random.Random()

# _______________________________________________________________________________________________________________________________
# Function responsible for generating a random action
def generate_action():
    return ng.choice(list(ActionName))

# _______________________________________________________________________________________________________________________________
# Function responsible for generating a random delay
def generate_delay():
    return ng.random()

# _______________________________________________________________________________________________________________________________
# Function responsible for checking if an entity died
# Passes:
#       entity:     an Entity object
#       list_place: index value representing which action is being executed
def check_status(entity, list_place):
    if list_place > 0:

        entity_curr_lives = entity.getActionList()[list_place].lives_count
        entity_prev_lives = entity.getActionList()[list_place - 1].lives_count

        if entity_curr_lives < entity_prev_lives:
            entity.died()

# _______________________________________________________________________________________________________________________________
#   Function that controls the execution of the master_entities actions
# from its action list
# Passes:
#       A master entity
def master_driver(master_entity):

    # If entity has already actions in its action list

    print('     The master entity has actions to play out....')

    for list_place, actions in enumerate(master_entity.getActionList()):
            actions.execute_action()
            print(str(actions))
            check_status(master_entity, list_place)
            time.sleep(0.1)
# _______________________________________________________________________________________________________________________________
#   Function that generates new action for entities that have no actions in
# thier action list
# Passes:
#       A entity
def generate_driver(entity):
    print('     Generatiing new actions....')
    for list_place in range(entity.getDNACap()):

        ng.seed()

        # Generates and execute new action
        new_action = action.Action(generate_action(), 1)
        print(str(new_action))
        new_action.execute_action()

        # Adds new action to entities action list
        entity.action_list.append(deepcopy(new_action))

        new_action = None

        # Checks status of entity
        check_status(entity, list_place)
        list_place += 1
        time.sleep(0.1)

# _______________________________________________________________________________________________________________________________
#   Function that replays action from a entity's action list. If stagnation was
# detected then the function will generate new action for the entity till is new
# dna cap is reached
# Passes:
#       A entity
def replay_driver(entity):
    print("     Replaying Actions....")
    for listplace, actions in enumerate(entity.getActionList()):

        print(str(actions))
        actions.execute_action()

        check_status(entity, listplace)

        if not entity.isAlive():
            return
        time.sleep(0.1)

    # Will enter loop if dnacap was increased due to stagnation
    while len(entity.getActionList()) < entity.getDNACap():
        print("     Adding New Actions to attempt to resolve stagnation")
        ng.seed()

        # Generates and execute new action
        new_action = action.Action(generate_action(), 1)
        new_action.execute_action()

        # Adds new action to entities action list
        entity.getActionList().append(deepcopy(new_action))

        new_action = None

        # Checks status of entity
        check_status(entity, len(entity.getActionList()) - 1)
        time.sleep(0.1)
    print('')
# _______________________________________________________________________________________________________________________________
