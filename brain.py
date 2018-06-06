
import eyes
import time

curr_rings = 0
curr_score = 0
game_started = False


def validate_score(score):
    global curr_score

    if score == 'Could not obtain score':
        return curr_score
    elif int(score)%100 != 0 or int(score) == 0:
        return curr_score
    elif int(score) < int(curr_score):
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

def gameStarted():

    global game_started

    if game_started == False:

        if eyes.score_grab() != 'Could not obtain score' and eyes.ring_grab() != 'Could not obtain ring count':

            game_started = True

    return game_started
