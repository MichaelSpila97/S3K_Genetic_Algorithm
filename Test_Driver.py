
from copy import deepcopy

import time
import threading
import queue

import gdv
import entity
import filehandler
from Test_GUI import Test_GUI

gui_func_qu = queue.Queue(maxsize=5)

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
    gui = Test_GUI()

# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities die or
# complete the game. After every entitiy is dead the entire generations state is
# saved in a pickle file denoted Raw.
#   Need to added functionality to determine if the entity wins the game
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_training(gen=[]):
    gui_func_qu.put('Toggle Button')
    print('Before sleep')
    time.sleep(2)

    # If thier are entities to test
    if gen:
        gen_num = gen[0].generation
        for entities in gen:
            entities.play_game()
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
# ______________________________________________________________________________


if __name__ == '__main__':
    main()
