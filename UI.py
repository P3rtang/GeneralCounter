from tkinter import *
from tkinter import messagebox
import CounterClass as CC
import pokemonMethodClass as pMC
import UImethods as UIM
from win32api import GetSystemMetrics


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


class Ui:
    def __init__(self, root, saves, _gui_chance=None):
        # all counters are in saves
        self.counters = saves

        # make secondary extra features window
        self.gui2 = UIM.UiMethods(self.counters)
        self.gui2.root.withdraw()

        # start index of selected counter as 0
        self.counterIndex = 0
        # active counter object
        self.counter = self.counters[self.counterIndex]

        # make al font sizes op to 100
        self.font = []
        for n in range(1, 101):
            self.font.append(("Helvetica", f"{n}", "bold"))

        self.selection = None

        # start tkinter rootW is main root
        self.rootW = root
        self.height = 14
        self.width = 75

        # configs stored as tuple of 3 elements
        # 1: transparent or not
        # 2: foreground color (color of the text)
        # 3: background color (best left white when using transparent
        self.configs = [(True, 'red', '#FF0001'), (True, '#5280e9', '#5280e8'), (False, 'black', 'white')]
        self.configNmr = 0
        # make body for easy addition and resizing in main window
        self.body = Frame(self.rootW, width=954, height=512)
        self.body.pack()
        self.body.grid_propagate(False)

        self.counterList = Listbox(self.body, width=self.width // 2 - 1, height=self.height - 1, font=self.font[24])

        self.refreshListBox()

        self.counterList.grid(row=0, rowspan=5)

        # gives a frame to store the label with the count of the selected counter
        self.scoreFrame = Frame(self.body, borderwidth=1, relief="sunken",
                                width=300, height=280)
        self.scoreFrame.grid(row=0, column=1, rowspan=2)
        self.scoreFrame.pack_propagate(False)

        # Label with the actual current count of the selected counter
        self.score = Label(self.scoreFrame, text='None Selected', font=self.font[24])
        self.score.pack(fill="both", expand=True)

        self.overlayCount = Label(self.rootW, text=0, font=self.font[75])

        select = Button(self.body, font=self.font[24], command=self.selectCounter, text='SELECT')
        select.grid(row=2, column=1, pady=(5, 0), padx=10)
        delete = Button(self.body, font=self.font[24], command=self.deleteCounter, text='DELETE')
        delete.grid(row=4, column=1, pady=5)
        new = Button(self.body, font=self.font[24], command=self.newCounter, text='NEW')
        new.grid(row=3, column=1, pady=(5, 0), ipadx=26)

        self.counterList.bind("<<ListboxSelect>>", self.callback)
        self.score.bind("<Button-1>", self.openOptions)
        self.rootW.protocol("WM_DELETE_WINDOW", self.save_quit)

        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

        self.rootW.geometry(f'+{self.screen_width // 2 - 477}+{self.screen_height // 2 - 256}')

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
        cur_chance = self.counter.odds
        method = self.counter.method_id
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
                cur_chance = dexnav_chance_inc(self.counter.value, self.counter.odds, self.chain)

                self.counter.odds = cur_chance

            if dec and not chain_lost:
                cur_chance = dexnav_chance_dec(self.counter.value, self.counter.odds, self.chain)

                self.counter.odds = cur_chance

            if chain_lost:
                cur_chance = self.counter.odds

            self.chance.config(text=f'{round((1 - cur_chance) * 100, 3):.3f}% - {self.chain}')

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

    def changeCounter(self):
        self.overlayCount.config(bg=self.configs[self.configNmr][2])
        self.chance.config(bg=self.configs[self.configNmr][2])

        self.overlay.attributes('-transparentcolor', self.overlayCount['bg'])
        self.overlay2.attributes('-transparentcolor', self.gui2.chance['bg'])

        self.overlayCount.config(fg=self.configs[self.configNmr][1])
        self.chance.config(fg=self.configs[self.configNmr][1])
        # roll over to the next config for next click
        self.configNmr += 1
        self.configNmr %= len(self.configs)

    def close_toplevel(self):
        for child in self.rootW.winfo_children():
            print(child)
            if '.!toplevel' in str(child) and str(child) != '.!toplevel' and str(child) != '.!toplevel2':
                self.save()
                child.destroy()

    def refreshListBox(self):
        self.counterList.delete(0, 'end')
        for counter in self.counters:
            self.counterList.insert(counter.id, counter.name)

    def selectCounter(self):

        self.score.config(text=str(self.counter.value), font=self.font[75])

    def deleteCounter(self):
        # delete highlighted counter Object from the list and save file
        if messagebox.askokcancel('Delete Counter', 'Deleting this counter is irreversible do you want to continue'):
            self.close_toplevel()
            self.score.config(text='None Selected', font=self.font[24])
            self.counters.pop(self.counterIndex)
            self.save()
            self.refreshListBox()

    def newCounter(self):
        # make new Counter Object and add to the library

        def next1():
            # confirm the adding of the Counter and close the child window
            if messagebox.askokcancel('Make new Counter', f'Make new counter with the name {entry_name.get()}'):
                # clear the entryBox for a new counter
                counter = CC.Counter(len(self.counters) + 1, entry_name.get(), 0)

                # get selected method and search for its ID
                selected_method_id = str(methods.index(hunt_option.get()))

                # Make method object
                method = pMC.Method(counter.id, counter.name, counter.value, counter.jump, selected_method_id, 1)

                self.counters.append(counter)
                self.gui2.method_list.append(method)

                entry_name.delete(0, 'end')
                make_counter.destroy()
                self.refreshListBox()
        # Child window for the name of the Counter
        make_counter = Toplevel(self.rootW)
        hunt_option = StringVar(make_counter)

        # Entry for the name
        entry_name = Entry(make_counter, font=self.font[32], width=24, text='Name')
        entry_name.grid(row=0, column=0, columnspan=2, pady=5, padx=3)
        # Option for Choosing the Pokemon hunt method
        methods = ['Encounters', 'DexNav', 'SOS']
        hunt_options = OptionMenu(make_counter, hunt_option, *methods)
        hunt_options.grid(row=1, column=0, columnspan=2, pady=5, padx=3)
        # cancel go back to main window
        cancel = Button(make_counter, font=self.font[20], width=14, text='CANCEL', command=make_counter.destroy)
        cancel.grid(row=2, column=0, padx=(0, 3), pady=(0, 5))
        # confirm new Counter see next1 Func
        next1 = Button(make_counter, font=self.font[20], width=14, text='CONTINUE', command=next1)
        next1.grid(row=2, column=1, padx=(0, 3), pady=(0, 5))

        entry_name.focus_force()

    def openOptions(self, _event):
        # close all other possible option windows
        self.close_toplevel()

        # save and apply chosen options
        def applyOption():
            # debug code
            print(step_size_entry.get(), set_count.get())
            # changing the counter values
            self.counter.jump = int(step_size_entry.get()) if step_size_entry.get() else 1
            self.counter.value = int(set_count.get()) if set_count.get() else self.counter.value
            # save all counters to 'counters.txt'
            self.save()
            self.score.config(text=self.counter.value, font=self.font[75])
            self.selectCounter()

        def showPokWindow():
            if show_pokemon['text'] == 'pokemon chance OFF':
                self.overlay2.deiconify()
                show_pokemon.config(text='pokemon chance ON')
                self.update_gui_chance(chain_lost=True)
            else:
                self.overlay2.withdraw()
                show_pokemon.config(text='pokemon chance OFF')

        def open_overlay():
            if open_Overlay['text'] == 'overlay OFF':
                self.overlay.deiconify()
                open_Overlay.config(text='overlay ON')
            else:
                self.overlay.withdraw()
                open_Overlay.config(text='overlay OFF')

        # check if a selection is made otherwise don't open option menu
        if self.selection:
            option_menu = Toplevel(self.rootW)

            option_menu.geometry(f'+{self.screen_width // 2 + 498}+{self.screen_height // 2 - 256}')

            # open overlay with current count
            open_Overlay = Button(option_menu, text='', font=self.font[16], command=open_overlay)
            open_Overlay.pack(pady=(0, 20), fill='x')
            open_overlay()

            # extra feature window toggle
            show_pokemon = Button(option_menu, text='', font=self.font[16], command=showPokWindow)
            show_pokemon.pack(pady=(0, 20), fill='x')
            showPokWindow()

            Label(option_menu, text='set step-size', font=self.font[20]).pack()
            step_size_entry = Entry(option_menu, font=self.font[16], justify='center')
            step_size_entry.pack()
            Label(option_menu, text='set count', font=self.font[20]).pack()
            set_count = Entry(option_menu, font=self.font[16], justify='center')
            set_count.pack()
            set_count.focus_force()

            button_frame = Frame(option_menu)
            button_frame.pack()

            cancel = Button(button_frame, text='CANCEL', font=self.font[16], command=option_menu.destroy)
            apply = Button(button_frame, text='APPLY', font=self.font[16], command=applyOption)

            cancel.grid(row=0, column=0, ipadx=8, sticky='w')
            apply.grid(row=0, column=1, ipadx=17, sticky='e')

            self.counter = self.counters[int(self.selection[0])]

    def callback(self, event):
        if event.widget.curselection() != self.selection:
            # save current state of counter in the dict
            self.save()

            # save index of selected object
            self.counterIndex = self.counterList.index('anchor')

            # open the newly selected counter object
            data = self.counters[self.counterIndex].value
            if data < 10000:
                self.score.configure(text=data, font=self.font[75])
            elif data < 100000:
                self.score.configure(text=data, font=self.font[70])
            else:
                self.score.configure(text=data, font=self.font[60])

            # save the selected counter as a single Counter object
            self.counter = self.counters[self.counterIndex]

            self.selection = event.widget.curselection()

            self.update_gui_chance(chain_lost=True)

            self.overlayCount.config(text=self.counter.value)

    def save(self):
        save_file = open('counters.txt', 'w')
        for c in self.counters:
            save_file.write(f'{c.id} {c.name.replace(" ", "_")} {c.value} {c.jump} {c.method_id} {c.odds}\n')
        save_file.close()
        save_file = open('methods.txt', 'w')
        for m in self.gui2.method_list:
            save_file.write(f'{m.method_id} {m.odds}\n')

    def save_quit(self):
        self.save()
        self.rootW.destroy()

        quit('The End!')
