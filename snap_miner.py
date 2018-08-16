from src.gdmodules import gdr
from PIL import ImageGrab
import os
# The current Postion and Num Map is for getting rings from my setup
snap_location = (604, 202, 621, 241)
snap_num_map = {'402': 0, '376': 1, '456': 2, '388': 3,
'557': 4, '428': 5, '468': 6, '359': 7, '483': 8, '458': 9}

# Enter Path name where you would like your test images stored
path_name = "images"
pic_name = "fullscreen"
def main():
    image = ImageGrab.grab()

    total = gdr.calc_num_id(num_image=image, num_map=snap_num_map)

    print(f'The pixel total from the calcluation is: {total}')

    if not os.path.isdir(path_name):
        os.mkdir(path_name)

    image.save(f'{path_name}/{pic_name}.png')


if __name__ == '__main__':
    main()
