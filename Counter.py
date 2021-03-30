import CounterReadClass as cR
import CounterClass as cC
import UI as UI
import tkinter as tk
from pynput.keyboard import Listener, KeyCode, Key


def on_release(event):
    if gui.selection != None:
        # check for which key has been pressed and update counter object accordingly
        if event == KeyCode(char='+') or event == Key.space:
            gui.counter.value += gui.counter.jump
            gui.update_gui_chance()
        elif event == KeyCode(char='-'):
            gui.counter.value -= gui.counter.jump
            gui.update_gui_chance(dec=True)
        elif event == KeyCode(char='/'):
            gui.update_gui_chance(chain_lost=True)
        gui.score.config(text=gui.counter.value, font=gui.font[75])
        gui.overlayCount.config(text=gui.counter.value, font=gui.font[75])


counters = cR.CounterRead('counters.txt')           # string with counter objects read by CounterRead class from 'counters.txt'
counterList = []                                    # list to store counter objects in
# making counter object from the read line and storing in counterList
for line in counters:
    item = line.split(' ')                          # individual characteristics of counter object are separated by spaces in the txt file

    # check whether the read line has actual text in it (because the last line of the txt file is empty at all times
    if item[0]:
        counterList.append(cC.Counter(*item))   # counter needs 4 arguments and they are stored from pos 0 to 4
        # TODO: the making of the methods list needs to be implemented here as well

root = tk.Tk()                                      # start main window

gui = UI.Ui(root, counterList)                      # start the UI class to populate the main root

# listener for keyboard events
listener = Listener(on_release=on_release)
listener.start()
listener.wait()

root.mainloop()
listener.stop()
