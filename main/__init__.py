import tkinter as tk
from pygame import mixer
import time
import keyboard
import threading
import queue
from .UI import Ui


def mix_play(file):
    mixer.music.load(f'{file}')
    mixer.music.play()


class Threading:
    def __init__(self, this):
        self.keyboard_thread = threading.Thread(target=keyboard.on_release,
                                                args=(lambda x: this.on_release(x), ))
        self.keyboard_thread.setDaemon(True)
        self.keyboard_thread.start()

        self.main_thread = threading.Thread(target=this.run)
        self.main_thread.run()


class StartCounter:
    def __init__(self):
        from .CounterRead import CounterRead
        self.root = tk.Tk()
        self.cur_time = time.time()

        self.keyboard_queue = queue.Queue()

        # string with counter objects read by CounterRead class from './saves/counters.txt'
        self.counters = CounterRead('./saves/counters.txt').get_list()

        mixer.init()

        self.gui = UI.Ui(self.root, self.counters)

        self.threads = Threading(self)
        self.threads.keyboard_thread.join()

    def run(self):
        while True:
            try:
                if self.cur_time != time.time():
                    change = time.time() - self.cur_time
                    self.cur_time = time.time()
                    if not self.gui.is_paused():
                        self.gui.counter.active_time += change

                    self.gui.update_time()
                if self.gui.counterList.curselection():
                    dec = False
                    try:
                        # data in the queue is a number referring to a keyboard input see on_release() for incoming data
                        data = self.keyboard_queue.get(block=False)
                        if data == 13:
                            self.gui.unpause_run_time()
                            self.gui.counter.value += self.gui.counter.jump
                            # play clicking sound as feedback
                            mix_play('./bin/mouse-click-clicking-single-click.wav')
                        elif data == 12:
                            self.gui.unpause_run_time()
                            self.gui.counter.value -= self.gui.counter.jump
                            # play the reverse of the clicking sound as feedback
                            mix_play('./bin/mouse-click-clicking-reverse-click.wav')
                            # argument for gui.update_gui_chance that indicates that the counter has decreased
                            dec = True
                        # show or hide the overlays
                        elif data == 9:
                            self.gui.toggle_counter_overlay()
                        elif data == 43:
                            self.gui.overlay.change_overlay_colours('#FF0000', '#000000', True)

                        # esc is used to disabled all controls
                        # keylogger is disabled until esc is pressed again
                        elif data == 1:
                            # save when disabling controls
                            # in the event the window is forgotten when shutting down the PC
                            self.gui.save()
                            # either disable or re-enable the controls
                            if self.gui.is_disabled() and self.gui.is_in_focus():
                                self.gui.unpause_run_time()
                                self.gui.enable()
                            else:
                                self.gui.disable()
                                self.gui.pause_run_time()

                        self.gui.last_input_time = time.time()
                    except queue.Empty:
                        if time.time() - self.gui.last_input_time > self.gui.pause_interval:
                            self.gui.pause_run_time()

                    if not self.gui.is_disabled() and not self.gui.is_menu_opened \
                            and not self.gui.counter.value == 'none selected':
                        # update the active counters to the current value
                        self.gui.score.config(text=self.gui.counter.value, font=self.gui.font[75])
                        self.gui.overlay.update(self.gui.counter.value)
                        self.gui.overlay2.update(UI.method_get_chance(self.gui.counter.method_id,
                                                                      self.gui.counter.odds,
                                                                      self.gui.counter.value))
                else:
                    try:
                        self.keyboard_queue.get(block=False)
                    except queue.Empty:
                        pass
                # update main window
                self.root.update()
                time.sleep(1 / self.gui.frame_rate)
            # TODO: remove this except clause that catches the program closing in the middle of the while loop
            except tk.TclError as e:
                print(e)
                exit(f'\nApplication Closed\nCounters Saved')

    # listener for keystrokes are handled by keyboard listener so the app can work when not in focus
    def on_release(self, event):
        # check for which key has been pressed and update counter object accordingly
        if not self.gui.is_disabled() or event.scan_code in [1, 9]:
            self.keyboard_queue.put(event.scan_code)
