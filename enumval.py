from enum import Enum

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

    act_b = (1410, 774, 1449, 813)
    act_e = (1374, 290, 1413, 329)

    start_game = (654, 929, 725, 962)

class StatNumberMaps(Enum):
    score_num_map = {'385': 0, '367': 1, '444': 2, '380': 3, '545': 4,
    '425': 5, '460': 6, '350': 7, '475': 8, '455': 9}

    ring_num_map = {'402': 0, '376': 1, '456': 2, '388': 3,
    '557': 4, '428': 5, '468': 6, '359': 7, '483': 8, '458': 9}

    live_num_map = {'152': 0, '191': 1, '141': [2, 7], '137': 3,
    '253': 4, '157': 5, '177': 6, '197': 8, '181': 9}

    act_b_map = {'739': 1, '638': 2}

    act_e_map = {'734': 1, '638': 2}

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
