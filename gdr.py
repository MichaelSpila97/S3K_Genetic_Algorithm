from PIL import ImageGrab
from enum import Enum

import gdv

# ______________________________________________________________________________
#   Collection of functions responsible for the retrival of data from the game
# through screenshots and pixel addition
# ______________________________________________________________________________

# The enumerated x and y coordiates for where each in game value is located on screen
# Only applicable to a screen using 1920x1080 resolution
class Static_Obj_Pos(Enum):

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


# --------------------------------Grabber Methods-------------------------
# General description:
#   Each grab method will get thier respective enum value from the Static_obj_Pos
# and send that enum value and its num map to the calc_num_total method. If a value returns
# the grab method will return that values. If nothing returns than each grabber method will
# return thier respective 'Could not get' string

# ______________________________________________________________________________
def score_grab():
    score_num_map = {'385': 0, '367': 1, '444': 2, '380': 3, '545': 4,
    '425': 5, '460': 6, '350': 7, '475': 8, '455': 9}

    score_box = Static_Obj_Pos.score.value

    score_total = calc_num_total(score_num_map, score_box)

    if score_total is None:
        return('Could not obtain score')
    else:
        return(score_total)
# _____________________________________________________________________________
def ring_grab():
    ring_num_map = {'402': 0, '376': 1, '456': 2, '388': 3,
    '557': 4, '428': 5, '468': 6, '359': 7, '483': 8, '458': 9}

    ring_box = Static_Obj_Pos.rings.value

    ring_total = calc_num_total(ring_num_map, ring_box)

    if ring_total is None:
        return('Could not obtain ring count')
    else:
        return(ring_total)
# _____________________________________________________________________________
def live_grab():
    live_num_map = {'152': 0, '191': 1, '141': [2, 7], '137': 3,
    '253': 4, '157': 5, '177': 6, '197': 8, '181': 9}

    lives_box = Static_Obj_Pos.lives.value

    lives_total = calc_num_total(live_num_map, lives_box)

    if lives_total is None:
        return('Could not obtain lives count')
    else:
        return(lives_total)
# ______________________________________________________________________________
def act_beginning_grab():
    act_beg_map = {'739': 1, '638': 2}

    act_beg_box = Static_Obj_Pos.act_b.value

    act_beg_total = calc_num_total(act_beg_map, act_beg_box)

    if act_beg_total is None:
        return('Could not obtain the beginning of the act')
    else:
        return(act_beg_total)
# ______________________________________________________________________________
def act_end_grab():
    act_end_map = {'734': 1, '638': 2}

    act_end_box = Static_Obj_Pos.act_e.value

    act_end_total = calc_num_total(act_end_map, act_end_box)

    if act_end_total is None:
        return('Could not obtain the end of the act')
    else:
        return(act_end_total)

# _____________________________________________________________________________
def start_game_grab():
    start_map = {'774': 'Go'}

    start_box = Static_Obj_Pos.start_game.value

    start = calc_num_total(start_map, start_box)

    if start is None:
        return('Not at Start Screen')
    else:
        return (start)

# ------------------------Number identification methods--------------------------

# ______________________________________________________________________________
#   The Function that calculates the total for any numeric in game value
# Passes:
#       num_map: The dictionary that contains the pixel additions totals
#                and the value 0-9 which they map to
#       box:     The box that defines where the screenshot will be taken
# Returns:
#       total: if there was value
#       none:  if nothing was nothing
def calc_num_total(num_map, box):

    numbers_place = 1
    total = 0
    num_id = 0
    num = 0
    curr_box = [box[0], box[1], box[2], box[3]]

    while True:

        # Screenshot
        num_image = ImageGrab.grab(curr_box)

        # Calculated the number id
        num_id = calc_num_id(num_image, num_map)

        # Retrive the number in the num_map that maps to the num_id
        # Will be none if nothing maps to the num_id
        num = num_map.get(str(num_id))

        #   Need to determine if two or seven if num_id pulls the list from the
        # the live num map since thier is no distince pixel addtion for two and
        # seven for lives
        if isinstance(num, list):
            num = check_if_two_or_seven(numbers_place)

        # Reaches end of number and will break
        if num is None:
            break

        elif num == 'Go':
            total = num
            break
        #   Calulates the total of the number and increases the current places
        # to the next number place in line
        elif isinstance(num, int):
            total = (num * numbers_place) + total
            numbers_place = numbers_place * 10

        # Adjust boxes for next number to be screenshotted
        curr_box[0] = curr_box[0] - 36
        curr_box[2] = curr_box[2] - 36

    if total == 0 and numbers_place == 1:
        return(None)
    else:
        return(total)
# ______________________________________________________________________________
#       Function that calculated the num_id used to identify what number
# a screenshot represents
# Passes:
#       num_image: The screenshot of the particular number that needs to be identified
#       num_map:   The dictionary that contains the pixel additions totals and
#                  the value 0-9 which they map to
#
# Returns:
#       result: the result of the calculation functions
def calc_num_id(num_image, num_map):

    image = list(num_image.getdata())
    result = 0

    for pixels in image:
        # If and else determines which types of pixels will be used in the calculations
        # Used for determining the screenshots for lives
        if num_map.get('152') == 0:
            if pixels[0] == 224 and pixels[1] == 224 and pixels[2] == 225:
                result = result + 1
        # Used for determining if the screenshot indicates the game is at the start screen
        elif num_map.get('774') == 'Go':
            if pixels[0] == 224 and pixels[1] == 0 and pixels[2] == 0:
                result = result + 1
        # Used for determing all other screenshots
        else:
            if pixels[0] == 224 and pixels[1] == 224 and pixels[2] == 225 or pixels[0] == 160 and pixels[1] == 160 and pixels[2] == 225:

                result = result + 1

    return result


# ______________________________________________________________________________
#   Function that determines weather to use two or seven in the lives num map
#   Determines through mod or int div the curr_lives from gdv by 10 and seeing
# if lives is closer to seven or two
#   Passes:
#          numbers_place: represents which numbers place the current digit belongs to
#   Returns:
#           2 if closer to 2 or 7 if closer to 7
def check_if_two_or_seven(numbers_place):
    live_num = 0
    if numbers_place == 1:
        live_num = gdv.curr_lives % 10

    elif numbers_place == 10:
        live_num = gdv.curr_lives // 10

    if live_num in range(5, 10):
        return 7
    else:
        return 2
# _______________________________________________________________________________
# time_num_map = {'385':0, '367': 1,'445':2,'375':3,'545':4,
# '423': 5,'460': 6,'356': 7,'475':8,'450': 9}
