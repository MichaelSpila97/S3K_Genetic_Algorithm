import pickle
# ______________________________________________________________________________
# File Handler
#   Contain functions responsible for saving and loading the state of
# generation. Probably extend its useablility to handle naming of files
# ______________________________________________________________________________

def save_data(data, filename):

    print(f'saving {filename}.pickle ')
    pickle_out = open(f'{filename}.pickle', "wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()
# ______________________________________________________________________________
def load_data(filename):

    pickle_in = open(f'{filename}', 'rb')
    data = pickle.load(pickle_in)
    return data
