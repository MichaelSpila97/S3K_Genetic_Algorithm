from tkinter import *

import eyes
import brain
import entity
import pickle
import time
import threading

def main():
    root = Tk()

    frame = Frame(root, width=100, height=50)
    frame.pack()

    score_L = Label(root, text= "The Game Has not Started Yet")
    score_L.pack()

    ring_L = Label(root, text ='')
    ring_L.pack()

    live_L = Label(root, text ='')
    live_L.pack()

    act_L = Label(root, text = '')
    act_L.pack()

    bttn = Button(root, text = "Start Tests", command = init_test)

    bttn.pack()

    labels = [score_L, ring_L, live_L, act_L ,time_L]

    root.after('100', update_core_stats, root, labels, 0)
    root.mainloop()

def update_core_stats(root, labels , exec_num):

    if brain.gameStarted():

        exec_num = exec_num + 1

        updated_score = eyes.score_grab()
        updated_rings = eyes.ring_grab()
        updated_lives = eyes.live_grab()

        labels[0].configure (text = 'Current Score: ' + str(brain.validate_score(updated_score)))
        labels[1].configure (text = 'Current Rings: ' + str(brain.validate_rings(updated_rings)))
        labels[2].configure (text = 'Current Lives: ' + str(brain.validate_lives(updated_lives)))
        labels[3].configure (text = str(brain.validate_act()))

    root.after('100', update_core_stats,root, labels, exec_num)


def init_test():
    if brain.gameStarted():

        g_thread = threading.Thread(target = begin_test, daemon = True)
        g_thread.start()

def begin_test():

    while brain.curr_lives > 0:

            new_entity = entity.Entity(act_list = [])
            new_entity.play_game()

            pickle_out = open(f"entity_data/Gen_0/entity_{4 - (brain.curr_lives + 1)}.pickle", "wb")
            pickle.dump(new_entity, pickle_out)
            pickle_out.close()

            new_entity = None
            

if __name__ == '__main__':
    main()
