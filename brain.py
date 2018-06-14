
import eyes
import time

curr_rings = 0
curr_score = 0
curr_lives = 3
curr_act = ''

game_started = False

def get_core_stats():
    while True:
        validate_lives(eyes.live_grab())
        validate_score(eyes.score_grab())
        validate_rings(eyes.ring_grab())
        validate_act()

        time.sleep(0.1)

def validate_score(score):
    global curr_score

    if score == 'Could not obtain score':
        return curr_score

    elif int(score)%10 != 0 or int(score) == 0:
        return curr_score
    else:
        curr_score = int(score)
        return curr_score

def validate_rings(rings):
    global curr_rings

    if rings == 'Could not obtain ring count':
        return curr_rings

    elif int(rings) < curr_rings and int(rings) != 0:
        return curr_rings

    elif int(rings) > 999:
        return curr_rings

    else:
        curr_rings = int(rings)
        return curr_rings

def validate_lives(lives):
    global curr_lives

    if lives == 'Could not obtain lives count':
        return curr_lives

    elif lives > curr_lives + 1:
        return curr_lives

    else:
        curr_lives = int(lives)
        return curr_lives

def validate_act():
    global curr_act
    act_b_status = eyes.act_beginning_grab()
    act_e_status = eyes.act_end_grab()

    if act_b_status != 'Could not obtain the beginning of the act':
        curr_act = f'Act {act_b_status}'

    elif act_e_status != 'Could not obtain the end of the act':
        curr_act = f'Act {act_e_status} End'

    return curr_act

def gameStarted():

    global game_started

    if game_started == False:

        if  curr_rings != -1 and curr_score != -1 and curr_lives != -1:
            print('game has started')
            game_started = True

    return game_started
