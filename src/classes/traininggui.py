import tkinter
from tkinter import ttk
from tkinter import filedialog, messagebox
import tkinter.font as font

import os
import threading

import trainingdriver
from ..gdmodules import gdv
from src.handlers import filehandler

class GUI:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('600x300+700+0')

        self.root.title("S3K Genetic Algorithm")
        self.init_labels()
        self.init_buttons()
        self.init_entry()

        #   Object List for the packer method to use when packing all object into the GUI
        self.obj_list = [self.score_label, self.ring_label, self.lives_label,
                        self.act_label, self.ent_label, [self.entity_num_L, self.entity_num_E],
                        [self.ent_rp_L, self.ent_rp_E],
                        [self.conRB, self.noncRB],
                        [self.ndtrain_button, self.ldtrain_button, self.replay_button]]

        self.create_grid()

        #   Queue and method to handle quene request are initlized here
        self.queue = trainingdriver.gui_func_qu
        self.gui_request_handler()

        self.root.mainloop()

# ---------------------------------------Sub Init Methods-----------------------------------------------
    def init_labels(self):
        statfont = font.Font(family='Helvetica', size=20, weight='bold')

        # Display Statistic Labels
        self.score_label = ttk.Label(self.root, text=f'Score: {gdv.curr_score}', font=statfont)
        self.ring_label = ttk.Label(self.root, text=f'Rings: {gdv.curr_rings}', font=statfont)
        self.lives_label = ttk.Label(self.root, text=f'Lives: {gdv.curr_lives}', font=statfont)
        self.act_label = ttk.Label(self.root, text=f'{gdv.curr_act}', font=statfont)
        self.ent_label = ttk.Label(self.root, text=f'', font=statfont)

        # Entry Box Labels
        self.entity_num_L = ttk.Label(self.root, text='Entities Per Generation: ')
        self.ent_rp_L = ttk.Label(self.root, text='Entity to Replay: ')

    def init_buttons(self):

        # Radio Buttons
        self.iscontinuous = tkinter.IntVar()
        self.conRB = ttk.Radiobutton(self.root, text='Continuous Traning',
                    variable=self.iscontinuous, value=1,
                    command=self.radio_selection)

        self.noncRB = ttk.Radiobutton(self.root, text='Non-Continuous Training',
                    variable=self.iscontinuous, value=0,
                    command=self.radio_selection)

        # Regular Buttons
        self.ndtrain_button = ttk.Button(self.root, text="No Data Training",
                                            command=self.request_training)
        self.ldtrain_button = ttk.Button(self.root, text="Load Data Training",
                                            command=self.load_data)
        self.replay_button = ttk.Button(self.root, text="Replay Entity",
                                            command=lambda: self.load_data(replay=True))

    def init_entry(self):
        # Entry for the number of entities that comprise one generation
        self.entity_num_E = ttk.Entry(self.root)
        self.entity_num_E.insert(2, 10)

        # Entry that recivie the identification number for an entity that will replay
        # its actions
        self.ent_rp_E = ttk.Entry(self.root)

# ---------------------------------------Other Methods-----------------------------------------------
    #   Method packs all GUI Objects
    def create_grid(self):
        for row_count, obj in enumerate(self.obj_list):
            if isinstance(obj, list):
                for column_count, item in enumerate(obj):
                    item.grid(row=row_count, column=column_count)
            else:
                obj.grid(row=row_count, column=1)

    #       Method handles the request that come in to the self.queue
    # Request Supported:
    #                  1) Updating Text On gui
    #                  2) Toggling Buttons State
    def gui_request_handler(self):
        if not self.queue.empty():

            request = self.queue.get()

            if request == 'Update Texts':
                self.change_labels_texts()

            elif request == 'Toggle Button':
                self.toggle_buttons_state()

        self.root.after('100', self.gui_request_handler)

    #   Method that handles the updating of text in each of the GUI Labels
    # when a request is made
    def change_labels_texts(self):
        labels = self.getLabels()

        labels[0].config(text=f'Score: {gdv.curr_score}')
        labels[1].config(text=f'Rings: {gdv.curr_rings}')
        labels[2].config(text=f'Lives: {gdv.curr_lives}')
        labels[3].config(text=f'{gdv.curr_act}')
        labels[4].config(text=f'Current Entity Playing: {gdv.curr_entity}')

    #   Method that handles the chanining of state of the two regular button when
    # a request is made
    def toggle_buttons_state(self):
        buttons = self.getButtons()

        for button in buttons:
            state = str(button["state"])
            if state == "normal":
                button.config(state="disabled")
            elif state == "disabled":
                button.config(state="normal")

    #   Method sets the global Test Driver continue_training varibale to the value of
    # self.iscontinuous
    def radio_selection(self):
        trainingdriver.continue_training = self.getIsContinuous()

    #   Method that starts a thread and begins the training of entities
    # Passes:
    #           gen: a list of entities defaults to an empty list if no lists are
    #                passed in
    def request_training(self, gen=None):
        gen = gen or []
        num_entity = 0

        # Trys to begin training and fails if user inputed a invaild number of entities
        try:
            num_entity = int(self.entity_num_E.get())
            if num_entity < 1 or num_entity > 10:
                raise ValueError
            training_thread = threading.Thread(target=trainingdriver.begin_training, args=[num_entity, gen], daemon=True)
            training_thread.start()

        except ValueError:
            messagebox.showerror("Error", "Inputed Invalid Value.\nPlease enter an positve non-zero Integer <= 10")

    #   Method that starts a thread that will replay an entiteis actions
    # Passes:
    #           gen: a list of entities
    def request_replay(self, gen):

        # Trys to begin replay of entities actions and fails if user inputed a invaild entity id
        try:
            entity_id = int(self.ent_rp_E.get())
            if entity_id < 0 or entity_id > len(gen) - 1:
                raise ValueError
            ent = gen[entity_id]

            replay_thread = threading.Thread(target=trainingdriver.replay_action, args=[ent], daemon=True)
            replay_thread.start()
        except ValueError:
            messagebox.showerror("Error", f"Inputed Invalid Value.\nPlease enter an Enitiy ID number from 0 to{len(gen  - 1)} ")

    #  Method that loads data, in the .pickle format, that the user chooses
    # Passes:
    #         replay: A boolean value that decides weather data was being loaded for
    #                 replaying an entities actions
    def load_data(self, replay=False):
        data = []

        answer = filedialog.askopenfilename(parent=self.root, initialdir=os.getcwd(),
        title="Please select a folder")

        data = filehandler.load_data(answer)
        if replay:
            self.request_replay(data)
        else:
            self.request_training(data)

    # ---------------------------------------Getter Methods-----------------------------------------------
    def getRoot(self):
        return self.root

    def getButtons(self):
        return [self.ndtrain_button, self.ldtrain_button, self.replay_button]

    def getLabels(self):
        return [self.score_label, self.ring_label, self.lives_label, self.act_label, self.ent_label]

    def getIsContinuous(self):
        return self.iscontinuous.get()
