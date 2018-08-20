from enum import Enum

# -------------------------------------------------------------------------
#   This file contains the enumerated values used for capturing in game data
# and for the specfic button that are need to be pressed for an action to
# be preformed.
#
# Note: The current enum values for caputuring in game data is calibrated for
#       the steam version of Sonic 3 & Knuckles at 1920 x 1080 Fullscreen @
#       60 Hz. Unless you have this setup you will have to mine for the values
#       corresponding to your setup. The Snap_Miner tool and Paint.net may be of
#       use to you when mining for these values.
class StatScreenPos(Enum):

    # Position of the ones digit for each of the values bellow
    # subtract x1 and x2 by 36 to move to obtain other digits
    score = (211, 45, 224, 68)
    rings = (163, 114, 176, 137)
    lives = (117, 475, 130, 490)

    #   The boxes are postion for taking snaps that determine the begining of an act
    # and the end of an act
    act_b = (523, 370, 540, 387)
    act_e = (507, 155, 524, 172)

    #   Used for determining if you are at the start screen of the game. Not used in this version
    # since save states are used to load into the game
    start_game = (654, 929, 725, 962)

class StatNumberMaps(Enum):
    score_num_map = {'12106': 0, '5538': 1, '12170': 2, '9540': 3, '11780': 4,
    '8908': 5, '11374': 6, '4148': 7, '11196': 8, '10854': 9}

    ring_num_map = {'12310': 0, '5798': 1, '12546': 2, '9744': 3,
    '10458': 4, '9572': 5, '11578': 6, '4380': 7, '11400': 8, '11058': 9}

    live_num_map = {'260': 0, '-354': 1, '628': 2, '1448': 3,
    '892': 4, '-540': 5, '446': 6, '-1204': 7, '442': 8, '-386': 9}

    #   The num maps are used to determine the begining of an act
    # and the end of an act
    act_b_map = {'14630': 1, '10852': 2}
    act_e_map = {'14842': 1, '10892': 2}

class ActionName(Enum):
    move_left = 'left'
    move_right = 'right'
    press_down = 'down'
    press_up = 'up'
    jump_up = 'a'
    jump_right = ['right', 'a']
    jump_left = ['left', 'a']
    wait = ''
    spindash = ['down', 'a']
    jump_shield = ['a', 'a']
