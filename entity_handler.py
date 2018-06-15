
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
    filehandler.save_data(generation, 'entity_data/Generation_0/tClean_gen_0')

def eval_dna(generation):
    pass

def reproduce(generation):
    pass


def choose_mates(generation):
    pass


def mutate_dna(generation):
    pass


def random_list_handler(generation):
    pass
