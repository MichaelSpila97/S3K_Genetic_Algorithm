
import src.handlers.filehandler as filehandler
from ..behavior_mods.penatly import *
from ..behavior_mods.reward import *

def calc_fitness(generation, gen_num):
    fitgen = generation
    fit_avg = 0
    for entities in generation:
        dna_len = len(entities.getActionList())
        mutation_total = 0

        for dna in entities.getActionList():
            mutation_total = mutation_total + dna.getMutation()

        entities.setFitness(round(1 - (mutation_total / dna_len), 2))
        fit_avg += entities.getFitness()

    fit_avg = round(fit_avg / len(generation), 2)
    filehandler.save_data(fit_avg, f'entity_data/Generation_{gen_num}/Avg_Fitness')
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
            in_last_five_seconds = delay_keeper <= 2

            delay_keeper = delay_keeper + actions.getDelay()
            #   Positive evaluation for the current action and previous action
            # will occur if the ring or score count has increased
            if ringsOrScoreIncreased(curr_rings, curr_score, prev_rings, prev_score):

                #   If the increases occured within five seconds of previous increase
                #   Then the positive reward for the current action an previous
                # action will increase to 0.100
                if in_last_five_seconds:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.100, 3, 'dec'))
                #   Else the reward for the current and previous action will be
                # the standarded 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 2, 'dec'))

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

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 2, 'inc'))

            # Penilize the current actions and previous action if the entities rings has not changed
            if ringsAreStagnating(rdelay_keeper, actions.getRingCount(), prev_rings):

                # If the entity has been holding no rings for awhile give them higher penility
                if isDefenseless(actions.getRingCount(), prev_rings):
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.10, 3, 'inc'))
                # Else the penility will be the standard 0.05
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 3, 'inc'))

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
