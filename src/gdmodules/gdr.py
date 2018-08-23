from PIL import ImageGrab
from src.handlers import window_handler as wh

# ______________________________________________________________________________
#   Collection of functions responsible for the retrival of data from the game
# through screenshots and pixel addition
# ______________________________________________________________________________

# The function that parses out the info list for the calc_num_total function and
# for the return value when no data was found
#
# Info list:
#           [0]: Name of Statistic
#           [1]: The Number Map
#           [2]: Statisitic position on screen
def grab_stat(info):

    stat_total = calc_num_total(num_map=info[1], pos_box=info[2])

    if stat_total is None:
        return(f'Could not obtain {info[0]}')
    else:
        return stat_total

# ------------------------Number identification methods--------------------------

# ______________________________________________________________________________
#   The function that obtains and translate the screenshots of the in game
# statistics
# Passes:
#       num_map: The dictionary that contains the pixel additions totals
#                and the values which they map to
#       box:     The box that defines the on screen postion
#                of a in game statistic
# Returns:
#       total: if there was value obtained from the screenshot
#       none:  if nothing was obtained from the screenshot
def calc_num_total(num_map, pos_box):

    # The number place of the current screenshot
    numbers_place = 1

    # The grand total of the in game statistics when screen reading is complete
    total = 0

    # The calculated number id from the pixel calculation
    num_id = 0

    # The number that the num_id maps to in the number map
    num = 0

    # The distance in pixel between each digit of an on screen statistic
    distance_between = 16

    # Adjust x and y position of in game statists if the game window was moved
    # from its initial position
    x_pad, y_pad = wh.adjust_box()
    curr_box = [pos_box[0] + x_pad, pos_box[1] + y_pad, pos_box[2] + x_pad, pos_box[3] + y_pad]

    while True:

        # Takes Screenshot
        num_image = ImageGrab.grab(curr_box)

        # Calculated the number id
        num_id = calc_num_id(num_image, num_map)

        # Retrive the number in the num_map that maps to the num_id
        # Will be none if nothing maps to the num_id
        num = num_map.get(str(num_id))

        # If nothing can be read in then either obtained faulty screenshot
        # or has read in the full in game statistic
        if num is None:
            break

        #   Calulates the total of the number and increases the current places
        # to the next number place in line
        elif isinstance(num, int):
            total = (num * numbers_place) + total
            numbers_place = numbers_place * 10

        # Adjust boxes for next number to be screenshoted
        curr_box[0] = curr_box[0] - distance_between
        curr_box[2] = curr_box[2] - distance_between

    nothing_was_read_in = total == 0 and numbers_place == 1
    if nothing_was_read_in:
        return None
    else:
        return total
# ______________________________________________________________________________
#       Function that calculated the num_id used to identify what number
# a screenshot represents
# Passes:
#       num_image: The screenshot of the particular number that needs to be identified
#       num_map:   The dictionary that contains the pixel additions totals and
#                  the values which they map to
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
