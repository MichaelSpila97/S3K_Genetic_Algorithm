import tkinter
import gdv

class Test_GUI:

    def __init__(self):
        self.root = tkinter.Tk()

        ld_lam = self.load_data()

        self.ndtrain_button = tkinter.Button(self.root, text="No Data Training", command=self.request_training)
        self.ldtrain_button = tkinter.Button(self.root, text="Load Data Training", command=ld_lam)

        self.score_label = tkinter.Label(self.root, text=f'Score: {gdv.curr_score}')
        self.ring_label = tkinter.Label(self.root, text=f'Rings: {gdv.curr_rings}')
        self.lives_label = tkinter.Label(self.root, text=f'Lives: {gdv.curr_lives}')
        self.act_label = tkinter.Label(self.root, text=f'Act: {gdv.curr_act}')

        self.obj_list = [self.score_label, self.ring_label, self.lives_label,
                        self.act_label, self.ndtrain_button, self.ldtrain_button]
        self.packer()

        self.queue = gdv.gui_func_qu
        self.queue_handler()
        self.root.mainloop()

    def packer(self):
        for obj in self.obj_list:
            obj.pack()

    def queue_handler(self):
        if not self.queue.empty():
            while not self.queue.empty():
                thread_func = self.queue.get()

                if thread_func == "change_labels_texts":
                    self.change_labels_texts()

        self.root.after('100', self.queue_handler)

    def change_labels_texts(self):
        labels = self.getLabels()

        labels[0].config(text=f'Score: {gdv.curr_score}')
        labels[1].config(text=f'Rings: {gdv.curr_rings}')
        labels[2].config(text=f'Lives: {gdv.curr_lives}')
        labels[3].config(text=f'Act: {gdv.curr_act}')

    def toggle_buttons_state(self):
        buttons = self.getButtons()

        for button in buttons:
            if button.state == "normal":
                button.config(state="disabled")
            elif button.state == "disabled":
                button.config(state="normal")

    def request_training(self, gen=[]):
        pass

    def load_data(self):
        data = []

        self.request_training(data)

    def getRoot(self):
        return self.root

    def getButtons(self):
        return [self.ndtrain_button, self.ldtrain_button]

    def getLabels(self):
        return [self.score_label, self.ring_label, self.lives_label, self.act_label]
