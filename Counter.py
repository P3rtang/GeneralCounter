import tkinter as tk

from pygame import mixer
from pynput.keyboard import Listener, KeyCode, Key

import CounterClass as cC
import CounterReadClass as cR
import UI as UI

class Debugger:
    def __init__(self, root):

        self.main_objects = [x for x in root.winfo_children()]

        self.debugRoot = tk.Toplevel(root)

        self.objects = tk.Listbox(self.debugRoot, height=20, width=30, font=gui.font[20])
        print(self.main_objects)
        for x, y in enumerate(self.main_objects):
            self.objects.insert(x, y)

        self.objects.pack()

        self.objects.bind("<<ListboxSelect>>", self.selectListBox)

    def selectListBox(self, _event):
        selected_child = self.main_objects[self.objects.index('anchor')]
        if selected_child.type in gui.resizable:
            pass
        else:
            objects = [x for x in self.main_objects[self.objects.index('anchor')].winfo_children()]

            self.main_objects = objects


# listener for keystrokes are handled by keyboard listener so the app can work when not in focus
def on_release(event):
    global listener
    if gui.selection is not None:
        # check for which key has been pressed and update counter object accordingly
        if not gui.isDisabled():
            if event == KeyCode(char='+') or event == Key.space:
                mixer.music.play(1)
                gui.counter.value += gui.counter.jump
                gui.update_gui_chance()
            elif event == KeyCode(char='-'):
                gui.counter.value -= gui.counter.jump
                gui.update_gui_chance(dec=True)
            # reset the chain when using the pokemon extra feature
            elif event == KeyCode(char='/'):
                gui.update_gui_chance(chain_lost=True)
            # show or hide the overlays
            elif event == KeyCode(char='*'):
                gui.showCounter()
            elif event == KeyCode(char='#'):
                gui.changeCounter()
            # update the active counters to the current value
            gui.score.config(text=gui.counter.value, font=gui.font[75])
            gui.overlayCount.config(text=gui.counter.value, font=gui.font[75])
        # esc is used to disabled all controls so the previous keys can be used in other programs without changing the counter
        if event == Key.esc:
            # save when disabling controls in the event the window is forgotten when shutting down the PC
            gui.save()
            # either disable or re-enable the controls
            if gui.isDisabled() and gui.inFocus():
                gui.enable()
            else:
                gui.disable()

        elif event == Key.f1:
            debugger = Debugger(root)


counters = cR.CounterRead('./saves/counters.txt')   # string with counter objects read by CounterRead class from './saves/counters.txt'
counterList = []

mixer.init()
mixer.music.load('bin/mouse-click-clicking-single-click.mp3')                         # list to store counter objects in
# making counter object from the read line and storing in counterList
for line in counters:
    item = line.split(' ')                          # individual characteristics of counter object are separated by spaces in the txt file

    # check whether the read line has actual text in it (because the last line of the txt file is empty at all times
    if item[0]:
        counterList.append(cC.Counter(*item))       # counter needs 6 arguments and they are stored in multiple objects

root = tk.Tk()             # start main window

gui = UI.Ui(root, counterList)                      # start the UI class to populate the main root

# listener for keyboard events
listener = Listener(on_release=on_release)
listener.start()

root.mainloop()
listener.stop()
    
