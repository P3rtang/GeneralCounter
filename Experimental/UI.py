import tkinter
from tkinter import *
from tkinter import messagebox
import time
import CounterClass as CC
import UImethods as UIM
import counterOptionClass as cOC
from win32api import GetSystemMetrics
from win32gui import GetWindowText, GetForegroundWindow
from PIL import ImageTk, Image


def dexnav_chance_inc(step, neg_chance, chain=0):
    if step <= 100:
        step_chance = step * 6 / 100 / 10000
    elif step <= 200:
        step_chance = ((step - 100) * 2 + 600) / 100 / 10000
    else:
        step_chance = (step - 200 + 800) / 100 / 10000

    if chain % 100 == 50:
        neg_chance *= (1 - step_chance) ** 5
    elif chain % 100 == 0 and chain != 0:
        neg_chance *= (1 - step_chance) ** 10
    else:
        neg_chance *= (1 - step_chance)
    return neg_chance


def dexnav_chance_dec(step, neg_chance, chain=0):
    if step < 100:
        step_chance = step * 6 / 100 / 10000
    elif step < 200:
        step_chance = ((step - 100) * 2 + 600) / 100 / 10000
    else:
        step_chance = (step - 200 + 800) / 100 / 10000

    if chain % 100 == 49:
        neg_chance /= (1 - step_chance) ** 5
    elif chain % 100 == 99 and chain != -1:
        neg_chance /= (1 - step_chance) ** 10
    else:
        neg_chance /= (1 - step_chance)
    return neg_chance


def highestId():
    with open('./saves/counters.txt') as saves:
        saves = saves.read()
    with open('./saves/archived.txt') as archive:
        archive = archive.read()

    highest_id = (saves + archive).count('\n')
    print(highest_id)
    return highest_id


class Ui:
    def __init__(self, tkRoot, saves, _gui_chance=None):
        # list to keep track of all resizable widgets to customize the layout
        self.resizable = []
        self.frame_rate = 120

        # all counters are in saves
        self.counters = saves

        # make secondary extra features window
        self.gui2 = UIM.UiMethods(self.counters)
        self.gui2.root.withdraw()

        # start index of selected counter as 0
        self.counterIndex = 0
        # active counter object
        self.counter = CC.Counter(0, 'None', 0)

        # flag to disable all events and keyboard listeners
        self.disabled_status = False

        # make al font sizes op to 100
        self.font = []
        for n in range(1, 101):
            self.font.append(("Helvetica", f"{n}", "bold"))
        self.fontCounter = self.font[75]

        self.selection = None

        # start tkinter, rootW is the main root
        self.rootW = tkRoot
        self.height = 15
        self.width = 75

        # configs stored as tuple of 3 elements
        # 1: transparent or not
        # 2: foreground color (color of the text)
        # 3: background color (best left white when using transparent
        self.configs = [(True, 'red', '#FF0001'), (True, '#5280e9', '#5280e8'), (False, 'black', 'white')]
        self.configNmr = 0
        # make body for easy addition and resizing in main window
        self.body = Frame(self.rootW)
        self.body.pack(fill='both')

        # list with all active counters
        # interact by clicking
        self.counterList = Listbox(self.body, width=self.width // 2 - 1, height=self.height - 1, font=self.font[24])

        # TODO: clicking in the window(listbox or outside) should deselect any counter
        # bind selecting a counter to listBoxSelect which in turn activates the counter object and refreshes the window
        self.counterList.bind("<<ListboxSelect>>", self.listBoxSelect)

        # gives a frame to store the label with; current time / time since opening counter (uptime)
        # change between the two options by clicking the time frame
        self.timeFrame = Frame(self.body, borderwidth=1, relief="sunken",
                               width=300, height=50)
        self.timeFrame.grid(row=0, column=1, rowspan=1, columnspan=2)
        self.timeFrame.pack_propagate(False)

        # Label with the actual current time / uptime of the selected counter
        self.timeLabel = Label(self.timeFrame, text=f'', font=self.font[24])
        self.timeLabel.pack(fill="both", expand=True)
        self.timeLabel.bind('<Button-1>', func=self.toggle_time_shown)
        self.time_state = 'local_time'
        self.timeLabel_change_state = time.time()

        self.last_input_time = time.time()
        self.pause_interval = 120
        self.paused_status = True

        # gives a frame to store the label with the count of the selected counter
        self.scoreFrame = Frame(self.body, borderwidth=1, relief="sunken",
                                width=300, height=280)
        self.scoreFrame.grid(row=1, column=1, rowspan=1, columnspan=2)
        self.scoreFrame.pack_propagate(False)

        # Label with the actual current count of the selected counter
        self.score = Label(self.scoreFrame, text='None Selected', font=self.font[24])
        self.score.pack(fill="both", expand=True)

        self.overlayCount = Label(self.rootW, text=0, font=self.font[75])

        select = Button(self.body, font=self.font[24], command=self.toggle_counter_overlay, text='SELECT')
        select.grid(row=2, column=1, pady=(5, 0), padx=10)
        delete = Button(self.body, font=self.font[24], command=self.delete_counter, text='DELETE')
        delete.grid(row=4, column=1, pady=5)
        new = Button(self.body, font=self.font[24], command=self.newCounter, text='NEW')
        new.grid(row=3, column=1, pady=(5, 0), ipadx=26)

        self.archive_image = ImageTk.PhotoImage(Image.open('./bin/archive2.png'))

        archive = Label(self.body, image=self.archive_image, width=60, height=60)
        archive.grid(row=4, column=2)
        archive.bind("<Button-1>", self.Archive)

        self.option_image = ImageTk.PhotoImage(Image.open('./bin/cog.png'))

        options = Label(self.body, image=self.option_image, width=60, height=60)
        options.grid(row=2, column=2)
        options.bind("<Button-1>", self.openMainOptions)

        self.delete_image = ImageTk.PhotoImage(Image.open('./bin/trashcan.png'))

        delete = Label(self.body, image=self.delete_image, width=60, height=60)
        delete.grid(row=3, column=2)
        delete.bind("<Button-1>", self.delete_counter)
        self.start()
        self.rootW.protocol("WM_DELETE_WINDOW", self.save_quit)

        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

        self.rootW.geometry(f'+{self.screen_width // 2 - 477}+{self.screen_height // 2 - 256}')
        self.rootW.bind("<Configure>", print('window size change...WIP'))

        self.overlay = Toplevel(self.rootW)

        self.overlayCount = Label(self.overlay,
                                  text=self.counter.value,
                                  font=self.font[75],
                                  bg='white')
        self.overlayCount.pack()

        self.overlay.overrideredirect(True)
        self.overlay.wm_attributes("-topmost", True)

        self.overlay.withdraw()

        # gui 2 for extra info specific to pokemon hunting
        self.overlay2 = Toplevel(self.rootW)
        # used in gui2
        self.chain = 0

        self.mainFrame = Frame(self.overlay2)
        self.mainFrame.pack()

        self.chance = Label(self.mainFrame, text=0, font=("Helvetica", "25"))
        self.chance.pack()

        self.overlay2.geometry('+0+122')

        self.overlay2.overrideredirect(True)  # windowless
        self.overlay2.wm_attributes("-topmost", True)

        # overlay 2

        self.overlay2.bind('<Button-1>', self.optionMenu)
        self.overlay2.withdraw()

    def isOverlayShown(self):
        if self.overlay.winfo_ismapped():
            return True
        return False

    def optionMenu(self, _counter):
        def applyOption():
            # changing the counter values
            self.chain = int(set_count.get()) if set_count.get() else self.chain
            self.chance.config(text=f'{float(self.chance["text"].split(" - ")[0]):.3f} - {self.chain}')

        def reset():
            self.chain = 0
            self.chance.config(text=f'{0:.3f}% - {self.chain}')
            option_menu.destroy()

        option_menu = Toplevel(self.overlay2)

        # reset the chance to zero with a button in the option menu
        reset_chance = Button(option_menu, text='Reset chance to 0', font=self.font[20], command=reset)
        reset_chance.pack()

        # set the chain length from an options menu opened when clicking on the widget
        Label(option_menu, text='set chain', font=self.font[20]).pack()
        set_count = Entry(option_menu, font=self.font[16], justify='center')

        set_count.pack()
        set_count.focus_force()

        button_frame = Frame(option_menu)
        button_frame.pack()

        cancel = Button(button_frame, text='CANCEL', font=self.font[16], command=option_menu.destroy)
        apply = Button(button_frame, text='APPLY', font=self.font[16], command=applyOption)

        cancel.grid(row=0, column=0, ipadx=8, sticky='w')
        apply.grid(row=0, column=1, ipadx=17, sticky='e')

    def update_gui_chance(self, dec=False, chain_lost=False, has_charm=False):
        # store the method for which values need to be calculated
        # cur_chance = self.counter.odds
        method = self.counter.method_id

        # updating the chain dependant on the input dec means decreasing and
        # any update with chain lost sets the chain to 0 (also used when starting the gui
        if chain_lost:
            self.chain = 0
        elif dec:
            self.chain -= 1
        else:
            self.chain += 1

        # normal random encounter with odds store in self.counter.odds method is stored in method_list
        if method == 0:
            cur_chance = 1 - (1 - 1 / self.counter.odds) ** self.counter.value
            self.chance.config(text=f'{round(cur_chance * 100, 3):.3f}%')

        # dexnav encounter with previous encounter odds stored in self.counter.odds
        elif method == 1:
            if not dec and not chain_lost:
                self.counter.odds = dexnav_chance_inc(self.counter.value, self.counter.odds, self.chain)

            if dec and not chain_lost:
                self.counter.odds = dexnav_chance_dec(self.counter.value, self.counter.odds, self.chain)

            self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}% - {self.chain}')

        # SOS encounters with previous encounter odds stored in self.counter.odds
        # this method works with rolls and is the base odds lifted to the power of the nr of rolls
        elif method == 2:
            rolls = 1
            neg_chance = 4095 / 4096

            if has_charm:
                rolls += 2

            if self.chain <= 10:
                pass
            elif self.chain <= 20:
                rolls += 4
            elif self.chain <= 30:
                rolls += 8
            elif self.chain > 70:
                rolls += 12

            # lift inverse (neg_chance) to the amount of rolls if chain lost reset it to 0
            if not dec and not chain_lost:
                self.counter.odds *= neg_chance ** rolls
            elif not chain_lost:
                self.counter.odds /= neg_chance ** rolls
            else:
                self.chain = 0
            # update overlay
            self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}% - {self.chain}')
        # masuda method
        elif method == 3:
            rolls = 6
            neg_chance = 4095/4096
            if has_charm:
                rolls += 2

            if not dec and not chain_lost:
                self.counter.odds *= neg_chance ** rolls
            elif dec and not chain_lost:
                self.counter.odds /= neg_chance ** rolls
            self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}%')

    def close_toplevel(self):
        for child in self.rootW.winfo_children():
            if '.!toplevel' in str(child) and str(child) != '.!toplevel' and str(child) != '.!toplevel2':
                self.save()
                child.destroy()

    def refresh_Listbox(self):
        self.counterList.delete(0, 'end')
        for counter in self.counters:
            self.counterList.insert(counter.id, counter.name)

    def toggle_counter_overlay(self):
        # if overlay is active hide it and show it in the other case
        if self.isOverlayShown():
            self.overlay.withdraw()
            self.overlay2.withdraw()
        else:
            # if the controls are disabled ask whether to enable the controls or just overlay the counter
            if self.isDisabled():
                if messagebox.askyesno('re-enable controls?', 'Do you want to re-enable the controls?'):
                    self.enable()
            self.overlayCount.config(text=self.counter.value)
            self.overlay.deiconify()
            self.overlay2.deiconify()

    def toggle_time_shown(self, *_event):
        self.time_state = 'local_time' if self.time_state == 'run_time' else 'run_time'
        self.timeLabel.config(text=f'{self.time_state.replace("_", " ")}')
        self.timeLabel_change_state = time.time()

    def delete_counter(self, archiving=False):
        operation = ('archive', 'archiving') if archiving else ('delete', 'deleting')

        # delete highlighted counter Object from the list and save file
        if messagebox.askokcancel(f'{operation[0]} Counter',
                                  f'{operation[1]} this counter is irreversible do you want to continue'):
            self.close_toplevel()
            self.score.config(text='None Selected', font=self.font[24])
            self.counters.pop(self.counterIndex)
            self.save()
            self.refresh_Listbox()

    def newCounter(self):
        # make new Counter Object and add to the library

        def next1():
            # confirm the adding of the Counter and close the child window
            if messagebox.askokcancel('Make new Counter', f'Make new counter with the name {entry_name.get()}'):
                odds = 1

                def next2():
                    nonlocal odds
                    if choice.get() == 'old odds':
                        odds = 8192.0
                    elif choice.get() == 'old odds w charm':
                        odds = 2731.000027128392
                    elif choice.get() == 'new odds with charm':
                        odds = 1365.666720926762
                    else:
                        odds = 4096.0

                    self.counters[-1].odds = odds

                    set_odds.destroy()

                new_id = highestId() + 1

                m_id = methods.index(hunt_option.get())

                # if the method is set to encounter the odds need to be known
                if m_id == 0:
                    set_odds = Toplevel(self.rootW)
                    choice = StringVar(set_odds)

                    choices = ['old odds', 'old odds w charm', 'new odds', 'new odds with charm']

                    odds_choice = OptionMenu(set_odds, choice, *choices)
                    odds_choice.config(font=self.font[32], width=24)
                    odds_choice.pack()
                    # confirm the odds of the random encounter see next1 Func
                    next2 = Button(set_odds, font=self.font[20], width=14, text='CONTINUE', command=next2)
                    next2.pack()

                # make new counter object and add it to the list
                counter = CC.Counter(new_id, entry_name.get(), 0, method_id=m_id, odds=odds)
                self.counters.append(counter)

                entry_name.delete(0, 'end')
                make_counter.destroy()
                self.refresh_Listbox()
                print(counter.odds, m_id)

        # Child window for the name of the Counter
        make_counter = Toplevel(self.rootW)
        hunt_option = StringVar(make_counter)

        # Entry for the name
        entry_name = Entry(make_counter, font=self.font[32], width=24, text='Name')
        entry_name.grid(row=0, column=0, columnspan=2, pady=5, padx=3)
        # Option for Choosing the Pokemon hunt method
        methods = ['Encounters', 'DexNav', 'SOS', 'Masuda Method']
        hunt_options = OptionMenu(make_counter, hunt_option, *methods)
        hunt_options.grid(row=1, column=0, columnspan=2, pady=5, padx=3)
        # cancel go back to main window
        cancel = Button(make_counter, font=self.font[20], width=14, text='CANCEL', command=make_counter.destroy)
        cancel.grid(row=2, column=0, padx=(0, 3), pady=(0, 5))
        # confirm new Counter see next1 Func
        next1 = Button(make_counter, font=self.font[20], width=14, text='CONTINUE', command=next1)
        next1.grid(row=2, column=1, padx=(0, 3), pady=(0, 5))

        entry_name.focus_force()

    def openMainOptions(self, _event):
        # TODO: controls disabled after x minutes
        self.close_toplevel()
        main_options = Toplevel(self.rootW)
        display_var = StringVar()
        monitors = []
        display_options = {}
        for display_nmr, display in enumerate(monitors):
            Checkbutton(main_options,
                        text=f'display {display_nmr}',
                        variable=display_options[display],
                        )

        setDisplay = OptionMenu(main_options, display_var, *display_options)
        setDisplay.pack()

    def pause_run_time(self):
        self.paused_status = True

    def unpause_run_time(self):
        self.paused_status = False

    def isPaused(self):
        return self.paused_status

    def isDisabled(self):
        return self.disabled_status

    def disable(self):
        self.disabled_status = True
        # change the label in the main window to reflect that controls are turned off
        self.score.config(text='Controls\nDisabled', font=self.font[45])
        # hide all overlays when disabling the controls
        self.overlay.withdraw()
        self.overlay2.withdraw()

    def enable(self, *_args):
        self.disabled_status = False
        # change the text from controls disable to the selected counter value
        self.score.config(text=self.counter.value, font=self.font[75])

    def inFocus(self):
        return GetWindowText(GetForegroundWindow()) == self.rootW.title()

    def isCounterSelected(self):
        return self.selection is not None

    def openCounterOptions(self, _event):
        """
        Opens the optional menu to change values of a counter object with a Toplevel UI
        :param _event:
        :return:
        """
        if self.isCounterSelected():
            # close all other possible option windows
            self.close_toplevel()

            self.score.config(text='close settings', font=self.font[24])
            self.score.bind("<Button-1>", self.start)
            self.counterList.delete(0, 'end')

            cOC.CounterOption(self)

    def start(self, *_event):
        if self.isCounterSelected():
            if self.isDisabled():
                self.score.config(text='Controls\nDisabled', font=self.font[45])
            self.score.config(text=self.counter.value, font=self.fontCounter)
        else:
            self.score.config(text='none selected', font=self.font[24])
        self.score.bind("<Button-1>", self.openCounterOptions)

        self.counterList = Listbox(self.body, width=self.width // 2 - 1, height=self.height - 1, font=self.font[24])
        self.refresh_Listbox()
        self.counterList.grid(row=0, rowspan=5)
        self.counterList.bind("<<ListboxSelect>>", self.listBoxSelect)

    def listBoxSelect(self, event):
        if event.widget.curselection() != self.selection:
            # save current state of counter in the dict
            self.save()
            self.unpause_run_time()
            self.toggle_time_shown()

            # save index of selected object
            self.counterIndex = self.counterList.index('anchor')

            # open the newly selected counter object
            data = self.counters[self.counterIndex].value

            # put the counter value into the score box as long as controls are enabled
            if not self.isDisabled():
                if data < 10000:
                    self.score.configure(text=data, font=self.font[75])
                elif data < 100000:
                    self.score.configure(text=data, font=self.font[70])
                    self.fontCounter = self.font[70]
                else:
                    self.score.configure(text=data, font=self.font[60])
                    self.fontCounter = self.font[60]

            # save the selected counter as a single Counter object
            self.counter = self.counters[self.counterIndex]

            self.selection = event.widget.curselection()

            self.update_gui_chance(chain_lost=True)

            self.overlayCount.config(text=self.counter.value)

    '''def changedWindowSize(self, _event):
        _height = _event.height
        _width = _event.width
        # self.counterList.config(height=max(5, height // 38), width=width // 27)
        # self.rootW.geometry(f'{width}x{height}')'''

    def Archive(self, _event):
        c = self.counter
        archive_file = open('./saves/archived.txt', 'a')
        archive_file.write(f'{c.id} {c.name.replace(" ", "_")} {c.value} {c.jump}'
                           f' {c.method_id} {c.odds} {c.active_time}\n')
        self.delete_counter(archiving=True)
        archive_file.close()

    def save(self):
        save_file = open('./saves/counters.txt', 'w')
        for c in self.counters:
            save_file.write(f'{c.id} {c.name.replace(" ", "_")} {c.value} {c.jump}'
                            f' {c.method_id} {c.odds} {c.active_time}\n')
        save_file.close()

    def save_quit(self):
        self.save()
        self.rootW.destroy()


def change_tk_Label_colours(tk_Label: tkinter.Label, fg_colour='#000000', bg_colour='#FFFFFF', transparent=False):
    """
    change the appearance of the overlay

    :param tk_Label: tkinter Label
    :param fg_colour: colour of the text in the overlay (default= black)
    :param bg_colour: colour of the background (default= white) (ignored if background is transparent)
    :param transparent: make the background transparent (default= False)
    :return: None
    """

    tk_Label.config(fg=fg_colour)
    if transparent:
        bg_colour = hex(int(fg_colour.strip("#"), 16) + 1).replace("0x", '#')
        tk_Label.config(bg=bg_colour)
        parent = tk_Label.master
        parent.attributes('-transparentcolor', bg_colour)
    else:
        tk_Label.config(bg=bg_colour)


if __name__ == '__main__':
    import CounterReadClass as cR
    import CounterClass as cC
    # string with counter objects read by CounterRead class from './saves/counters.txt'
    counters = cR.CounterRead('./saves/counters.txt')
    # list to store counter objects in
    counterList = []
    # making counter object from the read line and storing in counterList
    for line in counters:
        # individual characteristics of counter object are separated by spaces in the txt file
        item = line.split(' ')
        # check whether the read line has actual text in it (because the last line of the txt file is empty at all times
        if item[0]:
            # counter needs 6 arguments and they are stored in multiple objects
            counterList.append(cC.Counter(*item))

    # start main window
    root = Tk()
    gui = Ui(root, counterList)
    root.mainloop()
