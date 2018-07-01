
import random
from copy import deepcopy

import action

ng = random.Random()

# _______________________________________________________________________________________________________________________________
# Function responsible for generating random action
def generate_action():
    return ng.choice(list(action.action_name))

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
def action_driver(entity):

    # If entity has already actions in its action list
    if entity.action_list:
        print('has action to replay')

        list_place = 0

        old_list = deepcopy(entity.action_list)
        entity.setActionList([])

        for actions in old_list:

            # Stops action replay if the entity dies
            if not entity.isAlive():
                print('Entity died while replaying actions')
                return

            # Creates a new action object based of current action in the old_list
            else:
                action = action.Action(actions.getAction(), action.getDelay(), action.getMutation())
                action.execute_action()

                entity.action_list.append(deepcopy(action))
                action = None

            check_status(entity, list_place)
            list_place += 1

    print('Done replaying actions and creating new ones')

    list_place = len(entity.action_list) - 1
    
    # Continues to play and generate random action till the entity dies
    while entity.isAlive():

        ng.seed()

        # Generates and execute new action
        new_action = action.Action(generate_action(), generate_delay())
        new_action.execute_action()

        # Adds new action to entities action list
        entity.action_list.append(deepcopy(new_action))

        new_action = None

        # Checks status of entity
        check_status(entity, list_place)
        list_place += 1
# _______________________________________________________________________________________________________________________________
