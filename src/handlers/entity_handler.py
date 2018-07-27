from copy import deepcopy
from random import shuffle, choice, seed

from ..classes import action, entity
from ..handlers import action_handler as ah, filehandler
from .behavior_mods.penatly import *
from .behavior_mods.reward import *

# ____________________________________________________________________________________________
# --------------------------Beginning of Cleaning Functions---------------------------------
# Function cleans the dna of each entity for errors and incosistances
# Also adjustes the values in each dna to represent the spefic attempt
# of each entity
# Passes:
#       generation: a list of entities that belong to one generation
# Saves:
#       The state of the generation list after each entity has been cleaned
def clean_dna(generation):

    # The score the last entity started on
    previous_starting_score = 0

    # The score the next entity starts on
    next_starting_score = 0

    # Keeps the score and ring counts of previous action
    score_keeper = 0
    ring_keeper = 0

    for entities in generation:
        i = 0

        next_starting_score = deepcopy(entities.action_list[len(entities.action_list) - 1].score_count)

        for count, dna in enumerate(entities.action_list):
        # ---------------------------------------------------------------------
        # Beggining of Score Cleaning Block

            adjusted_score = dna.getScoreCount() - previous_starting_score
            # If the score is legit then score_keeper var should be set to
            # equal the current actions score count

            if score_keeper == (adjusted_score) or score_keeper < (adjusted_score):
                score_keeper = adjusted_score

                if previous_starting_score != 0:
                    dna.setScoreCount(score_keeper)

            # If the score count is not legit than the current actions score
            # count should be set to the ring keepers value
            elif score_keeper > (adjusted_score):
                dna.setScoreCount(score_keeper)

        # End of Score Cleaning Block
        # ---------------------------------------------------------------------
        # Beggining of Ring Cleaning Block

            #  If the ring count is legit then ring_keeper var should be set to
            # equal the current actions score count
            if ring_keeper == dna.getRingCount() or \
                 ring_keeper < dna.getRingCount() or \
                 dna.getRingCount() == 0:

                ring_keeper = dna.getRingCount()

            #       If the ring count is not legit than the current action ring count
            # should be set to the ring keepers value
            elif ring_keeper > dna.getRingCount() and dna.getRingCount() != 0:
                dna.setRingCount(ring_keeper)

        # End of ring cleaning block
        # ---------------------------------------------------------------------

        previous_starting_score = deepcopy(next_starting_score)

        score_keeper = 0
        ring_keeper = 0

    gen_num = generation[0].getGeneration()
    filehandler.save_data(generation, f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}')
# ____________________________________________________________________________________________
# --------------------------Beginning of Evaluating Functions---------------------------------
#   Wrapper function that execute all evaluation functions and saves the state of
# the generation object after evaluation
def eval_entity(generation):

    ngen = neg_dna_eval(deepcopy(generation))
    pgen = pos_dna_eval(deepcopy(ngen))
    fgen = calc_fitness(deepcopy(pgen))
    gen_num = generation[0].getGeneration()
    filehandler.save_data(fgen, f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}')

def calc_fitness(generation):
    fitgen = generation

    for entities in generation:
        dna_len = len(entities.getActionList())
        mutation_total = 0

        for dna in entities.getActionList():
            mutation_total = mutation_total + dna.getMutation()

        entities.setFitness(round(1 - (mutation_total / dna_len), 2))

    return fitgen
#   Function handles the postive evaluation of the dna sequence of each enitiy
# in the generation gen_list
# Passes:
#        Generation: List of entities that belong to the same Generation
#
# Returns:
#        pos_gen: the evaluated Generation
def pos_dna_eval(generation):

    for ent in generation:

        prev_rings = 0
        prev_score = 0
        prev_lives = ent.getActionList()[0].getLivesCount()
        delay_keeper = 0

        reset_delay = False
        rewardact = True

        for i, actions in enumerate(ent.getActionList()):

            curr_rings = actions.getRingCount()
            curr_score = actions.getScoreCount()
            curr_lives = actions.getLivesCount()
            curr_act = actions.getAct()

            # Modifiers to actions:
            in_last_five_seconds = delay_keeper <= 5

            delay_keeper = delay_keeper + actions.getDelay()
            #   Positive evaluation for the current action and previous action
            # will occur if the ring or score count has increased
            if ringsOrScoreIncreased(curr_rings, curr_score, prev_rings, prev_score):

                #   If the increases occured within five seconds of previous increase
                #   Then the positive reward for the current action an previous
                # action will increase to 0.100
                if in_last_five_seconds:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.100, 5, 'dec'))
                #   Else the reward for the current and previous action will be
                # the standarded 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 3, 'dec'))

                reset_delay = True

            if livesIncreased(curr_lives, prev_lives):
                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.3, 15, 'dec'))

            if completedAct(curr_act, rewardact):
                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.5, 14400, 'dec'))
                rewardact = False

            if completedZone(curr_act, rewardact):
                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.5, 14400, 'dec'))
                rewardact = True

            if startedAct(curr_act, rewardact):
                rewardact = True

            # Resets the delay to 0 once a reward has been distributed
            if reset_delay:
                delay_keeper = 0
                reset_delay = False

            prev_rings = actions.getRingCount()
            prev_score = actions.getScoreCount()
            prev_lives = actions.getLivesCount()

    return generation

#   Function handles the negavtive evaluation of the dna sequence
# of each enitiy in the generation gen_list
# Passes:
#        Generation: List of entities that belong to the same Generation
#
# Returns:
#        neg_gen: the evaluated Generation
def neg_dna_eval(generation):

    for ent in generation:

        prev_rings = 0
        prev_lives = ent.getActionList()[0].getLivesCount()

        # Ring delay keeper
        rdelay_keeper = 0

        reset_rdelay_keeper = False
        penilize_life = True

        for i, actions in enumerate(ent.getActionList()):

            rdelay_keeper = rdelay_keeper + actions.getDelay()
            past_start = i != 0

            # Penilize the current action and previous action if the entity losses rings
            if isDefenseless(actions.getRingCount(), prev_rings):

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 10, 'inc'))

            # Penilize the current actions and previous action if the entities rings has not changed
            if ringsAreStagnating(rdelay_keeper, actions.getRingCount(), prev_rings):

                # If the entity has been holding no rings for awhile give them higher penility
                if isDefenseless(actions.getRingCount(), prev_rings):
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.10, 10, 'inc'))
                # Else the penility will be the standard 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 10, 'inc'))

                reset_rdelay_keeper = True

            if past_start:
                if lostLife(actions.getLivesCount(), prev_lives, penilize_life):
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.25, 10, 'inc'))
                    penilize_life = False

            prev_rings = actions.getRingCount()
            prev_lives = actions.getLivesCount()

            # Resets rdelay onces a penalty has been assesed for ring counts
            if reset_rdelay_keeper:
                rdelay_keeper = 0
                reset_rdelay_keeper = False

    return generation

# Function controls the adjustment of mutation values of action object from an action_list
# Passes:
#        action_list: a list of action that an entity executed during its session
#        index:       The place where the modification to the mutatin values will
#                     begin in the action_list
#        amount:      The amount the mutation value will increase or decrease
#        delay:       How far back the list will iterator before it reaches the
#                     end of its mutation range
#        direction:   Weather the amount will be added or subtracted to the mutation values
#
# Returns:   The newly adjusted action_list

def mutation_adjuster(action_list, index, amount, delay, direction):

    while delay > 0 and index >= 0:

        # Decreases a range of mutation, defined by the delay, by the defined amount
        if direction == 'dec':
            new_mutation = float(format(action_list[index].getMutation() - amount, '.2f'))
            action_list[index].setMutation(new_mutation)

        # Increases a range of mutation, defined by the delay, by the defined amount
        elif direction == 'inc':
            new_mutation = float(format(action_list[index].getMutation() + amount, '.2f'))
            action_list[index].setMutation(new_mutation)

        # Keeps mutation values from going over 1
        if action_list[index].getMutation() > 1:
            action_list[index].setMutation(1)

        # Keeps mutation values from going under 0
        elif action_list[index].getMutation() < 0:
            action_list[index].setMutation(0)

        # delay is subtracted from the delay kept in the action list
        delay = delay - action_list[index].getDelay()
        index = index - 1

    return action_list
# ____________________________________________________________________________________________
# -------------------------------Beginning of Reproductin Functions---------------------------
#   Wrapper function that execute all reproduction functions and saves the state of
# the generation object after reproduction is done
def reproduce(generation, num_of_entities):

    gen_num = generation[0].getGeneration()

    mating_pool = assign_entities_to_pools(generation)
    print('Maiting Pool:')
    print_list(mating_pool)

    new_generation = []
    if isinstance(mating_pool, list):
        config_mp = configure_mating_percents(deepcopy(mating_pool))
        print('Config Pool:')
        print_list(config_mp)

        new_generation = choose_and_mate(config_mp, gen_num, num_of_entities)

    else:
        print('MASTER HAS BEEN CREATED.\n SETTING NEW MASTER ANS MAKING A EMPTY GENERATION')
        new_generation = assign_master(mating_pool, gen_num, num_of_entities)

    filehandler.save_data(new_generation, f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}')


def print_list(lis):
    if isinstance(lis, list):
        for count, item in enumerate(lis):
            if isinstance(item, list):
                print(f'{count}: ')
                for i, obj in enumerate(item):
                    print(f'        {i}: {obj}')
            else:
                print(f'{count}: {item}')
    else:
        print(lis)
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
        elif ent_fitness >= 70 and ent_fitness < 95:
            mating_pools[3].append([entities.getFitness(), entities])
            mating_pools[3].sort(key=lambda x: x[0])
        elif ent_fitness >= 95:
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

    while len(new_generation) < num_of_entities:
        print('new_entity')
        parents = choose_parents(choose_pool)
        new_generation.append(create_new_entity(parents, gen_num, len(new_generation) + 1))

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
        print("Choosing Parents...")
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
def create_new_entity(parents, gen_num, entity_num):

    new_entity = entity.Entity(name=f'G{gen_num + 1}E{entity_num}')

    new_entity.setGeneration(gen_num + 1)
    new_entity.setParents([parents[0].getName(), parents[1].getName()])
    new_entity.setActionList(construct_Dna(parents))
    new_entity.setMasterEntity(parents[0].getMasterEntity())
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


# ____________________________________________________________________________________________
