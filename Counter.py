import CounterReadClass as CR
import CounterClass as CC
import UI as UI
import tkinter as tk

counters = CR.CounterRead('counters.txt')           # string with counter objects read by CounterRead class from 'counters.txt'
counterList = []                                    # list to store counter objects in
# making counter object from the read line and storing in counterList
for line in counters:
    item = line.split(' ')                          # individual characteristics of counter object are separated by spaces in the txt file

    # check whether the read line has actual text in it (because the last line of the txt file is empty at all times
    if item[0]:
        counterList.append(CC.Counter(*item[:4]))   # counter needs 4 arguments and they are stored from pos 0 to 4
        # TODO: the making of the methods list needs to be implemented here as well

root = tk.Tk()                                       # start main window

gui = UI.Ui(root, counterList)                      # start the UI class to populate the main root

root.mainloop()                                     # loop
