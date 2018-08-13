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

    #   X and Y coordinates for collection what the hud time is displaying
    #   Not in use since keeping track of the in game timer using screenshots
    # is very unreliable
    # ones_sec = (604,125,621,163)
    # min_digit = (496,125,513,163)
    # tens_sec = (568,125,585,163)

    # Position of the ones digit for each of the values bellow
    # subtract x1 and x2 by 36 to move to obtain other digits
    score = (712, 47, 729, 85)
    rings = (604, 202, 621, 241)
    lives = (501, 1011, 518, 1044)

    #   The boxes are postion for taking snaps that determine the begining of an act
    # and the end of an act
    act_b = (1410, 774, 1449, 813)
    act_e = (1374, 290, 1413, 329)

    #   Used for determining if you are at the start screen of the game. Not used in this version
    # since save states are used to load into the game
    start_game = (654, 929, 725, 962)

class StatNumberMaps(Enum):
    score_num_map = {'385': 0, '367': 1, '444': 2, '380': 3, '545': 4,
    '425': 5, '460': 6, '350': 7, '475': 8, '455': 9}

    ring_num_map = {'402': 0, '376': 1, '456': 2, '388': 3,
    '557': 4, '428': 5, '468': 6, '359': 7, '483': 8, '458': 9}

    live_num_map = {'152': 0, '191': 1, '141': [2, 7], '137': 3,
    '253': 4, '157': 5, '177': 6, '197': 8, '181': 9}

    #   The num maps are used to determine the begining of an act
    # and the end of an act
    act_b_map = {'739': 1, '638': 2}
    act_e_map = {'734': 1, '638': 2}

    #   Used for determining if you are at the start screen of the game. Not used in this version
    # since save states are used to load into the game
    start_screen_map = {'774': 'Go'}

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
