from copy import deepcopy
from random import shuffle, choice, seed
from ...classes import action, entity
from ...handlers import action_handler as ah, filehandler

last_stag_gen = -1
# Function assigns entities to one of the four mating pools based on thier fitness score
#
# Passes:
#        generation: List of entities that belong to a generation
#
# Returns:
#        mating_pool: List of the four mating pools with the entities in their
#                     respective pools
def assign_entities_to_pools(generation):
    mating_pools = [[[2, 5]],
                    [[2, 15]],
                    [[2, 30]],
                    [[2, 50]]]

    for entities in generation:

        ent_fitness = entities.getFitness() * 100
        if ent_fitness < 30:
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
        elif ent_fitness >= 98:
            return entities

    return mating_pools

#   Function that moves mating percentage values from empty mating pool values in ward .
# If mating percentages are stuck in the middle of two occupied mating pools then those precentages goes
# up to the higher mating pool
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
#           new_generation: The new generation created from the mating of parents entities
def choose_and_mate(mating_pool, gen_num, num_of_entities):
    choose_pool = choose_pool_creater(mating_pool)
    # print(f'choose pool:')
    # print_list(choose_pool)

    new_generation = []
    isStag = stagnation_checker(gen_num)
    while len(new_generation) < num_of_entities:
        parents = choose_parents(choose_pool)
        new_generation.append(create_new_entity(parents, gen_num, len(new_generation) + 1, isStag))

    return new_generation

def assign_master(master, gen_num, num_of_entities):

    new_generation = []

    master_dna = master.getActionList()
    if master.getMasterEntity() is not None:
        master_dna = master.getMasterEntity().getActionList() + master_dna

    master.setActionList(master_dna)

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

# Function that is responsibe for creating the new entitiy based on its parents DNA
#
# Passes:
#        parents: The list that contains the name of the parents to the new entitiy
#        gen_num: The number of the generation that the new entity belongs to
#        entitiy_num: The number that idetifies each entity in generation apart
#
# Returns:
#        new_entity: the new entity created from the parents DNA
def create_new_entity(parents, gen_num, entity_num, isStagnating):

    new_entity = entity.Entity(name=f'G{gen_num + 1}E{entity_num}')

    new_entity.setGeneration(gen_num + 1)
    new_entity.setParents([parents[0].getName(), parents[1].getName()])
    new_entity.setActionList(construct_Dna(parents))
    new_entity.setMasterEntity(parents[0].getMasterEntity())
    if isStagnating:
        new_entity.setDNACap(parents[0].getDNACap() * 2)
    else:
        new_entity.setDNACap(parents[0].getDNACap())
    return new_entity

#   Function that is responsibe for creating the DNA based of the new entities parents
#
# Passes:
#        parents: the list of entities that are the parents to the new entitiy
#
# Returns:
#        new_dna: the list of actions that is the dna for the new entity
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

#   Function that decides wheater a gene will mutate
#
# Passes:
#        gene: an action that is being evaluted for wheather it will mutate
#
# Returns:
#        dna: the list of actions that is the dna for the new entity
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
#        elements: the list that contains lists of items that represents each parents
#                  and thier corresponding percent chance of being choosen
#
# Returns:
#        choose_pool: A list that is the newly created choose pool
def choose_pool_creater(elements):
    choose_pool = []
    target_len = 0

    for items in elements:
        last_index = len(items) - 1
        target_len += items[last_index][1]
        if len(items) > 1:
            equal_rep = target_len // (last_index + 1)
            for pos, ent in enumerate(items):
                if isinstance(ent[1], int):
                    break
                curr_list = equal_rep * [ent[1]]
                choose_pool += curr_list

            fitness_ent_pos = last_index - 1

            while len(choose_pool) < target_len:
                choose_pool.append(items[fitness_ent_pos][1])
                fitness_ent_pos -= 1

                if fitness_ent_pos < 0:
                    fitness_ent_pos = last_index - 1
    return choose_pool

def stagnation_checker(gen_num):
    global last_stag_gen

    print('\nStagnation Report:\n')
    initial_avg = filehandler.load_data(f'entity_data/Generation_{gen_num}/Avg_Fitness.pickle')
    initial_gen_num = gen_num
    num_of_stag = 0
    while gen_num > (initial_gen_num - 10) and gen_num >= 0:
        curr_avg = filehandler.load_data(f'entity_data/Generation_{gen_num}/Avg_Fitness.pickle')
        stagnating = (initial_avg - 0.01) <= curr_avg <= (initial_avg + 0.01) and last_stag_gen != gen_num
        print(f'    Generation {gen_num}: {initial_avg - 0.01} <= {curr_avg} <= {initial_avg + 0.01} is {stagnating}')
        if not stagnating:
            return False
        gen_num -= 1
        num_of_stag += 1

    print(f'\nNumber of Stagnating Generation: {num_of_stag}\n')
    if num_of_stag != 10:
        return False

    last_stag_gen = initial_gen_num
    print(f'last stagnating generation: {last_stag_gen}')
    print("STAGNATION HAS BEEN DETECTED!!!\n Extending DNA CAP to double the current one\n")
    return True
