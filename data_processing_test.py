import trainingdriver as td
import src.handlers.filehandler as fh

gen_file_path = 'entity_data/Generation_0/Raw_Gen_0.pickle'
# This file servers the purpose of running the process_data() fuction, in trainingdriver.py,
# outside of training for debuging purpose of process_data() and all functions
# in the entity_handler and its sub_handlers
# ------------------------------------------------------------------------
# NOTE: MUST HAVE ENTITY DATA GENERATED ALREADY BEFORE RUNNING THIS FILE
# ------------------------------------------------------------------------
# Simply enter the file path to the raw data of the generation you want
# to use to test the process_data fuction and then run this file.
#
# You should get outputs in the console of the entire process with no errors
# if it works correctly.

def main():
    test_process_data(gen_file_path)

# ______________________________________________________________________________
#   Function test the process data functinon with data specfied by paramater of load data
# in this function
def test_process_data(data_loaction):
    gen = fh.load_data(data_loaction)
    td.process_data(gen, 10)


if __name__ == '__main__':
    main()
