import gdr
import time

#_______________________________________________________________________________________________________________________________
#GDV(Game Data Validator)
#        This contains the collection of funciton that validate and stores the
#  core in game statistic that is used by the Aciton objects
#_______________________________________________________________________________________________________________________________   

#Global Variables used to keep track of current in game values
curr_rings = 0
curr_score = 0
curr_lives = 3
curr_act = ''

#game_started = False

#_______________________________________________________________________________________________________________________________
#Wrapper Function used to update the global varibles ever 0.1 seconded
def get_core_stats():
    while True:
        validate_lives(eyes.live_grab())
        validate_score(eyes.score_grab())
        validate_rings(eyes.ring_grab())
        validate_act()

        time.sleep(0.1)
#_______________________________________________________________________________________________________________________________
#Determine wheather the incoming score count is valid
#Passes:
#       score: the incoming score count
#
#Returns:
#       curr_score: the global variable of the score count
def validate_score(score):
    global curr_score

    if score == 'Could not obtain score':
        return curr_score

    #Score must be multiple of 10 or equal 0
    elif int(score)%10 != 0 or int(score) == 0:
        return curr_score

    else:
        curr_score = int(score)
        return curr_score
#_______________________________________________________________________________________________________________________________
#Determine wheather the incoming ring count is valid
#Passes:
#       rings: the incoming ring count
#
#Returns:
#       curr_rings: the global variable of the ring count
def validate_rings(rings):
    global curr_rings

    if rings == 'Could not obtain ring count':
        return curr_rings

    #ring cannot decrease to a non zero value
    elif int(rings) < curr_rings and int(rings) != 0:
        return curr_rings

    #rings cannot exceed over 999
    elif int(rings) > 999:
        return curr_rings

    else:
        curr_rings = int(rings)
        return curr_rings
#_______________________________________________________________________________________________________________________________
#Determine wheather the incoming live count is valid
#Passes:
#       lives: the incoming lives count
#
#Returns:
#       curr_lives: the global variable of the lives
def validate_lives(lives):
    global curr_lives

    if lives == 'Could not obtain lives count':
        return curr_lives

    #lives should not increase or decreases more than once at a time
    #Ex: lives 3 -> 2 or 3->4 is good
    #    lives 3 -> 0 or 3 -> 7 not good
    elif lives > curr_lives + 1 or lives < curr_lives - 1:
        return curr_lives

    else:
        curr_lives = int(lives)
        return curr_lives
#_______________________________________________________________________________________________________________________________
#Determine wheather the act has begun or ended
#Returns:
#        curr_act: the global variable that represent the act status
def validate_act():
    global curr_act
    act_b_status = eyes.act_beginning_grab()
    act_e_status = eyes.act_end_grab()

    if act_b_status != 'Could not obtain the beginning of the act':
        curr_act = f'Act {act_b_status}'

    elif act_e_status != 'Could not obtain the end of the act':
        curr_act = f'Act {act_e_status} End'

    return curr_act
#_______________________________________________________________________________________________________________________________
#Determines wheater the gmae has started
#returns the global variable that represented weather the game has started
#Method not usable in current state
#def gameStarted():

    #global game_started

    #if game_started == False:

        #if  curr_rings != -1 and curr_score != -1 and curr_lives != -1:
            #print('game has started')
            #game_started = True

    #return game_started
