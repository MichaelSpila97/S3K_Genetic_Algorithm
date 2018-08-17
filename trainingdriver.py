import threading
import queue
import os
import win32gui
import win32con
import time

from src.classes import entity, traininggui
from src.handlers import filehandler, entity_handler
from src.gdmodules import gdv
from src.buttonpress import load_state
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

    #    Uncomment this function below and comment everthing else out if you just want
    # to test the process data function. Change paramater to data file you want evaluate
    # by process data function
    # -----------------------------------------------------------------------------------
    # test_process_data('entity_data/Generation_0/Raw_Gen_0.pickle')
    # -----------------------------------------------------------------------------------

    # Creates and starts thread responsible for obtaining ingame stats
    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    stat_thread.start()
    setup_game()
    # Builds Gui that displays in game stats and used to start test
    traininggui.GUI()


def replay_action(ent):
    ent.resurrect()
    ent.play_game()

# ______________________________________________________________________________
#   Function that runs each entities attempt until all of the entities complete their attempt.
# After every entitiy is done training the entire generations state is saved in a pickle file, denoted Raw,
# and is then set to be processed by the process data method
#
# Passes:
#       gen: the list that contains entities from a single generation. Is empty list if nothing is passed.
#       num_of_entities: Passes number of entities that will train

def begin_training(num_of_entities, gen=None):

    gen_num = 0
    total_entities = num_of_entities

    # Turns off Buttons so no more testing request can be made till testing is over
    gui_func_qu.put('Toggle Button')

    load_state()

    # If thier are entities in the gen list
    if gen:
        # Gets Generation number from entities for file and directory nameing purposes
        gen_num = gen[0].getGeneration()
        print(f'Generation {gen_num} training has begun:\n')
        for entities in gen:
            gdv.reset_stats()
            entities.play_game()

    #       Else need to create a variable number of new entities, form num_of_entities,
    # that will compose generation 0
    else:
        print(f'Generation {gen_num} training has begun:\n')
        while num_of_entities > 0:

            ent = entity.Entity(name=f'G0E{total_entities - (num_of_entities - 1)}')
            gdv.reset_stats()
            ent.play_game()
            gen.append(ent)
            num_of_entities -= 1

    os.mkdir(f'{os.getcwd()}/entity_data/Generation_{gen_num}')
    filehandler.save_data(gen, f'entity_data/Generation_{gen_num}/Raw_Gen_{gen_num}')

    print(f'Generation {gen_num} training has ended\n')

    gui_func_qu.put('Toggle Button')

    process_data(gen, total_entities)
# ______________________________________________________________________________
#   Function that process the newly generated generation data from a training session .
# It Cleans the data of errors, evaluated each entities data and fitness, and then
# creates the generation offsprigs. If continuous training was selected the function will
# proceed to start up a new game an begin training again. If it wasn't then training will be
# over.
#
# Passes:
#        gen = List that contains entities that belong to the same generation
#        gen_num: The number of the gneration that is being passed in.
def process_data(gen, num_of_entities):
    gen_num = gen[0].getGeneration()
    print(f'\nProcessing Generation {gen_num} data...\n')

    # Cleans Data
    entity_handler.clean_dna(gen)
    clean_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}.pickle')

    # Evaluates entities for fitness
    entity_handler.eval_entity(clean_gen)
    eval_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}.pickle')

    # Prints out entities from fittess to least fit
    eval_gen.sort(key=lambda fit: fit.getFitness(), reverse=True)
    print(f'ENTITIES OF GENERATION {gen_num}:\n')
    for count, ent in enumerate(eval_gen):
        print(f'{count}: {ent}')

    # Creates Offspring for next generation
    entity_handler.reproduce(eval_gen, num_of_entities)

    #   Loads next Generation from offspring file and begins next game if continuous training was
    # choosen
    if continue_training == 1:
        offspring = filehandler.load_data(f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}.pickle')
        gen_num = offspring[0].getGeneration()

        print(f'Movining on to Generation {gen_num} training\n')
        gdv.reset_stats()

        begin_training(num_of_entities, offspring)

# ______________________________________________________________________________
#   Function test the process data functinon with data specfied by paramater of load data
# in this function
def test_process_data(data_loaction):
    gen = filehandler.load_data('entity_data/Generation_0/Raw_Gen_0.pickle')
    process_data(gen, 10)


def setup_game():
        segamegadriveclassics = "SEGAGameRoom.exe"
        os.chdir("E:\Steam\steamapps\common\Sega Classics")
        gamethread = threading.Thread(target=lambda: os.system(segamegadriveclassics), daemon=True)

        gamethread.start()

        time.sleep(5)
        window = win32gui.FindWindow(None, 'SEGA Mega Drive Classics')

        left, top, right, bottom = win32gui.GetWindowRect(window)

        win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 646, 509, 0)

        left, top, right, bottom = win32gui.GetWindowRect(window)

        print(f'left: {left}')
        print(f'top: {top}')
        print(f'right: {right}')
        print(f'bottom: {bottom}')


# ______________________________________________________________________________
if __name__ == '__main__':
    main()
