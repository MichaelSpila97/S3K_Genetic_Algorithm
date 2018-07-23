
def isDefenseless(curr_rings, prev_rings):
    return curr_rings == 0 and prev_rings != 0

def ringsAreStagnating(time_wr, curr_rings, prev_rings):
    return time_wr >= 7 and curr_rings == prev_rings

def scoreIsStangnating(time_ws, curr_score, prev_score):
    return time_ws >= 60 and curr_score == prev_score

def lostLife(curr_lives, prev_lives, allowpenalty):
    return curr_lives < prev_lives and allowpenalty
