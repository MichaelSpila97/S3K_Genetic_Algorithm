from tkinter import *
from tkinter import filedialog

import brain
import entity
import filehandler
import time
import os
import copy
import threading

button = []

def main():
    root = Tk()

    frame = Frame(root, width=100, height=50)
    frame.pack()

    start_bttn = Button(root, text = "Start Tests with no data", command = begin_test)
    start_bttn.pack()

    button.append(start_bttn)

    load_bttn = Button(root, text = "Start tests with data", command = lambda: load_gen(root))
    load_bttn.pack()

    button.append(load_bttn)

    stat_thread = threading.Thread(target = brain.get_core_stats, daemon = True)
    stat_thread.start()

    root.mainloop()

def load_gen(root):

    my_filetypes = [('allfiles', '.*')]

    answer = filedialog.askopenfilename(parent= root, initialdir = os.getcwd(),
    title = "Please select a folder")

    generation  =  filehandler.load_data(answer)


    begin_test(generation)

def begin_test(gen = []):

    button[0].config(state = "disabled")
    button[1].config(state = "disabled")
    print('Before sleep')
    time.sleep(2)

    if gen:

        for x in gen:
            x.play_game()
            print(x)

    else:

        while brain.curr_lives > 0:
            ent = copy.deepcopy(entity.Entity())
            ent.play_game()
            print(str(ent))
            gen.append(copy.deepcopy(ent))
            del ent

    filehandler.save_data(gen, 'entity_data/Generation_0/Raw_gen_0')


if __name__ == '__main__':
    main()
