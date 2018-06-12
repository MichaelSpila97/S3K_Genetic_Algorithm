
import action_handler
import brain
class Entity:

    def __init__(self, act_list, parents = None):

        self.action_list = act_list
        self.fitness = 0
        self.generation = 0
        self.parents = parents
        self.alive = True

    def __str__(self):
        action_str = ''
        i = 0
        for x in self.action_list:
            action_str =  action_str + f"""
\033[1;31;40mAction: [{i}]
            {self.action_list[i]}\n"""
            i = i + 1
        return f"""{action_str}
        \033[1;35;40mEntity Overall Stats:
                \033[1;37;40mFitness Score: {self.fitness}
                \033[1;37;40mGeneration: {self.generation}
                \033[1;37;40mParents to this Entity: {self.parents}
                \033[1;37;40mEntity's Status: {self.alive}"""

    def isAlive(self):

        if brain.curr_lives  == 0:
            self.Alive = False

        return self.alive

    def play_game(self):
        print('playing game...')
        if self.isAlive():
            action_handler.action_driver(self)
        else:
            print(f'A dead entity cannot play')

    def isAlive(self):
        return self.alive

    def died(self):
        print(f'entity is dead')
        self.alive = False

    def resurrect(self):
        self.Alive = True
