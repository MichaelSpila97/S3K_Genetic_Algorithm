from copy import deepcopy
from random import shuffle, choice, seed

from ..classes import action, entity
from ..handlers import action_handler as ah, filehandler
from behavior_mods.penatly import *
from behavior_mods.reward import *

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

        for dna in entities.action_list:
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

            #   Sets actions at Beggining to zero if they are not zero
            #   Countinues until first legit zero appears in a action in the
            # action list
            if dna.getRingCount() > 0 and i == 0:
                j = 0
                while entities.action_list[j].ring_count != 0:
                    entities.action_list[j].ring_count = 0
                    j += 1

            #       If the ring count is legit then ring_keeper var should be set to
            # equal the current actions score count
            elif ring_keeper == dna.getRingCount() or \
                 ring_keeper < dna.getRingCount() or \
                 dna.getRingCount() == 0:

                ring_keeper = dna.getRingCount()

            #       If the ring count is not legit than the current action ring count
            # should be set to the ring keepers value
            elif ring_keeper > dna.getRingCount() and dna.getRingCount() != 0:
                dna.setRingCount(ring_keeper)

        # End of ring cleaning block
        # ---------------------------------------------------------------------
            i += 1

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
        print(dna_len)
        mutation_total = 0

        for dna in entities.getActionList():
            mutation_total = mutation_total + dna.getMutation()

        entities.setFitness(1 - (mutation_total / dna_len))

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
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.100, 10, 'dec'))
                #   Else the reward for the current and previous action will be
                # the standarded 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 5, 'dec'))

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
        prev_score = 0
        prev_lives = ent.getActionList()[0].getLivesCount()

        # Ring delay keeper
        rdelay_keeper = 0

        # Score delay keeper
        sdelay_keeper = 0

        reset_sdelay_keeper = False
        reset_rdelay_keeper = False
        penilize_life = True

        for i, actions in enumerate(ent.getActionList()):

            rdelay_keeper = rdelay_keeper + actions.getDelay()
            sdelay_keeper = sdelay_keeper + actions.getDelay()
            past_start = i != 0

            # Penilize the current action and previous action if the entity losses rings
            if isDefenseless(curr_rings, prev_rings):

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 10, 'inc'))

            # Penilize the current actions and previous action if the entities rings has not changed
            if ringsAreStagnating(rdelay_keeper, curr_rings, prev_rings):

                # If the entity has been holding no rings for awhile give them higher penility
                if isDefenseless(curr_rings, prev_rings):
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.10, 30, 'inc'))
                # Else the penility will be the standard 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 30, 'inc'))

                reset_rdelay_keeper = True

            # Penilize the current actions and previous action if the entities score has not changed
            if scoreIsStangnating(sdelay_keeper, curr_score, prev_score):

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 30, 'inc'))
                reset_sdelay_keeper = True

            if past_start:
                if lostLife(curr_lives, prev_lives, penilize_life):
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.25, 30, 'inc'))
                    penilize_life = False

            prev_rings = actions.getRingCount()
            prev_score = actions.getScoreCount()
            prev_lives = actions.getLivesCount()

            # Resets rdelay onces a penalty has been assesed for ring counts
            if reset_rdelay_keeper:
                rdelay_keeper = 0
                reset_rdelay_keeper = False

            # Resets sdelay onces a penalty has been assessed for score counts
            if reset_sdelay_keeper:
                sdelay_keeper = 0
                reset_sdelay_keeper = False

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

    old_gen_num = generation[0].getGeneration()

    mating_pool = assign_entities_to_pools(generation)
    config_mp = configure_mating_percents(deepcopy(mating_pool))

    new_generation = choose_and_mate(config_mp, old_gen_num, num_of_entities)

    new_gen_num = generation[0].getGeneration()
    filehandler.save_data(new_generation, f'entity_data/Generation_{new_gen_num}/Offspring_gen_{new_gen_num}')

# Function assigns entities to one of the four mating pools based on thier fitness score
#
# Passes:
#        generation: List of entities that belong to a generation
#
# Returns:
#        mating_pool: List of the four mating pools with the entities in their
#                     respective pools
def assign_entities_to_pools(generation):
    mating_pools = [[5], [15], [30], [50]]

    for entities in generation:

        ent_fitness = entities.getFitness() * 100
        if ent_fitness < 30:
            mating_pools[0].sort()
            if len(mating_pools[0]) == 6:
                if mating_pools[0][0].getFitness() < ent_fitness:
                    maitng_pools[0][0] = entities
            else:
                mating_pools[0].append(entities)
        elif ent_fitness >= 30 and ent_fitness < 50:
            mating_pools[1].sort()
            mating_pools[1].append(entities)
        elif ent_fitness >= 50 and ent_fitness < 70:
            mating_pools[2].sort()
            mating_pools[2].append(entities)
        elif ent_fitness >= 70:
            mating_pools[3].sort()
            mating_pools[3].append(entities)

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
    print('     configuring mating p')

    top_iter = len(mating_pool) - 1
    bottom_iter = 0

    t_carry_percent = 0
    b_carry_percent = 0

    b_pool_is_empty = True
    t_pool_is_empty = True

    # Initial Moving of mating percent values in occupied pools
    while b_pool_is_empty or t_pool_is_empty:

        last_index = len(mating_pool[top_iter]) - 1
        mating_pool[top_iter][last_index] += t_carry_percent
        t_carry_percent = 0

        if len(mating_pool[top_iter]) == 1:
            t_carry_percent += mating_pool[top_iter][last_index]
            mating_pool[top_iter][last_index] = 0
            top_iter -= 1
        else:
            t_pool_is_empty = False

        last_index = len(mating_pool[bottom_iter]) - 1
        mating_pool[bottom_iter][0] += b_carry_percent
        b_carry_percent = 0

        if len(mating_pool[bottom_iter]) == 1:
            b_carry_percent += mating_pool[bottom_iter][last_index]
            mating_pool[bottom_iter][last_index] = 0
            bottom_iter += 1
        else:
            b_pool_is_empty = False

    i = 0
    dangling_percent = 0

    #   Second run over of mating pools to make sure no empty pools have non-zero
    # values

    while i != top_iter:
        last_index = len(mating_pool[i]) - 1
        if mating_pool[i][last_index] != 0 and len(mating_pool[i]) == 1:
            dangling_percent += mating_pool[i][last_index]
            mating_pool[i][last_index] = 0
        i += 1
    last_index = len(mating_pool[top_iter]) - 1
    mating_pool[top_iter][last_index] += dangling_percent

    print(f'{mating_pool}\n     Finish configuring mating pool')
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
    print('     Choosing and mating')
    choose_pool = choose_pool_creater(mating_pool)

    new_generation = []

    while len(new_generation) < num_of_entities:
        parents = choose_parents(choose_pool)
        new_generation.append(create_new_entity(parents, gen_num, len(new_generation) + 1))

    print('     Finish Choosing and mating')
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
    print('     Choosing parents')
    par_list = []
    while len(par_list) < 2:
        shuffle(choose_pool)
        new_parent = choice(choose_pool)

        if len(par_list) == 0:
            par_list.append(deepcopy(new_parent))
        else:
            if par_list[0].getFitness() != new_parent.getFitness():
                par_list.append(deepcopy(new_parent))
        seed()

    print('     Finish Choosing parents')
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
    print('     Creatining new entity')
    new_entity = entity.Entity(name=f'G{gen_num + 1}E{entity_num}')

    new_entity.setGeneration(gen_num + 1)
    new_entity.setParents([parents[0].getName(), parents[1].getName()])
    new_entity.setActionList(construct_Dna(parents))

    print('     Finish Creating new entity')
    return new_entity

#   Function that is responsibe for creating the DNA based of the new entities parents
#
# Passes:
#        parents: the list of entities that are the parents to the new entitiy
#
# Returns:
#        new_dna: the list of actions that is the dna for the new entity
def construct_Dna(parent):
    print('     Constructing DNA')
    new_dna = []

    par1_dna_left = True
    par2_dna_left = True

    par1_itr = 0
    par2_itr = 0

    par1_dna = parent[0].getActionList()
    par2_dna = parent[1].getActionList()

    while par1_dna_left or par2_dna_left:

        par_choice_list = ["P1"] * 50 + ["P2"] * 50
        shuffle(par_choice_list)
        par_choice = choice(par_choice_list)

        seed()

        if par_choice == "P1":

            if par1_dna_left:
                new_dna.append(attempt_mutation(par1_dna[par1_itr]))
            else:
                new_dna.append(attempt_mutation(par2_dna[par2_itr]))

        elif par_choice == "P2":

            if par2_dna_left:
                new_dna.append(attempt_mutation(par2_dna[par2_itr]))
            else:
                new_dna.append(attempt_mutation(par1_dna[par1_itr]))

        par1_itr += 1
        par2_itr += 1

        if par1_itr > len(par1_dna) - 1:
            par1_dna_left = False

        if par2_itr > len(par2_dna) - 1:
            par2_dna_left = False

    print('     Finish Constructing DNA')
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
    curr_max = None

    for items in elements:

        if len(items) > 1:
            last_index = len(items) - 1
            equal_rep = items[last_index] // (len(items) - 1)
            i = 1
            while i < len(items):
                curr_list = equal_rep * [items[i]]
                choose_pool += curr_list

                if curr_max is None:
                    curr_max = items[i]
                elif curr_max.getFitness() < items[i].getFitness():
                    curr_max = items[i]

                i += 1
    if len(choose_pool) != 100:
        while len(choose_pool) != 100:
            choose_pool.append(curr_max)

    return choose_pool


# ____________________________________________________________________________________________
