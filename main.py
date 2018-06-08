from tkinter import *

import eyes
import brain
import entity
import pickle
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

def init_test():
    thread = threading.Thread(target = begin_test, daemon = True)
    thread.start()

def begin_test():
    if brain.curr_lives != 0:
        num_entities = brain.curr_lives
        generation = []
        while(num_entities > 0):
            print(num_entities)
            new_entity = entity.Entity()
            entity_name = f'ent_{num_entities}'
            new_entity.play_game()

            generation.append(new_entity)

            pickle_out = open(f'{entity_name}.pickle',"wb")
            print('Saving entity.....')
            pickle.dump(new_entity, pickle_out)
            pickle_out.close()
            print('Entity saved')
            num_entities = brain.curr_lives

        print('Saving generation')
        pickle_out = open(f'gen.pickle',"wb")
        pickle.dump(generation ,pickle_out)
        pickle.close
        print('Generation saved')

if __name__ == '__main__':
    main()
