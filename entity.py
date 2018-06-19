
import action_handler
import brain
class Entity:

    def __init__(self, act_list = [], parents = None):

        self.action_list = act_list
        self.fitness = 0
        self.generation = 0
        self.parents = parents
        self.alive = True

    def __str__(self):
        action_str = ''
        i = 0
        time = 0
        while i < len(self.action_list):
            time = time + self.action_list[i].getDelay()
            action_str =  action_str + f"""
Action: [{i}] {format(time, '.2f')} 
            {self.action_list[i]}\n"""
            i = i + 1
        return f"""{action_str}
        Entity Overall Stats:
                Fitness Score: {self.fitness}
                Generation: {self.generation}
                Parents to this Entity: {self.parents}
                Entity's Status: {self.alive}"""


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
        self.alive = True

    def getActionList(self):
        return self.action_list

    def getFitness(self):
        return self.fitness

    def getParents(self):
        return self.parents

    def setActionList(self, new_act_list):
        self.action_list = new_act_list

    def setFitness(self, new_fitness):
        self.fitness = new_fitness

    def setParents(self, new_parents):
        self.parents = new_parents
