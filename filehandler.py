import pickle
#_______________________________________________________________________________________________________________________________
#File Handler
#   Contain functions responsible for saving and loading the state of
# generation. Probably extend its useablility to handle naming of files
#_______________________________________________________________________________________________________________________________

def save_data(data , filename):

    print('saving data')
    pickle_out = open(f'{filename}.pickle', "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()
#_______________________________________________________________________________________________________________________________   
def load_data(filename):

    pickle_in = open(f'{filename}', 'rb')
    data = pickle.load(pickle_in)
    return data
