
from copy import deepcopy

import time
import threading
import queue
import keyboard
import os

import gdv
import entity
import filehandler
import entity_handler
from Test_GUI import Test_GUI

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
    Test_GUI()


# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities complete their attempt.
# After every entitiy is dead the entire generations state is saved in a pickle file, denoted Raw,
# and is then set to be processed by the process data method
#
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_training(gen=[]):

    gen_num = 0

    # Turns off Buttons so no more testing request can be made till testing is over
    gui_func_qu.put('Toggle Button')

    # Automatics press correct buttons to start game if the program is at the start screen
    if gdv.isAtStartScreen():
        start_next_game()

    # Waits for statistic to appear on screen to begin training
    while not gdv.isTrainingStarted():
        pass

    # If thier are entities in the gen list
    if gen:
        # Gets Generation number from entities for file and directory nameing purposes
        gen_num = gen[0].generation

        for entities in gen:
            entities.play_game()

        os.mkdir(f'{os.getcwd()}/entity_data/Generation_{gen_num}')
        filehandler.save_data(gen, f'entity_data/Generation_{gen_num}/Raw_Gen_{gen_num}')

    # Else need to create three new entities that will compose generation 0
    else:
        while gdv.curr_lives > 0:

            ent = deepcopy(entity.Entity(name=f'G0E{3 - (gdv.curr_lives - 1)}'))
            ent.play_game()
            gen.append(deepcopy(ent))
        filehandler.save_data(gen, 'entity_data/Generation_0/Raw_gen_0')

    print('Game over\nSaving Data..')

    gui_func_qu.put('Toggle Button')

    process_data(gen, gen_num)
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
def process_data(gen, gen_num):
    print('cleaning data')
    entity_handler.clean_dna(gen)

    print('Evaluating data')
    clean_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}.pickle')
    entity_handler.eval_entity(clean_gen)

    print('Creating offspring')
    eval_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}.pickle')
    entity_handler.reproduce(eval_gen)

    if continue_training == 1:
        offspring = filehandler.load_data(f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}.pickle')
        while not gdv.isAtStartScreen():
            print('Not at start')

        gdv.reset_stats()
        start_next_game()
        begin_training(offspring)

# ______________________________________________________________________________
#       Fuction that execute necessary button press to get from the start screen of Sonic
# 3 and Knukles to a new game. Note you will have to scoll up the first time this is executed to
# get Sonic only a character since the game remeber your selection of characters in the no save
# selection.
def start_next_game():
    print('Starting game..')

    # Presses enter to move to save select screen
    time.sleep(5)
    keyboard.press('enter')
    time.sleep(0.1)
    keyboard.release('enter')

    time.sleep(5)

    # Press left to move cursor over the no save selection
    keyboard.press('left')
    time.sleep(0.1)
    keyboard.release('left')

    time.sleep(1)

    # Press enter to start the game
    keyboard.press('enter')
    time.sleep(0.2)
    keyboard.release('enter')

# ______________________________________________________________________________


if __name__ == '__main__':
    main()
