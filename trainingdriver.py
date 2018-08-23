import threading
import queue
import os

from src.classes import entity, traininggui
from src.handlers import filehandler, entity_handler, window_handler
from src.gdmodules import gdv
from src.buttonpress import load_state

gui_func_qu = queue.Queue(maxsize=5)
continue_training = 0
entity_playing = ''

# ______________________________________________________________________________
# This file is responsible for:
#       1) Launching the game window in the correct place on screen
#       2) Lauching the Training GUI
#       3) Handeling the Training process of each generation
#       4) Processing a generation's data
#       5) Automating the training process for multiple generation
# ______________________________________________________________________________
#   The main creates and executes the thread responsible for capturing data from
# the game screen, calls the window handler to lauch the game windows, and Lauches
# the Training GUI
def main():

    # Creates and starts thread responsible for obtaining in game data
    stat_thread = threading.Thread(target=gdv.get_core_stats, daemon=True)
    stat_thread.start()

    window_handler.setup_game()

    # Launches the Training GUI
    traininggui.GUI()

# Function that replays the passed in entity's actions
def replay_action(ent):
    ent.resurrect()
    ent.play_game()

# ______________________________________________________________________________

# This function handles the training of an generation that is either passed in
# or created inside this function. Passes the generation to the process data
# method once training is finished for a generation
def begin_training(num_of_entities, gen=None):
    global entity_playing

    no_entity_data_dir = not os.path.exists(f'{os.getcwd()}/entity_data')

    if no_entity_data_dir:
        print('Making entity_data dir...')
        os.mkdir(f'{os.getcwd()}/entity_data')

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
            entity_playing = entities.getName()
            print(f'This entity is playing: {entity_playing}')
            entities.play_game()

    #       Else need to create a variable number of new entities, form num_of_entities,
    # that will compose generation 0
    else:
        print(f'Generation {gen_num} training has begun:\n')
        while num_of_entities > 0:

            ent = entity.Entity(name=f'G0E{total_entities - (num_of_entities - 1)}')
            entity_playing = ent.getName()
            print(f'This entity is playing: {entity_playing}')
            gdv.reset_stats()
            ent.play_game()
            gen.append(ent)
            num_of_entities -= 1

    no_current_generation_dir = os.path.exists(f'{os.getcwd()}/entity_data/Generation_{gen_num}')

    if no_current_generation_dir:
        os.mkdir(f'{os.getcwd()}/entity_data/Generation_{gen_num}')

    filehandler.save_data(gen, f'entity_data/Generation_{gen_num}/Raw_Gen_{gen_num}')

    print(f'Generation {gen_num} training has ended\n')

    gui_func_qu.put('Toggle Button')

    process_data(gen, total_entities)
# ______________________________________________________________________________
# This function handles:
#        1) The cleaning of each entities data in the generation
#        2) The evaulation of each entities data in the generation
#        3) The creatation of the next generations from the current generations
#           data
# This function will either save the data and quit training all together or pass
# the new generations data to the begin_training function.
def process_data(gen, num_of_entities):
    gen_num = gen[0].getGeneration()
    print(f'\nProcessing Generation {gen_num} data...\n')

    # Cleans the data
    entity_handler.clean_dna(gen)
    clean_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Clean_gen_{gen_num}.pickle')

    # Evaluates entities for fitness
    entity_handler.eval_entity(clean_gen)
    eval_gen = filehandler.load_data(f'entity_data/Generation_{gen_num}/Eval_gen_{gen_num}.pickle')

    # Prints out each entities from the fittess to least fit
    eval_gen.sort(key=lambda fit: fit.getFitness(), reverse=True)
    print(f'ENTITIES OF GENERATION {gen_num}:\n')
    for count, ent in enumerate(eval_gen):
        print(f'{count}: {ent}')

    # Creates Offspring for next generation
    entity_handler.reproduce(eval_gen, num_of_entities)

    #   Loads next Generation from offspring file and begins next training session
    # if continuous training was choosen
    if continue_training == 1:
        offspring = filehandler.load_data(f'entity_data/Generation_{gen_num}/Offspring_gen_{gen_num}.pickle')
        gen_num = offspring[0].getGeneration()

        print(f'Movining on to Generation {gen_num} training\n')
        gdv.reset_stats()

        begin_training(num_of_entities, offspring)


# ______________________________________________________________________________
if __name__ == '__main__':
    main()
