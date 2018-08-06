from copy import deepcopy
from ..handlers import filehandler
from .subhandlers.evaluation_handler import *
from .subhandlers.reproduc_handler import *

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
#   Wrapper function that execute all evaluation functions and saves the state of
# the generation object after evaluation
def eval_entity(generation):

    ngen = neg_dna_eval(deepcopy(generation))
    pgen = pos_dna_eval(deepcopy(ngen))
    gen_num = generation[0].getGeneration()
    fgen = calc_fitness(deepcopy(pgen), gen_num)

    filehandler.save_data(fgen, f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}')


# ____________________________________________________________________________________________
#   Wrapper function that execute all reproduction functions and saves the state of
# the generation object after reproduction is done
def reproduce(generation, num_of_entities):

    gen_num = generation[0].getGeneration()
    mating_pool = assign_entities_to_pools(generation)

    print('Maiting Pool:')
    print_list(mating_pool)

    new_generation = []

    # Creates next generation with current dna data if no master was created
    if isinstance(mating_pool, list):
        config_mp = configure_mating_percents(deepcopy(mating_pool))
        print('Config Pool:')
        print_list(config_mp)
        new_generation = choose_and_mate(config_mp, gen_num, num_of_entities)

    # Creates next generation with no dna data and appends new master if a master was created
    else:
        print('MASTER HAS BEEN CREATED.\n SETTING NEW MASTER ANS MAKING A EMPTY GENERATION\n')
        new_generation = assign_master(mating_pool, gen_num, num_of_entities)

    print('\n')
    filehandler.save_data(new_generation, f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}')

# Generic function for print out list of objects. Mainly used to print out generation of entities
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
# ____________________________________________________________________________________________
