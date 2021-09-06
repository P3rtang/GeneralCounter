# open child window with the current value of the chosen Counter object
from tkinter import *


class overlayUI:
    def __init__(self, main_ui):
        self.mainUI = main_ui

        self.overlay = Tk()
        self.overlayCount = Label(self.overlay,
                                  text=str(self.mainUI.counter.value),
                                  font=self.mainUI.font[75],
                                  bg=self.mainUI.configs[self.mainUI.configNmr][2])
        self.overlayCount.pack()

        self.overlay.overrideredirect(True)  # windowless

        # self.overlay.bind("<*>", self.changeCounter)
        # self.overlay.bind("</>", lambda i=True: self.mainUI.gui2.update(self.mainUI.counter, chain_lost=i))

        # when escape is pressed with the overlay active close all the overlays (including the extra feature window)
        # self.overlay.bind("<Escape>", self.exitOverlay)

    def changeCounter(self, _event):
        self.overlay.attributes('-transparentcolor', '')
        self.mainUI.gui2.root.attributes('-transparentcolor', '')

        self.overlayCount.config(bg=self.mainUI.configs[self.mainUI.configNmr][2])
        self.mainUI.gui2.chance.config(bg=self.mainUI.configs[self.mainUI.configNmr][2])

        if self.mainUI.configs[self.mainUI.configNmr][0]:
            self.overlay.attributes('-transparentcolor', self.overlayCount['bg'])
            self.mainUI.gui2.root.attributes('-transparentcolor', self.mainUI.gui2.chance['bg'])

        self.overlayCount.config(fg=self.mainUI.configs[self.mainUI.configNmr][1])
        self.mainUI.gui2.chance.config(fg=self.mainUI.configs[self.mainUI.configNmr][1])
        # roll over to the next config for next click
        self.mainUI.configNmr += 1
        self.mainUI.configNmr %= len(self.mainUI.configs)

    def exitOverlay(self, _event):
        self.mainUI.save()
        self.overlay.destroy()
        self.mainUI.gui2.root.withdraw()
