from tkinter import *

import eyes
import brain

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

    labels = [score_L, ring_L, live_L, act_L]

    root.after('500', update_core_stats, root, labels)
    root.mainloop()

def update_core_stats(root, labels):

    if brain.gameStarted():
        updated_score = eyes.score_grab()
        updated_rings = eyes.ring_grab()
        updated_lives = eyes.live_grab()

        labels[0].configure (text = 'Current Score: ' + str(brain.validate_score(updated_score)))
        labels[1].configure (text = 'Current Rings: ' + str(brain.validate_rings(updated_rings)))
        labels[2].configure (text = 'Current Lives: ' + str(brain.validate_lives(updated_lives)))
        labels[3].configure (text = str(brain.validate_act()))

    root.after('500', update_core_stats,root, labels)
if __name__ == '__main__':
    main()
