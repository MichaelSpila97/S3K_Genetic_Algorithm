from PIL import ImageGrab

from ..gdmodules import gdv

# ______________________________________________________________________________
#   Collection of functions responsible for the retrival of data from the game
# through screenshots and pixel addition
# ______________________________________________________________________________


# --------------------------------Grabber Methods-------------------------
# General description:
#   Each grab method will get thier respective enum value from the Static_obj_Pos
# and send that enum value and its num map to the calc_num_total method. If a value returns
# the grab method will return that values. If nothing returns than each grabber method will
# return thier respective 'Could not get' string

# ______________________________________________________________________________

def grab_stat(info):

    stat_total = calc_num_total(num_map=info[1], pos_box=info[2])

    if stat_total is None:
        return(f'Could not obtain {info[0]}')
    else:
        return stat_total

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
def calc_num_total(num_map, pos_box):

    numbers_place = 1
    total = 0
    num_id = 0
    num = 0
    curr_box = [pos_box[0], pos_box[1], pos_box[2], pos_box[3]]

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
        # Used for determining the screenshots for live
        if num_map.get('152') == 0:
            if pixels == (224, 224, 225):
                result = result + 1

        # Used for determining if the screenshot indicates the game is at the start screen
        elif num_map.get('774') == 'Go':
            if pixels == (224, 0, 0):
                result = result + 1

        # Used for determing all other screenshots
        else:
            if pixels == (224, 224, 225) or pixels == (160, 160, 225):
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
