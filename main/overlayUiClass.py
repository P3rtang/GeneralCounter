# open child window with the current value of the chosen Counter object
from tkinter import *
import CounterReadClass as cR


class OverlayUi:
    def __init__(self, main_ui):
        self.main_ui = main_ui

        self.overlay = Tk()
        self.overlay_count = Label(self.overlay,
                                   text=str(self.main_ui.counter.value),
                                   font=self.main_ui.font[75],
                                   bg=self.main_ui.configs[self.main_ui.configNmr][2])
        self.overlay_count.pack()
        # make windowless
        self.overlay.overrideredirect(True)

    def change_counter(self, _event):
        self.overlay.attributes('-transparentcolor', '')
        self.main_ui.gui2.root.attributes('-transparentcolor', '')

        self.overlay_count.config(bg=self.main_ui.configs[self.main_ui.configNmr][2])
        self.main_ui.gui2.chance.config(bg=self.main_ui.configs[self.main_ui.configNmr][2])

        if self.main_ui.configs[self.main_ui.configNmr][0]:
            self.overlay.attributes('-transparentcolor', self.overlay_count['bg'])
            self.main_ui.gui2.root.attributes('-transparentcolor', self.main_ui.gui2.chance['bg'])

        self.overlay_count.config(fg=self.main_ui.configs[self.main_ui.configNmr][1])
        self.main_ui.gui2.chance.config(fg=self.main_ui.configs[self.main_ui.configNmr][1])
        # roll over to the next config for next click
        self.main_ui.configNmr += 1
        self.main_ui.configNmr %= len(self.main_ui.configs)

    def close_overlay(self, _event):
        self.main_ui.save()
        self.overlay.destroy()
        self.main_ui.gui2.root.withdraw()


if __name__ == '__main__':
    root = Tk()
    counters = cR.CounterRead('..\\saves\\counters.txt').get_list()
    import UI
    root_ui = UI.Ui(root, counters)
    overlay_test = OverlayUi(root_ui)

    root.mainloop()
