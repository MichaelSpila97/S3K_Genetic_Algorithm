
from copy import deepcopy

import time
import threading
import queue

import gdv
import entity
import filehandler
from Test_GUI import Test_GUI

main_func_qu = queue.Queue(maxsize=5)
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

    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    gui_thread = threading.Thread(target=create_gui, daemon=True)

    # Creates and execute thread responsible for capturing data from game screen in concurence
    # with the testing code
    gui_thread.start()
    stat_thread.start()

    while True:
        exec_func_from_threads()

def create_gui():
    global gui
    gui = Test_GUI()

def add_func_for_main(func):
    main_func_qu.put(func)

def exec_func_from_threads():
    if not main_func_qu.empty():
        thread_func = main_func_qu.get()
        thread_func()

# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities die or
# complete the game. After every entitiy is dead the entire generations state is
# saved in a pickle file denoted Raw.
#   Need to added functionality to determine if the entity wins the game
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_test(gen=[]):

    print('Before sleep')
    time.sleep(2)

    # If thier are entities to test
    if gen:
        for entities in gen:
            entities.play_game()

    # Else need to create three new entities and have them attempt the
    # game to create Generation 0
    else:
        while gdv.curr_lives > 0:
            print(f'cur lives {gdv.curr_lives}')
            ent = deepcopy(entity.Entity(name=f'G0E{3 - (gdv.curr_lives - 1)}'))
            ent.play_game()
            gen.append(deepcopy(ent))

    print('Game over\nSaving Data..')
    filehandler.save_data(gen, 'entity_data/Generation_0/Raw_gen_0')

# ______________________________________________________________________________


if __name__ == '__main__':
    main()
