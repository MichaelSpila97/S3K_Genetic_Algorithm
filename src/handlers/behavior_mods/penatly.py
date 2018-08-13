
def isDefenseless(curr_rings, prev_rings):
    return curr_rings == 0 and prev_rings != 0

def ringsAreStagnating(time_wr, curr_rings, prev_rings):
    return time_wr >= 1 and curr_rings == prev_rings

def lostLife(curr_lives, prev_lives, allowpenalty):
    return curr_lives < prev_lives and allowpenalty
