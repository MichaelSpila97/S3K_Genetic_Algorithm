import time

from src.enumval import StatNumberMaps, StatScreenPos
from ..gdmodules import gdr
import trainingdriver

# ______________________________________________________________________________
#        This contains the collection of funciton that validate and stores the
#  core in game statistic that is used by the Aciton objects
# ______________________________________________________________________________
# Global Variables used to keep track of current in game values
curr_rings = 0
curr_score = 0
curr_lives = 3
curr_act = ''
curr_entity = ''

# Booleans vars used to determine if training has started and if the global stats
# need to be updated by force
training_start = False
force_update = False

# Global tuples that contains the basic info needed for the screen reader, in gdv.py,
# to function properly
live_info = ('lives', StatNumberMaps.live_num_map.value, StatScreenPos.lives.value)
score_info = ('score', StatNumberMaps.score_num_map.value, StatScreenPos.score.value)
ring_info = ('rings', StatNumberMaps.ring_num_map.value, StatScreenPos.rings.value)

# Reset Stats to intial values when called on
def reset_stats():
    print('Reseting Stats for next Training Session')
    global curr_rings, curr_score, curr_lives, curr_act, force_update
    curr_rings = 0
    curr_score = 0
    curr_lives = 3
    force_update = True
# ______________________________________________________________________________

# Function obtain core stats through screen readers grab_stat() functions and
# tells the GUI to update the labels of the stats if the one of stats
# has changed values
def get_core_stats():
    global force_update, curr_entity

    while True:
        # Stores previous values of global for purpose of dectecting a change
        # each statistic
        lives = curr_lives
        rings = curr_rings
        score = curr_score
        act = curr_act

        # Obtains the current values of each statists from the screen reader
        # or trainingdriver
        entity = trainingdriver.entity_playing
        validate_lives(gdr.grab_stat(live_info))
        validate_score(gdr.grab_stat(score_info))
        validate_rings(gdr.grab_stat(ring_info))
        validate_act()

        detect_change = lives != curr_lives or \
                        rings != curr_rings or \
                        score != curr_score or \
                        act != curr_act or \
                        curr_entity != entity

        # If change is detected or update is forced the GUI will be told to update
        # its labels that display the statists to the current values stored in the
        # globals
        if detect_change or force_update:
            trainingdriver.gui_func_qu.put('Update Texts')
            curr_entity = trainingdriver.entity_playing

            # Reset force_update to false so force update doesn't immediatly trigger
            # an update again
            if force_update:
                force_update = False

        # Makes thread sleep so the function isn't constatly calling the screen reader
        # and slowing the program down in the process
        time.sleep(0.1)
# ______________________________________________________________________________
# Passes:
#       score: the incoming score count
#
# Returns:
#       curr_score: the global variable of the score count
def validate_score(score):
    global curr_score

    if score == 'Could not obtain score':
        return curr_score

    # Score must be multiple of 10 or equal 0
    elif int(score) % 10 != 0 or int(score) == 0:
        return curr_score

    else:
        curr_score = int(score)
        return curr_score
# ______________________________________________________________________________
# Passes:
#       rings: the incoming ring count
#
# Returns:
#       curr_rings: the global variable of the ring count
def validate_rings(rings):
    global curr_rings

    if rings == 'Could not obtain rings':
        return curr_rings

    # ring cannot decrease to a non zero value
    elif int(rings) < curr_rings and int(rings) != 0:
        return curr_rings

    # rings cannot exceed over 999
    elif int(rings) > 999:
        return curr_rings

    else:
        curr_rings = int(rings)
        return curr_rings
# ____________________________________________________________________________
# Passes:
#       lives: the incoming lives count
#
# Returns:
#       curr_lives: the global variable of the lives
def validate_lives(lives):
    global curr_lives

    if lives == 'Could not obtain lives':
        return curr_lives

    # lives should not increase or decreases more than once at a time
    # Ex: lives 3 -> 2 or 3->4 is good
    #    lives 3 -> 0 or 3 -> 7 not good
    elif lives > curr_lives + 1 or lives < curr_lives - 1:
        return curr_lives

    else:
        curr_lives = int(lives)
        return curr_lives
# ______________________________________________________________________________
# Returns:
#        curr_act: the global variable that represent the act status
def validate_act():
    global curr_act
    act_b_status = gdr.grab_stat(('Bact', StatNumberMaps.act_b_map.value, StatScreenPos.act_b.value))
    act_e_status = gdr.grab_stat(('Eact', StatNumberMaps.act_e_map.value, StatScreenPos.act_e.value))

    act_b_fail_str = 'Could not obtain Bact'
    act_e_fail_str = 'Could not obtain Eact'

    if act_b_status != act_b_fail_str:
        curr_act = f'Act {act_b_status}'

    elif act_e_status != act_e_fail_str:
        curr_act = f'Act {act_e_status} End'

    elif curr_act == 'Act 2 End':
        curr_act = f'Transitioning to next Zone...'

    return curr_act


# _____________________________________________________________________________
# Function responsible for finiding out if training is aloud to start
#
# Returns:
#        training_start: a boolean variable that tells wheather training can be
#                        started
def isTrainingStarted():

    global training_start

    fring_str = 'Could not obtain rings'
    fscore_str = 'Could not obtain score'
    flives_str = 'Could not obtain lives'

    if gdr.grab_stat(ring_info) == fring_str and \
       gdr.grab_stat(score_info) == fscore_str and \
       gdr.grab_stat(live_info) == flives_str:

        training_start = False
    else:
        training_start = True

    return training_start
