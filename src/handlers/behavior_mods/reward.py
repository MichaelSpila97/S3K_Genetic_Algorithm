
def ringsOrScoreIncreased(curr_rings, curr_score, prev_rings, prev_score):
    return prev_rings < curr_rings or \
           prev_score < curr_score

def livesIncreased(curr_lives, prev_lives):
    return curr_lives > prev_lives

def completedAct(curr_act, allow_reward):
    return curr_act == 'Act 1 End' and \
           allow_reward is True

def completedZone(curr_act, allow_reward):
    return curr_act == 'Act 2 End' and \
           allow_reward is True

def startedAct(curr_act, allow_reward):
    return curr_act == 'Act 1' or \
           curr_act == 'Act 2' and \
           allow_reward is False
