from ..enumval import ActionName
from ..gdmodules import gdv
from .. import buttonpress as bp

# ______________________________________________________________________________
#   Action is an object that represent a single action executed by the computer
# during a session of Sonic 3 and Knukles
# Each Action have the following attributes to them:
#   action:      the string or list of strings, from the enumerated action_name
#                class, that contain the buttons need when executing an
#                action_name
#
#   delay:       The time that is required in between pressing and releasing
#                the button for an action to be preformed. Also can be used to
#                represent the time need to execute a particular action
#
#   ring_count:  The ring_count that is recorded during the execution of the
#                action
#
#   score_count: The score_count that is recorded during the execution of the
#                action
#
#   lives_count: The lives_count that is recorded during the execution of the
#                action
#
#   act:         The act that is recorded during the execution of the action
#
#   mutation:    The rate in which an action will change to a diffrent action
#                during the repoduction phase
# ______________________________________________________________________________

class Action:
    # __________________________________________________________________________
    def __init__(self, action, delay, mutation=0.5):
        self.action = action
        self.delay = delay
        self.mutation = mutation

        self.ring_count = 0
        self.score_count = 0
        self.lives_count = 0
        self.act = ''

    # __________________________________________________________________________
    def __str__(self):
        return f"""
        Action:                       {self.action}
        Mutation Chance:              {self.mutation}
                                                     """

    # __________________________________________________________________________
    # Function for setting the core stats of the action object during execution
    def set_core_stats(self):
        self.ring_count = gdv.curr_rings
        self.score_count = gdv.curr_score
        self.lives_count = gdv.curr_lives
        self.act = gdv.curr_act

    # __________________________________________________________________________
    # The Function that execute the action through keyboard presses
    def execute_action(self):

        # Execution instructions for spindash
        if self.action == ActionName.spindash:
            bp.spindash(self.action.value, self.delay)

        # Execution instructions for jump_shield
        elif self.action == ActionName.jump_shield:
            bp.jump_shield(self.action.value, self.delay)

        # Execution instructions for jump_right or jump_left
        elif isinstance(self.action.value, list):
            bp.jump_left_or_right(self.action.value, self.delay)
        # Execution instructions for every other action
        else:
            bp.general_action(self.action.value, self.delay)

        # Set stats after execution is complete
        self.set_core_stats()

# ______________________________________________________________________________
# --------------------Getter methods for Action attributes---------------------
    def getAction(self):
        return self.action

    def getDelay(self):
        return self.delay

    def getRingCount(self):
        return self.ring_count

    def getScoreCount(self):
        return self.score_count

    def getLivesCount(self):
        return self.lives_count

    def getAct(self):
        return self.act

    def getMutation(self):
        return self.mutation

# -------------------Setter methods for Action attributes----------------------
    def setAction(self, action):
        self.action = action

    def setDelay(self, delay):
        self.delay = delay

    def setRingCount(self, ring):
        self.ring_count = ring

    def setScoreCount(self, score):
        self.score_count = score

    def setLivesCount(self, lives):
        self.lives_count = lives

    def setAct(self, act):
        self.act = act

    def setMutation(self, mutation):
        self.mutation = mutation
