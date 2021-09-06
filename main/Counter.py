import tkinter as tk
from pygame import mixer

import time
import keyboard
import threading
import queue

import CounterClass as cC
import CounterReadClass as cR
import UI as UI


class Debugger:
    def __init__(self, tk_root):
        debugger_toplevel = tk.Toplevel(tk_root)

        self.currentCounterInfo = tk.Label(debugger_toplevel, text=gui.counter)

        self.size = tk.Scale(debugger_toplevel, from_=10, to=50,
                             orient='horizontal', command=self.change_main_frame_size)
        # self.size.bind("<Button-1>", self.changeMainFrameSize)
        self.size.pack()

    def start(self):
        self.currentCounterInfo.pack()

    def change_main_frame_size(self, *_event):
        gui.counterList.config(height=int(self.size.get() / 2.75), width=self.size.get())
        gui.scoreFrame.config(height=int(self.size.get() * 7.5), width=self.size.get() * 7.5)


def mix_play(file):
    mixer.music.load(f'{file}')
    mixer.music.play()


def main(main_root, queue1):
    cur_time = time.time()
    keyboard_thread.join()
    while True:
        try:
            if cur_time != time.time():
                change = time.time() - cur_time
                cur_time = time.time()
                if not gui.isPaused():
                    gui.counter.active_time += change

                if cur_time - gui.timeLabel_change_state > 1 and gui.time_state == 'local_time':
                    gui.timeLabel.config(text=f'{time.strftime("%H:%M:%S")}')
                elif cur_time - gui.timeLabel_change_state > 1:
                    t = gui.counter.active_time
                    gui.timeLabel.config(text=f'{int(t//3600):02d}:{int(t//60%60):02d}'
                                              f':{int(t%60):02d}.{int((t-int(t))*100):02d}')
            if gui.isCounterSelected():
                dec = False
                try:
                    # data in the queue is a number referring to a keyboard input see on_release() for incoming data
                    data = queue1.get(block=False)
                    if data == 13:
                        gui.unpause_run_time()
                        gui.counter.value += gui.counter.jump
                        # play clicking sound as feedback
                        mix_play('../main/bin/mouse-click-clicking-single-click.mp3')
                    elif data == 12:
                        gui.unpause_run_time()
                        gui.counter.value -= gui.counter.jump
                        # play the reverse of the clicking sound as feedback
                        mix_play('../main/bin/mouse-click-clicking-reverse-click.mp3')
                        # argument for gui.update_gui_chance that indicates that the counter has decreased
                        dec = True
                    # show or hide the overlays
                    elif data == 9:
                        gui.toggle_counter_overlay()
                    elif data == 43:
                        UI.change_tk_Label_colours(gui.overlayCount, '#FF0000', '#000000', True)

                    # esc is used to disabled all controls
                    # keylogger is disabled until esc is pressed again
                    elif data == 1:
                        # save when disabling controls in the event the window is forgotten when shutting down the PC
                        gui.save()
                        # either disable or re-enable the controls
                        if gui.isDisabled() and gui.inFocus():
                            gui.unpause_run_time()
                            gui.enable()
                        else:
                            gui.disable()
                            gui.pause_run_time()

                    gui.last_input_time = time.time()
                except queue.Empty:
                    if time.time() - gui.last_input_time > gui.pause_interval:
                        gui.pause_run_time()

                if not gui.isDisabled():
                    # update the active counters to the current value
                    gui.update_gui_chance(dec=dec)
                    gui.score.config(text=gui.counter.value, font=gui.font[75])
                    gui.overlayCount.config(text=gui.counter.value, font=gui.font[75])

            # update main window
            main_root.update()
            time.sleep(1/gui.frame_rate)

        # TODO: remove this except clause that catches the program closing in the middle of the while loop
        except tk.TclError as e:
            print(e)
            exit(f'\nApplication Closed\nCounters Saved')


# listener for keystrokes are handled by keyboard listener so the app can work when not in focus
def on_release(event, queue1):
    # print(event.scan_code)
    if gui.isCounterSelected():
        # check for which key has been pressed and update counter object accordingly
        if not gui.isDisabled() or event.scan_code in [1, 9]:
            queue1.put(event.scan_code)


# string with counter objects read by CounterRead class from './saves/counters.txt'
counters = cR.CounterRead('.\\saves\\counters.txt')

# list to store counter objects in
counterList = []

mixer.init()
# making counter object from the read line and storing in counterList
for line in counters:
    # individual characteristics of counter object are separated by spaces in the txt file
    item = line.split(' ')
    # check whether the read line has actual text in it
    # because the last line of the txt file is an empty string at all times
    if item[0]:
        print(item)
        counterList.append(cC.Counter(*item))       # counter needs 7 arguments and they are stored in multiple objects


root = tk.Tk()
gui = UI.Ui(root, counterList)
q = queue.Queue()

keyboard_thread = threading.Thread(target=keyboard.on_release, args=(lambda x: on_release(x, q), ))
keyboard_thread.setDaemon(True)
keyboard_thread.start()

main_thread = threading.Thread(target=main, args=(root, q))
main_thread.run()
