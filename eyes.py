from PIL import ImageGrab
from PIL import Image
from PIL import ImageStat

from enum import Enum

import os
import time
import brain

class Static_Obj_Pos(Enum):
    #Fixed:
    ones_sec = (604,125,621,163)
    min_digit = (496,125,513,163)
    tens_sec = (568,125,585,163)

    #subtract x1 and x2 by 36 to move to next num pos
    score = (712,47, 729, 85)
    rings = (604, 202, 621, 241)

    lives = (501,1011,518,1044)

    act_b = (1410,774,1449,813)
    act_e = (1374,290,1413,329)

def score_grab():

    score_num_map = {'385':0, '367': 1,'444':2,'380':3,'545':4,
    '425': 5,'460': 6,'350': 7,'475':8,'455': 9}

    score_box = Static_Obj_Pos.score.value

    score_total = calc_num_total(score_num_map, score_box)

    if score_total == None:
        return('Could not obtain score')
    else:
        return(score_total)

def ring_grab():

    ring_num_map = {'402':0, '376': 1,'456':2,'388':3,
    '557':4,'428': 5,'468': 6,'359': 7,'483':8,'458': 9}

    ring_box = Static_Obj_Pos.rings.value

    ring_total = calc_num_total(ring_num_map, ring_box)

    if ring_total == None:
        return('Could not obtain ring count')
    else:
        return(ring_total)


def live_grab():
    live_num_map = {'152': 0, '191': 1, '141': [2,7], '137' : 3, '253': 4, '157': 5, '177': 6, '197': 8, '181': 9}

    lives_box = Static_Obj_Pos.lives.value

    lives_total = calc_num_total(live_num_map, lives_box)

    if lives_total == None:
        return('Could not obtain lives count')
    else:
        return(lives_total)

def act_beginning_grab():
    act_beg_map = {'739': 1, '638': 2}

    act_beg_box = Static_Obj_Pos.act_b.value

    act_beg_total = calc_num_total(act_beg_map, act_beg_box)

    if act_beg_total == None:
        return('Could not obtain the beginning of the act')
    else:
        return(act_beg_total)

def act_end_grab():
    act_end_map = {'734': 1, '638': 2}

    act_end_box = Static_Obj_Pos.act_e.value

    act_end_total = calc_num_total(act_end_map, act_end_box)

    if act_end_total == None:
        return('Could not obtain the end of the act')
    else:
        return(act_end_total)

def calc_num_total(num_map, box):
    current_place = 1
    total = 0
    num_id = 0
    num = 0
    curr_box = [box[0], box[1],box[2],box[3]]

    while True:

        num_image = ImageGrab.grab(curr_box)

        num_id = count_decider(num_image, num_map)

        num = num_map.get(str(num_id))

        if isinstance(num, list):
            num = check_if_two_or_seven(num, current_place)

        if num == None:
            break

        elif isinstance(num, int):
            total = (num *current_place) + total
            current_place = current_place *10

        curr_box[0] = curr_box[0] - 36
        curr_box[2] = curr_box[2] - 36

    if total == 0 and current_place == 1:
        return(None)
    else:
        return(total)


def count_decider(num_image , num_map):
    num = 0

    if num_map.get('152') == 0:
        num = calc_live_num_id(num_image)

    else:
        num = calc_num_id(num_image)

    return num

def check_if_two_or_seven(num, current_place):
    live_num = 0

    if  current_place == 1:
        live_num = brain.curr_lives%10

    elif current_place == 10:
        live_num = brain.curr_lives/10

    if live_num in range (5,10):
        live_num = num[1]
    else:
        live_num = num[0]

    return live_num

def calc_num_id(im):
    pixel = list(im.getdata());
    pixtot = 0

    for i in pixel:
        if  (i[0] == 224 and i[1] == 224 and i[2]==225) or (i[0] == 160 and i[1] == 160 and i[2]==225):
            pixtot = pixtot + 1

    return pixtot

def calc_live_num_id(im):
    pixel = list(im.getdata());
    pixtot = 0

    for i in pixel:
        if  i[0] == 224 and i[1] == 224 and i[2]==225:
            pixtot = pixtot + 1

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
