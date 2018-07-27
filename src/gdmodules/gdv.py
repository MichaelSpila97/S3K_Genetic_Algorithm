import time
from copy import deepcopy

from src.enumval import StatNumberMaps, StatScreenPos
from src.gdmodules.gdr import grab_stat
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

at_start_screen = False
training_start = False
force_update = False

live_info = ('lives', StatNumberMaps.live_num_map.value, StatScreenPos.lives.value)
score_info = ('score', StatNumberMaps.score_num_map.value, StatScreenPos.score.value)
ring_info = ('rings', StatNumberMaps.ring_num_map.value, StatScreenPos.rings.value)

def reset_stats():
    print('Reseting Stats for next Training Session')
    global curr_rings, curr_score, curr_lives, curr_act, force_update
    curr_rings = 0
    curr_score = 0
    curr_lives = 3
    force_update = True
# ______________________________________________________________________________
def get_core_stats():
    global force_update
    while True:
        lives = deepcopy(curr_lives)
        rings = deepcopy(curr_rings)
        score = deepcopy(curr_score)
        act = deepcopy(curr_act)

        validate_lives(grab_stat(live_info))
        validate_score(grab_stat(score_info))
        validate_rings(grab_stat(ring_info))
        validate_act()

        detect_change = lives != curr_lives or rings != curr_rings or score != curr_score or act != curr_act
        if detect_change or force_update:
            trainingdriver.gui_func_qu.put('Update Texts')
            if force_update:
                force_update = False

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
    act_b_status = grab_stat(('Bact', StatNumberMaps.act_b_map.value, StatScreenPos.act_b.value))
    act_e_status = grab_stat(('Eact', StatNumberMaps.act_e_map.value, StatScreenPos.act_e.value))

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

    if grab_stat(ring_info) == fring_str and \
       grab_stat(score_info) == fscore_str and \
       grab_stat(live_info) == flives_str:

        training_start = False
    else:
        training_start = True

    return training_start
# _____________________________________________________________________________
# Function responsible for finiding out if the game is at the start screen
#
# Returns:
#        at_start_screen: a boolean variable that tells wheather the game is at
#                         the start screen
def isAtStartScreen():
    global at_start_screen

    if grab_stat(('ss', StatNumberMaps.start_screen_map.value, StatScreenPos.start_game.value)) == 'Go':
        at_start_screen = True
    else:
        at_start_screen = False

    return at_start_screen