import time
import gdr
import Test_Driver
from copy import deepcopy

# ______________________________________________________________________________
#        This contains the collection of funciton that validate and stores the
#  core in game statistic that is used by the Aciton objects
# ______________________________________________________________________________
# Global Variables used to keep track of current in game values
curr_rings = 0
curr_score = 0
curr_lives = 3
curr_act = ''

# game_started = False

# ______________________________________________________________________________
def get_core_stats():
    while True:
        lives = deepcopy(curr_lives)
        rings = deepcopy(curr_rings)
        score = deepcopy(curr_score)
        act = deepcopy(curr_act)

        validate_lives(gdr.live_grab())
        validate_score(gdr.score_grab())
        validate_rings(gdr.ring_grab())
        validate_act()

        detect_change = lives != curr_lives or rings != curr_rings or score != curr_score or act != curr_act
        if detect_change:
            Test_Driver.gui_func_qu.put('Update Texts')
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

    if rings == 'Could not obtain ring count':
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

    if lives == 'Could not obtain lives count':
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
    act_b_status = gdr.act_beginning_grab()
    act_e_status = gdr.act_end_grab()

    act_b_fail_str = 'Could not obtain the beginning of the act'
    act_e_fail_str = 'Could not obtain the end of the act'

    if act_b_status != act_b_fail_str:
        curr_act = f'Act {act_b_status}'

    elif act_e_status != act_e_fail_str:
        curr_act = f'Act {act_e_status} End'

    elif curr_act == 'Act 2 End':
        curr_act = f'Transitioning to next Zone...'

    return curr_act
# _____________________________________________________________________________
# returns the global variable that represented weather the game has started
# Method not usable in current state
# def gameStarted():

    # global game_started

    # if game_started == False:

    # if  curr_rings != -1 and curr_score != -1 and curr_lives != -1:
    # print('game has started')
    # game_started = True

    # return game_started
