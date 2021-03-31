import tkinter as tk

from pynput.keyboard import Listener, KeyCode, Key

from pygame import mixer

import CounterClass as cC
import CounterReadClass as cR
import UI as UI


# listener for keystrokes are handled by keyboard listener so the app can work when not in focus
def on_release(event):
    global disableControls
    if gui.selection is not None:
        # check for which key has been pressed and update counter object accordingly
        if not disableControls:
            if event == KeyCode(char='+') or event == Key.space:
                mixer.music.load('mouse-click-clicking-single-click.mp3')
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
                gui.selectCounter()
            # update the active counters to the current value
            gui.score.config(text=gui.counter.value, font=gui.font[75])
            gui.overlayCount.config(text=gui.counter.value, font=gui.font[75])
        # esc is used to disabled all controls so the previous keys can be used in other programs without changing the counter
        if event == Key.esc:
            # save when disabling controls in the event the window is forgotten when shutting down the PC
            gui.save()
            # either disable or re-enable the controls
            if disableControls:
                disableControls = False
                gui.score.config(text=gui.counter.value, font=gui.font[75])
                gui.overlayCount.config(text=gui.counter.value, font=gui.font[75])
            else:
                # change the label in the main window to reflect that controls are turned off
                gui.score.config(text='Controls\nDisabled', font=gui.font[45])
                disableControls = True
                # hide all overlays when disabling the controls
                gui.overlay.withdraw()
                gui.overlay2.withdraw()


disableControls = False
counters = cR.CounterRead('counters.txt')           # string with counter objects read by CounterRead class from 'counters.txt'
counterList = []                                    # list to store counter objects in
# making counter object from the read line and storing in counterList
for line in counters:
    item = line.split(' ')                          # individual characteristics of counter object are separated by spaces in the txt file

    # check whether the read line has actual text in it (because the last line of the txt file is empty at all times
    if item[0]:
        counterList.append(cC.Counter(*item))       # counter needs 6 arguments and they are stored in multiple objects

root = tk.Tk()                                      # start main window

gui = UI.Ui(root, counterList)                      # start the UI class to populate the main root

# listener for keyboard events
listener = Listener(on_release=on_release)
listener.start()
listener.wait()

mixer.init()
root.mainloop()
listener.stop()
