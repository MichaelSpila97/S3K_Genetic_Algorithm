from tkinter import *
from tkinter import filedialog
from copy import deepcopy

import time
import os
import threading

import gdv
import entity
import filehandler

button = []
# ______________________________________________________________________________
#   This contains the tkinter gui and methods responsible for facillitating an
# entire generations attempts at completing sonic 3 and Knukles. Can start test
# by simplely pressing a button. Planning to added more features such as a graphical
# display of all entities and thier current states through sprites
# ______________________________________________________________________________
#   The main builds the tkinter gui and sets the functions to be called when one
# of the buttons is pressed
def main():
    root = Tk()

    # Creates frame
    frame = Frame(root, width=100, height=50)
    frame.pack()

    # Creates start buttons
    start_bttn = Button(root, text="Start Tests with no data", command=begin_test)
    start_bttn.pack()
    button.append(start_bttn)

    # Creates load button
    load_bttn = Button(root, text="Start tests with data", command=lambda: load_gen(root))
    load_bttn.pack()
    button.append(load_bttn)

    #   Creates and execute thread responsible for capturing data from game screen in concurence
    # with the testing code
    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    stat_thread.start()

    root.mainloop()

# _____________________________________________________________________________
#   Function that loads the data specfied by the user and sends it off
# to the begin_test function
# Passes:
#       root: the root of the tkinter gui. Needed to create file dialog
def load_gen(root):

    answer = filedialog.askopenfilename(parent=root, initialdir=os.getcwd(),
    title="Please select a folder")

    generation = filehandler.load_data(answer)

    begin_test(generation)

# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities die or
# complete the game. After every entitiy is dead the entire generations state is
# saved in a pickle file denoted Raw.
#   Need to added functionality to determine if the entity wins the game
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
def begin_test(gen=[]):

    button[0].config(state="disabled")
    button[1].config(state="disabled")
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
