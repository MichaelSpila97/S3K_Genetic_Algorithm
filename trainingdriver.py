import threading
import queue
import os

from src.classes import entity, traininggui
from src.handlers import filehandler, entity_handler
from src.gdmodules import gdv

gui_func_qu = queue.Queue(maxsize=5)
continue_training = 0
# ______________________________________________________________________________
#   This contains the function responsible for facilitating the training and processing
# of entities and thier data. Also responsible for automating the process of training
# so the user does not need to be present at all times while training is occuring
# ______________________________________________________________________________
#   The main creates and execute thread responsible for capturing data from game screen
# and call Test_GUI to build the programs gui
def main():
    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    stat_thread.start()

    # Builds Gui that displays in game stats and used to start test
    traininggui.GUI()


# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities complete their attempt.
# After every entitiy is dead the entire generations state is saved in a pickle file, denoted Raw,
# and is then set to be processed by the process data method
#
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_training(num_of_entities, gen=None):

    gen_num = 0
    total_entities = num_of_entities

    # Turns off Buttons so no more testing request can be made till testing is over
    gui_func_qu.put('Toggle Button')

    # Automatics press correct buttons to start game if the program is at the start screen

    # Waits for statistic to appear on screen to begin training
    while not gdv.isTrainingStarted():
        pass

    # If thier are entities in the gen list
    if gen:
        # Gets Generation number from entities for file and directory nameing purposes
        gen_num = gen[0].getGeneration()
        print(f'Generation {gen_num} training has begun')
        for entities in gen:
            entities.play_game()

    # Else need to create three new entities that will compose generation 0
    else:
        print(f'Generation {gen_num} training has begun')
        while num_of_entities > 0:

            ent = entity.Entity(name=f'G0E{total_entities - (num_of_entities - 1)}')
            ent.play_game()
            gen.append(ent)
            num_of_entities -= 1

    os.mkdir(f'{os.getcwd()}/entity_data/Generation_{gen_num}')
    filehandler.save_data(gen, f'entity_data/Generation_{gen_num}/Raw_Gen_{gen_num}')

    print(f'Generation {gen_num} training has ended')

    gui_func_qu.put('Toggle Button')

    process_data(gen, num_of_entities)
# ______________________________________________________________________________
#   Function that process the newly generated generation data from a training session .
# It Cleans the data of errors, evaluated each entities data and fitness, and then
# creates the generation offsprigs. If continuous training was selected the function will
# proceed to start up a new game an begin training again. If it wasn't the training will be
# over.
#
# Passes:
#        gen = List that contains entities that belong to the same generation
#        gen_num: The number of the gneration that is being passed in.
def process_data(gen, num_of_entities):
    gen_num = gen[0].getGeneration()
    print(f'\nProcessing Generation {gen_num} data...\n')
    entity_handler.clean_dna(gen)

    clean_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}.pickle')
    entity_handler.eval_entity(clean_gen)

    eval_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}.pickle')
    entity_handler.reproduce(eval_gen, num_of_entities)

    if continue_training == 1:
        print(f'Movining on to Generation {gen_num} training')
        offspring = filehandler.load_data(f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}.pickle')
        gdv.reset_stats()
        begin_training(offspring)

# ______________________________________________________________________________


if __name__ == '__main__':
    main()
