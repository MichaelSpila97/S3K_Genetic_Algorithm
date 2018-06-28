import tkinter
from tkinter import filedialog
import gdv
import os
import Test_Driver
import threading
import filehandler


class Test_GUI:

    def __init__(self):
        self.root = tkinter.Tk()

        self.ndtrain_button = tkinter.Button(self.root, text="No Data Training", command=self.request_training)
        self.ldtrain_button = tkinter.Button(self.root, text="Load Data Training", command=self.load_data)

        self.score_label = tkinter.Label(self.root, text=f'Score: {gdv.curr_score}')
        self.ring_label = tkinter.Label(self.root, text=f'Rings: {gdv.curr_rings}')
        self.lives_label = tkinter.Label(self.root, text=f'Lives: {gdv.curr_lives}')
        self.act_label = tkinter.Label(self.root, text=f'Act: {gdv.curr_act}')

        self.obj_list = [self.score_label, self.ring_label, self.lives_label,
                        self.act_label, self.ndtrain_button, self.ldtrain_button]
        self.packer()

        self.queue = Test_Driver.gui_func_qu
        self.gui_request_handler()
        self.root.mainloop()

    def packer(self):
        for obj in self.obj_list:
            obj.pack()

    def gui_request_handler(self):
        if not self.queue.empty():
            while not self.queue.empty():
                request = self.queue.get()

                if request == 'Update Texts':
                    print("Updating Text")
                    self.change_labels_texts()

                elif request == 'Toggle Button':
                    print("Toggling Buttons")
                    self.toggle_buttons_state()

        self.root.after('100', self.gui_request_handler)

    def change_labels_texts(self):
        labels = self.getLabels()

        labels[0].config(text=f'Score: {gdv.curr_score}')
        labels[1].config(text=f'Rings: {gdv.curr_rings}')
        labels[2].config(text=f'Lives: {gdv.curr_lives}')
        labels[3].config(text=f'Act: {gdv.curr_act}')

    def toggle_buttons_state(self):
        buttons = self.getButtons()

        for button in buttons:
            state = str(button["state"])
            if state == "normal":
                button.config(state="disabled")
            elif state == "disabled":
                button.config(state="normal")

    def request_training(self, gen=[]):
        print('request testing')
        training_thread = threading.Thread(target=Test_Driver.begin_training, args=[gen], daemon=True)
        training_thread.start()

    def load_data(self):
        data = []

        answer = filedialog.askopenfilename(parent=self.root, initialdir=os.getcwd(),
        title="Please select a folder")

        data = filehandler.load_data(answer)
        self.request_training(data)

    def getRoot(self):
        return self.root

    def getButtons(self):
        return [self.ndtrain_button, self.ldtrain_button]

    def getLabels(self):
        return [self.score_label, self.ring_label, self.lives_label, self.act_label]
