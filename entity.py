
import action_handler

# _______________________________________________________________________________________________________________________________
# Entity is an object that represent a single attempt by the computer to complete Sonic 3 and Knunkles
# Each Entity have the following attributes to them:
#     action_list: This is a list of the actions, represented by an action object, that an entity took during its life
#     fitness:     This represent the fitness of an entity and is used to determine how easily the entity will be able to reproduce
#     generation:  This represent the generation the entity belongs to
#     parents:     This is a list that contains the parents to the entity. Will be empty if the entity belongs to Gen 0
#     alive:       This represent wheater the entity living status. Used to stop entities run if it dies during the game
# _______________________________________________________________________________________________________________________________

class Entity:

# _______________________________________________________________________________________________________________________________
    def __init__(self, name, act_list=None, parents=None):

        self.name = name
        self.action_list = act_list or []
        self.fitness = 0
        self.generation = 0
        self.parents = parents
        self.alive = True

# ______________________________________________________________________________________________________________________________
    def __str__(self):
        action_str = ''
        i = 0
        time = 0
        for i, action in enumerate(self.action_list):
            time = time + action.getDelay()
            action_str = action_str + f"""
Action: [{i}] {format(time, '.2f')}
              {self.action_list[i]}\n"""

        return f"""
        Entity {self.name} Overall Stats:
                Fitness Score: {self.fitness}
                Generation: {self.generation}
                Parents to this Entity: {self.parents}
                Entity's Status: {self.alive}
                Actions:
                         {action_str}        """

# ______________________________________________________________________________________________________________________________
    # This function directs living entities to attempt Sonic 3 and Knuckles
    def play_game(self):
        print(f'{self.name} is Training')
        if self.isAlive():
            action_handler.action_driver(self)
        else:
            print(f'A dead entity cannot play')

# _____________________________________________________________________________________________________________________________
    # Getter for alive attribute
    def isAlive(self):
        return self.alive

# ______________________________________________________________________________________________________________________________
    # Sets alive variable to false if it died in game
    def died(self):
        print(f'{self.name} is dead')
        self.alive = False

# ___________________________________________________________________________________________________________________________
    # Sets alive variable to true if enitites needs to reattempt the game
    def resurrect(self):
        self.alive = True

# -----------------Getter methods for all Entity attributes(except alive)---------------
    def getActionList(self):
        return self.action_list

    def getName(self):
        return self.name

    def getGeneration(self):
        return self.generation

    def getFitness(self):
        return self.fitness

    def getParents(self):
        return self.parents

# ------------------Getter methods for all Entity attributes(except alive)----------------------------------------------
    def setActionList(self, new_act_list):
        self.action_list = new_act_list

    def setFitness(self, new_fitness):
        self.fitness = new_fitness

    def setParents(self, new_parents):
        self.parents = new_parents

    def setName(self, new_name):
        self.name = new_name

    def setGeneration(self, new_gen):
        self.generation = new_gen
