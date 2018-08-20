from src.gdmodules import gdr
from PIL import ImageGrab
import os

from src.enumval import StatScreenPos
# The current Postion and Num Map is for getting rings from my setup
snap_location = StatScreenPos.rings.value
snap_num_map = {}

# Enter Path name where you would like your test images stored
path_name = "images"
pic_name = "fullscreen"
def main():

    curr_box = [snap_location[0], snap_location[1], snap_location[2], snap_location[3]]

    print(curr_box)
    curr_box[0] -= 0
    curr_box[2] -= 0

    print(curr_box)
    image = ImageGrab.grab(curr_box)

    total = gdr.calc_num_id(num_image=image, num_map=snap_num_map)

    print(f'The pixel total from the calcluation is: {total}')

    if not os.path.isdir(path_name):
        os.mkdir(path_name)

    image.save(f'{path_name}/{pic_name}.png')


if __name__ == '__main__':
    main()
