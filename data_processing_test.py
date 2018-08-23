import trainingdriver as td
import src.handlers.filehandler as fh

gen_file_path = 'entity_data/Generation_0/Raw_Gen_0.pickle'
# Used for the independent testing of the process_data() function and all functions
# that it uses
# ------------------------------------------------------------------------
# NOTE: MUST HAVE ENTITY DATA GENERATED ALREADY BEFORE RUNNING THIS FILE
# ------------------------------------------------------------------------
# Enter the file path of the raw entity data you want to use in this test in
# the gen_file_path variable. Then simply run the file to begin the test.

def main():
    test_process_data(gen_file_path)

def test_process_data(data_loaction):
    gen = fh.load_data(data_loaction)
    td.process_data(gen, 10)


if __name__ == '__main__':
    main()
