from PIL import ImageGrab
from PIL import Image
from PIL import ImageStat

from enum import Enum

import os
import time

class Static_Obj_Pos(Enum):
    #Fixed:
    ones_sec = (604,125,621,163)
    min_digit = (496,125,513,163)
    tens_sec = (568,125,585,163)

    #subtract x1 and x2 by 36 to move to next num pos
    score = (712,47, 729, 85)
    rings = (604, 202, 621, 241)

    #needs diffrent method
    lives = (500,101,528,1045)

def update_core_stats(root, labels):

    labels[0].configure (text = score_grab())
    labels[1].configure (text = ring_grab())

    root.after('500', update_core_stats,root, labels)


def score_grab():
    #print('Grabbing score')
    score_num_map = {'385':0, '367': 1,'444':2,'380':3,'545':4,
    '425': 5,'460': 6,'350': 7,'475':8,'455': 9}

    score_box = Static_Obj_Pos.score.value

    score_total = calc_num_total(score_num_map, score_box)

    if score_total == None:
        #print(f'Could not obtain score')
        return('Could not obtain score')
    else:
        #print(f'Current Score: {score_total}')
        return(score_total)

def ring_grab():
    #print('Grabbing rings')

    ring_num_map = {'402':0, '376': 1,'456':2,'388':3,
    '557':4,'428': 5,'468': 6,'359': 7,'483':8,'458': 9}

    ring_box = Static_Obj_Pos.rings.value

    ring_total = calc_num_total(ring_num_map, ring_box)

    if ring_total == None:
        #print(f'Could not obtain ring count')
        return('Could not obtain ring count')
    else:
        #print(f'Current ring count: {ring_total}')
        return(ring_total)

def calc_num_total(num_map, box):
    current_place = 1
    total = 0
    num_id = 0
    curr_box = [box[0], box[1],box[2],box[3]]

    while True:
        num_image = ImageGrab.grab(curr_box)
        num_id = calc_num_id(num_image)
        num_id = num_map.get(str(num_id))


        if num_id == None:
            break

        else:
            total = num_id *current_place + total
            current_place = current_place *10


        curr_box[0] = curr_box[0] - 36
        curr_box[2] = curr_box[2] - 36

    #print(total)
    #print(current_place)

    if total == 0 and current_place == 1:
        return(None)
    else:
        return(total)

def calc_num_id(im):
    pixel = list(im.getdata());
    pixtot = 0
    for i in pixel:
        if  i[0] == 224 and i[1] == 224 and i[2]==225:
            pixtot = pixtot + 1

    #print(pixtot)
    return pixtot





#time_num_map = {'385':0, '367': 1,'445':2,'375':3,'545':4,
#'423': 5,'460': 6,'356': 7,'475':8,'450': 9}

#box = Static_Obj_Pos.score
#print(box)

#box.value[0] = box.value[0] - 72
#box.value[2] = box.value[2] - 72

#im = ImageGrab.grab(box.value);
#im.save(os.getcwd() + '\\Snaps\\Score_num\\num_A5.png','PNG')
#im = Image.open(os.getcwd() + '\\Snaps\\numA9.png')

#pixel = list(im.getdata());
#pixtot = 0;
#print(pixel[0])
#out = ImageStat.Stat(im)
#print("This is out: ", pixel)

#for i in pixel:
    #if  i[0] == 224 and i[1] == 224 and i[2]==225:
        #print("hi")
        #pixtot = pixtot + 1


#print("Score num 5:" ,pixtot)
#print(pixtot == num_map['5'])
