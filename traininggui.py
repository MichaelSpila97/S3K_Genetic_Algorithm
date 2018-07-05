import tkinter
from tkinter import filedialog
import os
import threading

import gdv
import trainingdriver
import filehandler


class GUI:

    def __init__(self):
        self.root = tkinter.Tk()

        # No-Data Training Button and Load_data Training Button
        self.ndtrain_button = tkinter.Button(self.root, text="No Data Training", command=self.request_training)
        self.ldtrain_button = tkinter.Button(self.root, text="Load Data Training", command=self.load_data)

        # Statistics Labels
        self.score_label = tkinter.Label(self.root, text=f'Score: {gdv.curr_score}')
        self.ring_label = tkinter.Label(self.root, text=f'Rings: {gdv.curr_rings}')
        self.lives_label = tkinter.Label(self.root, text=f'Lives: {gdv.curr_lives}')
        self.act_label = tkinter.Label(self.root, text=f'{gdv.curr_act}')

        #   The Radio Buttons for deciding between Continuous Traning and Non-Continuous Training and
        # the variable the buttons will modifying when they are pressed on
        self.iscontinuous = tkinter.IntVar()
        self.conrb = tkinter.Radiobutton(self.root, text='Continuous Traning', variable=self.iscontinuous,
        value=1, command=self.radio_selection)
        self.noncrb = tkinter.Radiobutton(self.root, text='Non-Continuous Training', variable=self.iscontinuous,
        value=0, command=self.radio_selection)

        #   Object List for the packer method to use when packing all object into the GUI
        self.obj_list = [self.score_label, self.ring_label, self.lives_label,
                        self.act_label, self.ndtrain_button, self.ldtrain_button,
                        self.conrb, self.noncrb]
        self.packer()

        #   Queue and method to handle quene request are initlized here
        self.queue = trainingdriver.gui_func_qu
        self.gui_request_handler()

        self.root.mainloop()

    #   Method packs all GUI Objects
    def packer(self):
        for obj in self.obj_list:
            obj.pack()

    #       Method handles the request that come in to the self.queue
    # Request Supported:
    #                  1) Updating Text On gui
    #                  2) Toggling Buttons State
    def gui_request_handler(self):
        if not self.queue.empty():
            while not self.queue.empty():
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
        labels[3].config(text=f'Act: {gdv.curr_act}')

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
    # passed inStatNumberMaps.act_e_map
    def request_training(self, gen=[]):
        print('request testing')
        training_thread = threading.Thread(target=trainingdriver.begin_training, args=[gen], daemon=True)
        training_thread.start()

    #   Method that loads data, in the .pickle format, that the user chooses
    def load_data(self):
        data = []

        answer = filedialog.askopenfilename(parent=self.root, initialdir=os.getcwd(),
        title="Please select a folder")

        data = filehandler.load_data(answer)
        self.request_training(data)

    # ---------------------------------------Getter Methods-----------------------------------------------
    def getRoot(self):
        return self.root

    def getButtons(self):
        return [self.ndtrain_button, self.ldtrain_button]

    def getLabels(self):
        return [self.score_label, self.ring_label, self.lives_label, self.act_label]

    def getIsContinuous(self):
        return self.iscontinuous.get()