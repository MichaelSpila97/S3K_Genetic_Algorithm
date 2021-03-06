
from ..handlers import action_handler
from ..buttonpress import load_state
# _______________________________________________________________________________________________________________________________
# Entity is an object that represent a single attempt by the computer to complete Sonic 3 and Knunkles
#
# Each Entity have the following attributes to them:
#     action_list: This is a list of the actions, represented by an action object,
#                  that an entity took during its attempt at the game
#     fitness:     This represent the fitness of an entity and is used to determine
#                  how easily the entity will be able to reproduce during reproduction
#     generation:  This represent the generation the entity belongs to
#     parents:     This is a list that contains the parents to the entity.
#                  Will be empty if the entity belongs to Gen 0
#     alive:       This represent the entity's living status.
#                  Used to stop entities run if it dies during the game
#     dnacap:      This is the number of action an entities is allowed to take
#                  before its in game attempt is over
#     master_ent:  The entity that is used to play out an action sequences that
#                  was evaluated as being the fittess set of actions from previous
#                  generations' play attempts.
# _______________________________________________________________________________________________________________________________

class Entity:

# _______________________________________________________________________________________________________________________________
    def __init__(self, name, act_list=None, parents=None, dna_cap=7):

        self.name = name
        self.action_list = act_list or []
        self.fitness = 0
        self.generation = 0
        self.parents = parents
        self.alive = True
        self.dnacap = dna_cap
        self.master_ent = None

# ______________________________________________________________________________________________________________________________
    def __str__(self):

        return f"""
        Entity {self.name} Overall Stats:
                Fitness Score: {self.fitness}
                Generation: {self.generation}
                Parents to this Entity: {self.parents}
                Entity's Status: {self.alive}
                """


# ______________________________________________________________________________________________________________________________
    # This function handles an entity's attempt at Sonic 3 & Knuckles
    def play_game(self):
        print(f'    {self.name} is Training....')
        if self.isAlive():
            load_state()

            # Master plays actions out first is it has been created
            if self.getMasterEntity() is not None:
                if self.getMasterEntity().getActionList() != []:
                    action_handler.master_driver(self.getMasterEntity())

            # Then if previous action were created those action will be played out
            if self.getActionList() != []:
                action_handler.replay_driver(self)

            # Else new action must be generated for this entity
            else:
                action_handler.generate_driver(self)
        else:
            print(f'    A dead entity cannot play')

        # For an entity that either prematurly died during the action generation step
        if len(self.getActionList()) != self.getDNACap():
            print('     Entity did not produce enough DNA\n     Giving Entity A Second Chace...')
            self.setActionList([])
            self.resurrect()
            self.play_game()
        print('')

# _____________________________________________________________________________________________________________________________
    # Getter for alive attribute
    def isAlive(self):
        return self.alive

# ______________________________________________________________________________________________________________________________
    # Sets alive variable to false if an entity died in game
    def died(self):
        print(f'    {self.name} is dead\n')
        self.alive = False

# ___________________________________________________________________________________________________________________________
    # Sets alive variable to true if  an enitity needs to reattempt the game
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

    def getDNACap(self):
        return self.dnacap

    def getMasterEntity(self):
        return self.master_ent

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

    def setDNACap(self, new_dnacap):
        self.dnacap = new_dnacap

    def setMasterEntity(self, new_masterentity):
        self.master_ent = new_masterentity
