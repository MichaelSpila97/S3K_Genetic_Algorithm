
import entity
import filehandler
import time
import os
import copy


#checks score is consitantly increasing
#if it decreases for no reason set value to previous correct value

#Rings will stay the same at the beginning form last attempt if rings do not go away upon death
#as such set rings to zero for first action of entity

#make the score represent what the entity actual gained and not the overall score for a generation
def clean_dna(generation):
    gen_list = generation

    score = 0
    curr_previous_score = 0
    next_previous_score = 0
    rings = 0
    lives = 3

    for entities in generation:
        i = 0

        print(f'entity beginning {entities.action_list[len(entities.action_list) - 1].score_count}')
        next_previous_score = copy.deepcopy(entities.action_list[len(entities.action_list) - 1].score_count)

        for dna in entities.action_list:

            if score == (dna.getScoreCount() - curr_previous_score) or score < (dna.getScoreCount() - curr_previous_score):

                score = (dna.getScoreCount() - curr_previous_score)
                print(f"score: {dna.getScoreCount()} - {curr_previous_score} = {dna.getScoreCount() - curr_previous_score}")

                if curr_previous_score != 0:
                    dna.setScoreCount(score)

            elif score > (dna.getScoreCount()- previous_score):
                dna.setScoreCount(score)

            if dna.getRingCount() > 0 and i == 0:
                j = 0
                while entities.action_list[j].ring_count != 0:
                    entities.action_list[j].ring_count = 0
                    j += 1

            elif rings == dna.getRingCount() or rings < dna.getRingCount() or dna.getRingCount() == 0:
                dna.setRingCount(rings)

            elif rings > dna.getRingCount() and dna.getRingCount() != 0:
                dna.setRingCount(rings)

            if lives == dna.getLivesCount() or lives + 1 == dna.getLivesCount():
                lives = dna.lives_count

            elif lives < dna.getLivesCount():
                entites.setActionList(entites.action_list[:i])
            i += 1

        curr_previous_score = copy.deepcopy(next_previous_score)

        score = 0
        rings = 0
    filehandler.save_data(generation, 'entity_data/Generation_0/Clean_gen_0')

def eval_dna(generation):

    pgen = positive_eval(copy.deepcopy(generation))
    ngen = negative_eval(copy.deepcopy(pgen))
    filehandler.save_data(ngen, 'entity_data/Generation_0/Eval_gen_0')

def positive_eval(generation):
    pos_gen = generation

    for ent in pos_gen:

        rings = 0
        score = 0
        delay = 0

        reset_delay = False
        i = 0
        curr_lives = ent.action_list[i].getLivesCount()

        while ent.action_list[i].getLivesCount() >= curr_lives:

            delay =  delay + ent.action_list[i].getDelay()
            if rings < ent.action_list[i].getRingCount() or score < ent.action_list[i].getScoreCount():

                if delay <= 5:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.100, 10, 'dec'))
                else:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 5, 'dec'))

                reset_delay = True

            if reset_delay:
                delay = 0
                reset_delay = False

            rings = ent.action_list[i].getRingCount()
            score = ent.action_list[i].getScoreCount()
            #print(f'Mutation: {ent.action_list[i].getMutation()}')
            i = i + 1

    return pos_gen

def negative_eval(generation):
    neg_gen = generation

    for ent in generation:

        rings = 0
        score = 0
        rdelay = 0
        sdelay = 0

        reset_sdelay = False
        reset_rdelay = False

        i = 0

        curr_lives = ent.action_list[i].getLivesCount()

        while ent.action_list[i].getLivesCount() >= curr_lives:

            rdelay =  rdelay + ent.action_list[i].getDelay()
            sdelay =  sdelay + ent.action_list[i].getDelay()

            if ent.action_list[i].getRingCount() == 0:

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.010, 10, 'inc'))

            if rdelay >= 30 and ent.action_list[i].getRingCount() == rings:

                if rings == 0:
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.10, 30, 'inc'))
                else :
                    ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 30, 'inc'))

                reset_rdelay = True

            if sdelay >= 30 and ent.action_list[i].getScoreCount() == score:

                ent.setActionList(mutation_adjuster(ent.getActionList(), i, 0.050, 30, 'inc'))
                reset_sdelay = True


            rings = ent.action_list[i].getRingCount()
            score = ent.action_list[i].getScoreCount()


            if reset_rdelay:
                rdelay = 0
                reset_rdelay = False

            if reset_sdelay:
                sdelay = 0
                reset_sdelay = False

            i = i + 1

    return neg_gen
def mutation_adjuster(action_list, index, amount, delay, direction):

    while delay > 0 and index >= 0:

        if direction == 'dec':

            action_list[index].setMutation(float(format(action_list[index].getMutation() - amount, '.2f')))

        elif direction == 'inc':

            action_list[index].setMutation(float(format(action_list[index].getMutation() + amount, '.2f')))

        if action_list[index].getMutation() > 1:
            action_list[index].setMutation(1)

        elif action_list[index].getMutation() < 0:
            action_list[index].setMutation(0)

        delay = delay - action_list[index].getDelay()
        index = index - 1

    return action_list

def reproduce(generation):
    pass

def choose_mates(generation):
    pass

def mutate_dna(generation):
    pass

def random_list_handler(generation):
    pass
