
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
#   This contains the tkinter gui and methods responsible for facillitating an
# entire generations attempts at completing sonic 3 and Knukles. Can start test
# by simplely pressing a button. Planning to added more features such as a graphical
# display of all entities and thier current states through sprites
# ______________________________________________________________________________
#   The main builds the tkinter gui and sets the functions to be called when one
# of the buttons is pressed
def main():
    # Creates and execute thread responsible for capturing data from game screen in concurence
    # with the testing code

    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    stat_thread.start()
    Test_GUI()


# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities die or
# complete the game. After every entitiy is dead the entire generations state is
# saved in a pickle file denoted Raw.
#   Need to added functionality to determine if the entity wins the game
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_training(gen=[]):

    gui_func_qu.put('Toggle Button')

    if gdv.isAtStartScreen():
        start_next_game()

    while not gdv.isTrainingStarted():
        pass

    if gen:
        gen_num = gen[0].generation
        for entities in gen:
            entities.play_game()

        os.mkdir(f'{os.getcwd()}/entity_data/Generation_{gen_num}')
        filehandler.save_data(gen, f'entity_data/Generation_{gen_num}/Raw_Gen_{gen_num}')
    # Else need to create three new entities and have them attempt the
    # game to create Generation 0
    else:
        while gdv.curr_lives > 0:
            print(f'cur lives {gdv.curr_lives}')
            ent = deepcopy(entity.Entity(name=f'G0E{3 - (gdv.curr_lives - 1)}'))
            ent.play_game()
            gen.append(deepcopy(ent))
        filehandler.save_data(gen, 'entity_data/Generation_0/Raw_gen_0')

    print('Game over\nSaving Data..')
    gui_func_qu.put('Toggle Button')
    process_data(gen)

def process_data(gen):
    gen_num = gen[0].getGeneration()
    print('cleaning data')
    entity_handler.clean_dna(gen)

    print('Evaluating data')
    clean_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}.pickle')
    entity_handler.eval_entity(clean_gen)

    print('Creating offspring')
    eval_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}.pickle')
    entity_handler.reproduce(eval_gen)

    print(continue_training)
    print(continue_training == 1)
    if continue_training == 1:
        offspring = filehandler.load_data(f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}.pickle')
        while not gdv.isAtStartScreen():
            print('Not at start')

        start_next_game()
        begin_training(offspring)

def start_next_game():
    print('Starting game..')
    time.sleep(5)
    keyboard.press('enter')
    time.sleep(0.1)
    keyboard.release('enter')

    time.sleep(5)

    keyboard.press('left')
    time.sleep(0.1)
    keyboard.release('left')

    time.sleep(1)

    keyboard.press('enter')
    time.sleep(0.2)
    keyboard.release('enter')

# ______________________________________________________________________________


if __name__ == '__main__':
    main()
