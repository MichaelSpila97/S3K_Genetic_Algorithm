from PIL import ImageGrab
from src.handlers import window_handler as wh

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
    distance_between = 16
    x_pad, y_pad = adjust_box()

    curr_box = [pos_box[0] + x_pad, pos_box[1] + y_pad, pos_box[2] + x_pad, pos_box[3] + y_pad]

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

        # Reaches end of number and will break
        if num is None:
            break

        #   Calulates the total of the number and increases the current places
        # to the next number place in line
        elif isinstance(num, int):
            total = (num * numbers_place) + total
            numbers_place = numbers_place * 10

        # Adjust boxes for next number to be screenshotted
        curr_box[0] = curr_box[0] - distance_between
        curr_box[2] = curr_box[2] - distance_between

    if total == 0 and numbers_place == 1:
        return None
    else:
        return total
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

    for count, pixels in enumerate(image):

        if pixels == (224, 224, 225) or pixels == (160, 160, 225):
            row = count % 14
            col = count - 14 * row

            pix_val = row + col
            result += pix_val

    return result


def adjust_box():
    if wh.win_pos != wh.orig_win_pos:
        x_pad = wh.win_pos[0] - wh.orig_win_pos[0]
        y_pad = wh.win_pos[1] - wh.orig_win_pos[1]

        return x_pad, y_pad
    return 0, 0
