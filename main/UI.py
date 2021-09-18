from tkinter import *
from tkinter import messagebox
import time
from sys import platform
if platform == 'win32':
    from win32api import GetSystemMetrics
    from win32gui import GetWindowText, GetForegroundWindow
elif platform == 'linux' or platform == 'linux2':
    import screeninfo
from PIL import ImageTk, Image
from .Counter import Counter
from .MainOption import MainOptionMenu, CounterOption
from .overlayUi import OverlayUi


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


def method_get_chance(method_id, odds, steps):
    if type(steps) == int:
        if method_id == 0:
            return f'{(1 - (1 - 1 / odds) ** steps) * 100:.03f}%'
    else:
        return 1


def get_highest_id(save_file, archive_file):
    """
    Function meant to return the number of counters saved in both the active save file and the archive file
    This is done by counting and adding all the newlines in both save files

    :param str save_file: save file location  for active counters
    :param str archive_file: save file location for archived counters
    :return int:
    """
    with open(save_file) as saves:
        saves = saves.read()
    with open(archive_file) as archive:
        archive = archive.read()
    # count every newline in both the saves and archive file, add them together and return
    highest_id = (saves + archive).count('\n')
    return highest_id


class Ui:
    # TODO: add docstring
    def __init__(self, tk_root: Tk, saves: list):
        # TODO: make the window respond to resizing without crashing or creating blank space
        # list to keep track of all resizable widgets to customize the layout
        self.resizable = []
        # TODO: frame rate should be tightened to a variable changed in the options menu
        self.frame_rate = 120

        # all counters are in saves
        self.counters = saves

        # make secondary extra features window
        # self.gui2 = UIM.UiMethods(self.counters)
        # self.gui2.root.withdraw()

        # start index of selected counter as 0
        self.counterIndex = 0
        # active counter object
        self.counter = Counter(0, 'None', 'none selected')

        # flag to disable all events and keyboard listeners
        self.disabled_status = False

        # make al font sizes op to 100
        self.font = []
        for n in range(1, 101):
            self.font.append(("Helvetica", f"{n}", "bold"))
        self.fontCounter = self.font[75]

        self.selection = None

        # start tkinter, rootW is the main root
        self.rootW = tk_root
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

        self.MainOptions = MainOptionMenu(self)
        self.CounterOptions = CounterOption(self)
        self.is_menu_opened = False

        self.counterList = Listbox(self.body, width=self.width // 2 - 1, height=self.height - 1, font=self.font[24])
        # TODO: clicking in the window(listbox or outside) should deselect any counter
        # gives a frame to store the label with; current time / time since opening counter (uptime)
        # change between the two options by clicking the time frame
        self.timeFrame = Frame(self.body, borderwidth=1, relief="sunken",
                               width=300, height=50)
        self.timeFrame.grid(row=0, column=1, rowspan=1, columnspan=2)
        self.timeFrame.pack_propagate(False)

        # current mode the time window is in
        # default = local_time when no counter is selected
        self.timeLabel_states = ['local_time', 'run_time']
        self.timeLabel_state = self.timeLabel_states[0]
        # save time when label changed between local an run time in order to show the setting for (default=1) seconds
        # TODO add default time state as an option in the menu
        self.timeLabel_change_state = time.time()
        self.timeLabel_show_state_time = 1

        # Label with the actual current time / uptime of the selected counter
        self.timeLabel = Label(self.timeFrame, text=f'{self.timeLabel_state.replace("_", " ")}', font=self.font[24])
        self.timeLabel.pack(fill="both", expand=True)
        self.timeLabel.bind('<Button-1>', func=self.toggle_time_shown)

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

        select = Button(self.body, font=self.font[24], command=self.toggle_counter_overlay, text='OVERLAY')
        select.grid(row=2, column=1, pady=(5, 0), padx=10)
        delete = Button(self.body, font=self.font[24], command=self.delete_counter, text='DELETE')
        delete.grid(row=4, column=1, pady=5, ipadx=14)
        new = Button(self.body, font=self.font[24], command=self.new_counter, text='NEW')
        new.grid(row=3, column=1, pady=(5, 0), ipadx=41)

        self.archive_image = ImageTk.PhotoImage(Image.open('./bin/archive2.png'))

        archive = Label(self.body, image=self.archive_image, width=60, height=60)
        archive.grid(row=4, column=2)
        archive.bind("<Button-1>", self.archive)

        self.option_image = Image.open('./bin/cog.png')
        self.option_image_tk = ImageTk.PhotoImage(self.option_image)

        options = Label(self.body, image=self.option_image_tk, width=60, height=60)
        options.grid(row=2, column=2)
        options.bind("<Button-1>", self.open_main_options)

        self.delete_image = ImageTk.PhotoImage(Image.open('./bin/trashcan.png'))

        delete = Label(self.body, image=self.delete_image, width=60, height=60)
        delete.grid(row=3, column=2)
        delete.bind("<Button-1>", self.delete_counter)
        self.show_counter_listbox()
        self.rootW.protocol("WM_DELETE_WINDOW", self.save_quit)

        from screeninfo import get_monitors
        for monitor in get_monitors():
            self.screen_width = monitor.width
            self.screen_height = monitor.height

        self.rootW.geometry(f'+{self.screen_width // 2 - 477}+{self.screen_height // 2 - 256}')
        self.rootW.bind("<Configure>", print('window size change...WIP'))

        self.overlay = OverlayUi(self, self.counter.value)
        self.overlay2 = OverlayUi(self, method_get_chance(self.counter.method_id,
                                                          self.counter.odds,
                                                          self.counter.value), font_size=20)

    # def update_gui_chance(self, dec=False, chain_lost=False, has_charm=False):
    #     # store the method for which values need to be calculated
    #     # cur_chance = self.counter.odds
    #     method = self.counter.method_id
    #
    #     # updating the chain dependant on the input dec means decreasing and
    #     # any update with chain lost sets the chain to 0 (also used when starting the gui
    #     if chain_lost:
    #         self.chain = 0
    #     elif dec:
    #         self.chain -= 1
    #     else:
    #         self.chain += 1
    #
    #     # normal random encounter with odds store in self.counter.odds method is stored in method_list
    #     if method == 0 and self.counter.value:
    #         cur_chance = 1 - (1 - 1 / self.counter.odds) ** self.counter.value
    #         self.chance.config(text=f'{round(cur_chance * 100, 3):.3f}%')
    #
    #     # dexnav encounter with previous encounter odds stored in self.counter.odds
    #     elif method == 1:
    #         if not dec and not chain_lost:
    #             self.counter.odds = dexnav_chance_inc(self.counter.value, self.counter.odds, self.chain)
    #
    #         if dec and not chain_lost:
    #             self.counter.odds = dexnav_chance_dec(self.counter.value, self.counter.odds, self.chain)
    #
    #         self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}% - {self.chain}')
    #
    #     # SOS encounters with previous encounter odds stored in self.counter.odds
    #     # this method works with rolls and is the base odds lifted to the power of the nr of rolls
    #     elif method == 2:
    #         rolls = 1
    #         neg_chance = 4095 / 4096
    #
    #         if has_charm:
    #             rolls += 2
    #
    #         if self.chain <= 10:
    #             pass
    #         elif self.chain <= 20:
    #             rolls += 4
    #         elif self.chain <= 30:
    #             rolls += 8
    #         elif self.chain > 70:
    #             rolls += 12
    #
    #         # lift inverse (neg_chance) to the amount of rolls if chain lost reset it to 0
    #         if not dec and not chain_lost:
    #             self.counter.odds *= neg_chance ** rolls
    #         elif not chain_lost:
    #             self.counter.odds /= neg_chance ** rolls
    #         else:
    #             self.chain = 0
    #         # update overlay
    #         self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}% - {self.chain}')
    #     # masuda method
    #     elif method == 3:
    #         rolls = 6
    #         neg_chance = 4095/4096
    #         if has_charm:
    #             rolls += 2
    #
    #         if not dec and not chain_lost:
    #             self.counter.odds *= neg_chance ** rolls
    #         elif dec and not chain_lost:
    #             self.counter.odds /= neg_chance ** rolls
    #         self.chance.config(text=f'{round((1 - self.counter.odds) * 100, 3):.3f}%')

    def close_toplevel(self):
        for child in self.rootW.winfo_children():
            if '.!toplevel' in str(child) and str(child) != '.!toplevel' and str(child) != '.!toplevel2':
                self.save()
                child.destroy()

    def refresh_listbox(self):
        self.counterList.delete(0, 'end')
        for counter in self.counters:
            self.counterList.insert(counter.id, counter.name)

    def closed_menu(self):
        self.score.unbind('<Button-1>')
        self.counterList.grid(row=0, rowspan=5)
        self.score.config(text=self.counter.value, font=self.font[75])
        self.score.bind('<Button-1>', self.open_counter_options)
        self.is_menu_opened = False
        self.score.focus_force()

    def toggle_time_shown(self, *_args, new_state=None):
        """
        switch between time modes shown
        if time_new_state is specified switch to that

        :param new_state: 2 possible options 'local_time', 'run_time'
        :return: None
        """
        if new_state not in self.timeLabel_states and new_state is not None:
            raise ValueError(f'new_state must be one of {self.timeLabel_states} or None not {new_state}')
        elif new_state:
            self.timeLabel_state = new_state
        else:
            self.timeLabel_state = 'local_time' if self.timeLabel_state == 'run_time' else 'run_time'
        self.timeLabel.config(text=f'{self.timeLabel_state.replace("_", " ")}')
        self.timeLabel_change_state = time.time()

    def update_time(self):
        cur_time = time.time()
        if (cur_time - self.timeLabel_change_state > self.timeLabel_show_state_time
                and self.timeLabel_state == 'local_time'):
            self.timeLabel.config(text=f'{time.strftime("%H:%M:%S")}')
        elif cur_time - self.timeLabel_change_state > self.timeLabel_show_state_time:
            t = self.counter.active_time
            self.timeLabel.config(text=f'{int(t // 3600):02d}:{int(t // 60 % 60):02d}'
                                       f':{int(t%60):02d}.{int((t-int(t))*100):02d}')

    def delete_counter(self, archiving=False):
        operation = ('archive', 'archiving') if archiving else ('delete', 'deleting')

        # delete highlighted counter Object from the list and save file
        if messagebox.askokcancel(f'{operation[0]} Counter',
                                  f'{operation[1]} this counter is irreversible do you want to continue'):
            self.close_toplevel()
            self.score.config(text='None Selected', font=self.font[24])
            self.counters.pop(self.counterIndex)
            self.save()
            self.refresh_listbox()

    def new_counter(self):
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

                new_id = get_highest_id('../saves/counters.txt', '../saves/archived.txt') + 1

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
                counter = cC.Counter(new_id, entry_name.get(), 0, method_id=m_id, odds=odds)
                self.counters.append(counter)

                entry_name.delete(0, 'end')
                make_counter.destroy()
                self.refresh_listbox()
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

    def pause_run_time(self):
        self.paused_status = True

    def unpause_run_time(self):
        self.paused_status = False

    def is_paused(self):
        return self.paused_status

    def is_disabled(self):
        return self.disabled_status

    def disable(self):
        self.disabled_status = True
        # change the label in the main window to reflect that controls are turned off
        self.score.config(text='Controls\nDisabled', font=self.font[45])
        # hide all overlays when disabling the controls
        self.overlay.hide()

    def enable(self, *_args):
        self.disabled_status = False
        # change the text from controls disable to the selected counter value
        self.score.config(text=self.counter.value, font=self.font[75])

    def is_in_focus(self):
        return GetWindowText(GetForegroundWindow()) == self.rootW.title()

    def is_counter_selected(self):
        return self.selection is not None

    def open_main_options(self, _event):
        self.close_toplevel()
        self.is_menu_opened = True
        self.MainOptions.show()

        self.score.config(text='close settings', font=self.font[24])
        self.score.bind("<Button-1>", self.MainOptions.close_menu)

    def open_counter_options(self, _event):
        if self.counterList.curselection():
            self.close_toplevel()
            self.is_menu_opened = True
            self.CounterOptions.open(self.counter)

            self.score.config(text='close settings', font=self.font[24])
            self.score.bind("<Button-1>", self.MainOptions.close_menu)

    def toggle_counter_overlay(self):
        self.overlay.hide() if self.overlay.is_active else self.overlay.show()
        if self.MainOptions.pokemon_hunt_mode_toggle.get():
            self.overlay2.hide() if self.overlay2.is_active else self.overlay2.show()

    def show_counter_listbox(self, *_event):
        if self.is_counter_selected():
            if self.is_disabled():
                self.score.config(text='Controls\nDisabled', font=self.font[45])
            self.score.config(text=self.counter.value, font=self.fontCounter)
        else:
            self.score.config(text='none selected', font=self.font[24])
        self.score.bind("<Button-1>", self.open_counter_options)
        self.refresh_listbox()
        self.counterList.grid(row=0, rowspan=5)
        self.counterList.bind("<<ListboxSelect>>", self.listbox_select)

    def listbox_select(self, event):
        if event.widget.curselection() != self.selection:
            # save current state of counter in the dict
            self.save()
            self.unpause_run_time()
            self.toggle_time_shown(new_state='run_time')

            # save index of selected object
            self.counterIndex = self.counterList.index('anchor')

            # open the newly selected counter object
            data = self.counters[self.counterIndex].value

            # put the counter value into the score box as long as controls are enabled
            if not self.is_disabled():
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
            self.overlay.update(self.counter.value)

    '''def changedWindowSize(self, _event):
        _height = _event.height
        _width = _event.width
        # self.counterList.config(height=max(5, height // 38), width=width // 27)
        # self.rootW.geometry(f'{width}x{height}')'''

    def archive(self, _event):
        c = self.counter
        archive_file = open('../saves/archived.txt', 'a')
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


if __name__ == '__main__':
    import CounterRead as cR
    import Counter as cC
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
