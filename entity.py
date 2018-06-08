
import action_handler
import brain
class Entity:

    def __init__(self, act_list = [], parents = None):

        self.action_list = act_list
        self.fitness = 0
        self.generation = 0
        self.parents = parents
        self.alive = True


    def isAlive(self):

        if brain.curr_lives  == 0:
            self.Alive = False

        return self.alive

    def play_game(self):

        if self.isAlive():
             action_handler.gen_action_driver(self)
        else:
            print(f'A dead entity cannot play')

    def isAlive(self):
        return self.alive

    def died(self):
        self.alive = False

    def resurrect(self):

        self.Alive = True
