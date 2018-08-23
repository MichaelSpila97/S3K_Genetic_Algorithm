from copy import deepcopy
from random import shuffle, choice, seed
from ...classes import action, entity
from ...handlers import action_handler as ah, filehandler

last_stag_gen = -1
#  Function assigns entities to one of the four mating pools based on thier
#  fitness score.
# Also used to determine if a master has been created.
# Passes:
#        generation: List of entities that belong to a generation
#
# Returns:
#        mating_pool: List of the four mating pools with the entities in their
#                     respective pools
#
#        entities: the master entity
def assign_entities_to_pools(generation):
    mating_pools = [[[2, 5]],
                    [[2, 15]],
                    [[2, 30]],
                    [[2, 50]]]

    for entities in generation:
        ent_fitness = entities.getFitness() * 100
        if ent_fitness < 30:
            # Removes least fit entity if the mating pool is full and
            # the incoming entity has a greater fitness score than the
            # least fit entity
            if len(mating_pools[0]) == 6:
                least_fit_ent = mating_pools[0][0][0]
                if least_fit_ent < ent_fitness:
                    mating_pools[0][0] = [entities.getFitness(), entities]
            else:
                mating_pools[0].append([entities.getFitness(), entities])
            mating_pools[0].sort(key=lambda x: x[0])

        elif ent_fitness >= 30 and ent_fitness < 50:
            mating_pools[1].append([entities.getFitness(), entities])
            mating_pools[1].sort(key=lambda x: x[0])

        elif ent_fitness >= 50 and ent_fitness < 70:
            mating_pools[2].append([entities.getFitness(), entities])
            mating_pools[2].sort(key=lambda x: x[0])

        elif ent_fitness >= 70 and ent_fitness < 98:
            mating_pools[3].append([entities.getFitness(), entities])
            mating_pools[3].sort(key=lambda x: x[0])

        # Master entity has been found
        elif ent_fitness >= 98:
            return entities

    return mating_pools

# Functions that adds empty mating pool's mating percent to occupied mating pools
#
# Passes:
#        mating_pool: List of the four mating pools with the entities in their
#                     respective pools
#
# Returns:
#       mating_pool: Same as passes but the mating percent values have been moved to
#                    to occupied pools
def configure_mating_percents(mating_pool):

    prev_pop_pool = False
    unused_mating_percent = 0

    for count, pools in enumerate(mating_pool):
        per_place = len(pools) - 1
        if per_place == 0:
            unused_mating_percent += pools[per_place][1]
            pools[per_place][1] = 0
        elif per_place != 0:
            prev_pop_pool = count

        if prev_pop_pool is not False:
            per_place = len(mating_pool[prev_pop_pool]) - 1
            mating_pool[prev_pop_pool][per_place][1] += unused_mating_percent
            unused_mating_percent = 0

    return mating_pool

#   Fuction responsible faciliting the choosing of parents and creation of their
# offsprings
#
# Passes:
#           mating_pool: List of the four mating pools with the entities in their
#                        respective pools
#
# Returns:
#           new_generation: The new generation created from the mating of parent entities
def choose_and_mate(mating_pool, gen_num, num_of_entities):
    choose_pool = choose_pool_creater(mating_pool)

    new_generation = []
    isStag = stagnation_checker(gen_num)

    while len(new_generation) < num_of_entities:
        parents = choose_parents(choose_pool)
        new_generation.append(create_new_entity(parents, gen_num, len(new_generation) + 1, isStag))

    return new_generation
#   Fuction responsible for assigning the created master as the new master entity
#   of the next generation. The next generation will also have no action in their
#   action list as result of the master being created.
#
# Passes:
#           master:          The entities whose fitness score is greater than or equal
#                            to 98%
#           gen_num:         The generation number of the current generation
#           num_of_entities: The number of entities that will be created for the next
#                            generation
#
# Returns:
#           new_generation: The new generation created from the creation of the master entity
def assign_master(master, gen_num, num_of_entities):

    new_generation = []

    master_dna = master.getActionList()

    # Adds previous master DNA to new master DNA to create the new master
    if master.getMasterEntity() is not None:
        master_dna = master.getMasterEntity().getActionList() + master_dna

    master.setActionList(master_dna)

    # Creates new master generation
    while len(new_generation) < num_of_entities:
        empty_entity = entity.Entity(name=f'G{gen_num + 1}E{len(new_generation)}')
        empty_entity.setMasterEntity(master)
        empty_entity.setGeneration(gen_num + 1)
        new_generation.append(empty_entity)

    return new_generation
#   Fuction responsible for choosing the parents that will mate and create a new entity
#
# Passes:
#           choose_pool: list that contains multiple copies of pontential parents from the current
#                        generation. The list will allways be length 100.
#
# Returns:
#           par_list: the list of the two parents that will mate
def choose_parents(choose_pool):
    par_list = []
    while len(par_list) < 2:
        shuffle(choose_pool)
        new_parent = choice(choose_pool)

        if len(par_list) == 0:
            par_list.append(deepcopy(new_parent))
        else:
            if par_list[0].getName() != new_parent.getName():
                par_list.append(deepcopy(new_parent))
        seed()

    return par_list

# Function that is responsibe for creating the new entitiy based on their parent's DNA
#
# Passes:
#        parents: The list that contains the parent entities
#        gen_num: The number of the generation that the new entity belongs to
#        entitiy_num: The number that idetifies each entity in generation apart
#        isStagnating: Boolean value responsibe for identifiying if stagnation has occured
# Returns:
#        new_entity: the new entity created from the parent's DNA
def create_new_entity(parents, gen_num, entity_num, isStagnating):

    new_entity = entity.Entity(name=f'G{gen_num + 1}E{entity_num}')

    # Sets the new entity's statistic
    new_entity.setGeneration(gen_num + 1)
    new_entity.setParents([parents[0].getName(), parents[1].getName()])
    new_entity.setActionList(construct_Dna(parents))
    new_entity.setMasterEntity(parents[0].getMasterEntity())

    # Doubles DNA Cap if Stagnating else keep DNA Cap the same
    if isStagnating:
        new_entity.setDNACap(parents[0].getDNACap() * 2)
    else:
        new_entity.setDNACap(parents[0].getDNACap())
    return new_entity

#   Function that is responsibe for creating the DNA based of the DNA from it's parents
#
# Passes:
#        parents: the list of entities that are the parents to the new entitiy
#
# Returns:
#        new_dna: the list of actions that is the DNA for the new entity
def construct_Dna(parent):
    new_dna = []

    par1_dna = parent[0].getActionList()
    par2_dna = parent[1].getActionList()

    assert len(par1_dna) == len(par2_dna)
    for iter in range(len(par1_dna)):

        if par1_dna[iter].getMutation() < par2_dna[iter].getMutation():
            new_dna.append(attempt_mutation(par1_dna[iter]))

        else:
            new_dna.append(attempt_mutation(par2_dna[iter]))

    return new_dna

#   Function that decides if a gene will mutate
#
# Passes:
#        gene: an action that could undergo the process of mutation
#
# Returns:
#       gene: The same action that was passed in if no mutation has occured
#             or a randomly generated action if mutation has occured
def attempt_mutation(gene):
    seed()

    mutation_chance = gene.getMutation()
    yes_mut = int(mutation_chance * 100)
    no_mut = 100 - yes_mut
    mut_list = ['Y'] * yes_mut + ['N'] * no_mut

    shuffle(mut_list)
    mut_choice = choice(mut_list)

    if mut_choice == 'Y':
        return action.Action(ah.generate_action(), 1)
    else:
        return gene
#   Function that creates the choose pool used to choose parents for mating
#
# Passes:
#        mating_pool: the list that is used to determine how much of the total mating
#                     pool each entity will occupy
#
# Returns:
#        choose_pool: A list that is used to choose which entities will mate
def choose_pool_creater(mating_pool):
    choose_pool = []
    target_len = 0

    for pools in mating_pool:
        # Obtains the total amount of space each pool will occupy in the choose pool
        last_index = len(pools) - 1
        target_len += pools[last_index][1]

        # If there are entities to occupy the targeted amount of space in the choose pool
        if len(pools) > 1:
            #   Determines how much space each entity from the mating_pool are gaurenteed
            # to have in the choose pool
            equal_rep = target_len // (last_index + 1)

            # Allocates equal amount of spaces to each entitiy from the mating pool into
            # the choose pool
            for pos, ent in enumerate(pools):
                if isinstance(ent[1], int):
                    break
                curr_list = equal_rep * [ent[1]]
                choose_pool += curr_list

            fitness_ent_pos = last_index - 1

            # If there is space remaing in the choose pool, for the current mating pool,
            # that has not been allocated, then entities from the current mating pool, from fittess
            # entitiy to  the least fit entity, will be added until the space is filled.
            while len(choose_pool) < target_len:
                choose_pool.append(pools[fitness_ent_pos][1])
                fitness_ent_pos -= 1

                if fitness_ent_pos < 0:
                    fitness_ent_pos = last_index - 1

    return choose_pool

#   Function that checks to see if the generation fitness avarage has been stagnating
# for the past 10 generation
#
# Passes:
#          gen_num: The number that represent which generation the program is currently on
#
# Returns:
#        True: if stagnation occured
#        False: if stagnation has not occured
def stagnation_checker(gen_num):
    global last_stag_gen

    print('\nStagnation Report:\n')

    # Loads in the fitness average of the current generation the program is on
    initial_avg = filehandler.load_data(f'entity_data/Generation_{gen_num}/Avg_Fitness.pickle')
    initial_gen_num = gen_num

    # Keeps track of the number of stagnating generation
    num_of_stag = 0

    # Looks back at previous 10 generation until:
    #       A generation average deviates from the current stagnating avaerage
    #       10 generation are in the range of the stagnating avaerage
    #       or the 0ith generation is reached
    while gen_num > (initial_gen_num - 10) and gen_num >= 0:
        curr_avg = filehandler.load_data(f'entity_data/Generation_{gen_num}/Avg_Fitness.pickle')
        stagnating = (initial_avg - 0.01) <= curr_avg <= (initial_avg + 0.01) and last_stag_gen != gen_num
        print(f'    Generation {gen_num}: {initial_avg - 0.01} <= {curr_avg} <= {initial_avg + 0.01} is {stagnating}')
        if not stagnating:
            return False
        gen_num -= 1
        num_of_stag += 1

    # Must been at least 10 generation with values within stagnation range in order
    # for stagnation to occur
    print(f'\nNumber of Stagnating Generation: {num_of_stag}\n')
    if num_of_stag != 10:
        return False

    #   Sets the intial gen num as last stagnation generation in
    # order to prevent concurrent stagnation detection
    last_stag_gen = initial_gen_num
    print(f'last stagnating generation: {last_stag_gen}')
    print("STAGNATION HAS BEEN DETECTED!!!\n Extending DNA CAP to double the current one\n")
    return True
