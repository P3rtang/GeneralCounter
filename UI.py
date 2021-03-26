from tkinter import *
from tkinter import messagebox
import CounterClass as CC
import UImethods as UIM


class Ui:
    def __init__(self, saves, _gui_chance=None):
        # all counters are in saves
        self.counters = saves

        # start index of selected counter as 0
        self.counterIndex = 0
        # active counter object
        self.counter = self.counters[self.counterIndex]

        # make and configure the optional window for extra features
        self.gui2 = UIM.UiMethods(self.counters)

        self.gui2.root.overrideredirect(True)
        self.gui2.root.wm_attributes("-topmost", True)
        self.gui2.root.withdraw()

        # make al font sizes op to 100
        self.font = []
        for n in range(1, 101):
            self.font.append(("Helvetica", f"{n}", "bold"))

        self.selection = None

        # start tkinter rootW is main root
        self.rootW = Tk()
        self.height = 14
        self.width = 75

        # configs stored as tuple of 3 elements
        # 1: transparent or not
        # 2: foreground color (color of the text)
        # 3: background color (best left white when using transparent
        self.configs = [(True, 'red', '#FF0001'), (True, '#5280e9', '#5280e8'), (False, 'black', 'white')]
        self.configNmr = 2
        # make body for easy addition and resizing in main window
        self.body = Frame(self.rootW)
        self.body.pack()

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

        self.select = Button(self.body, font=self.font[24], command=self.selectCounter, text='SELECT')
        self.select.grid(row=2, column=1, pady=(5, 0), padx=10)
        self.delete = Button(self.body, font=self.font[24], command=self.deleteCounter, text='DELETE')
        self.delete.grid(row=4, column=1, pady=5)
        self.new = Button(self.body, font=self.font[24], command=self.newCounter, text='NEW')
        self.new.grid(row=3, column=1, pady=(5, 0), ipadx=26)

        self.counterList.bind("<<ListboxSelect>>", self.callback)
        self.score.bind("<Button-1>", self.openOptions)
        self.rootW.protocol("WM_DELETE_WINDOW", self.saveQuit)

        self.rootW.mainloop()

    def closeToplevel(self):
        for child in self.rootW.winfo_children():
            if '.!toplevel' in str(child):
                self.save()
                child.destroy()

    def refreshListBox(self):
        self.counterList.delete(0, 'end')
        for counter in self.counters:
            self.counterList.insert(counter.id, counter.name)

    def selectCounter(self):
        # open child window with the current value of the chosen Counter object
        def changeCounter(_event):
            overlay.attributes('-transparentcolor', '')
            self.gui2.root.attributes('-transparentcolor', '')

            self.overlayCount.config(bg=self.configs[self.configNmr][2])
            self.gui2.chance.config(bg=self.configs[self.configNmr][2])

            if self.configs[self.configNmr][0]:
                overlay.attributes('-transparentcolor', self.overlayCount['bg'])
                self.gui2.root.attributes('-transparentcolor', self.gui2.chance['bg'])

            self.overlayCount.config(fg=self.configs[self.configNmr][1])
            self.gui2.chance.config(fg=self.configs[self.configNmr][1])
            # roll over to the next config for next click
            self.configNmr += 1
            self.configNmr %= len(self.configs)

        def exitOverlay(_event):
            self.save()
            overlay.destroy()
            self.gui2.root.withdraw()

        # call function to close any other child windows
        self.closeToplevel()

        overlay = Toplevel(self.rootW)
        self.overlayCount = Label(overlay,
                                  text=str(self.counter.value),
                                  font=self.font[75],
                                  bg=self.configs[self.configNmr][2])
        self.overlayCount.pack()
        overlay.overrideredirect(True)  # windowless
        overlay.lift()
        overlay.wm_attributes("-topmost", True)
        overlay.focus_force()

        overlay.bind("<KeyRelease>", self.keyUp)
        overlay.bind("<*>", changeCounter)
        overlay.bind("</>", lambda i=True: self.gui2.update(self.counter, chainLost=i))

        # when escape is pressed with the overlay active close all the overlays (including the extra feature window)
        overlay.bind("<Escape>", exitOverlay)

    def deleteCounter(self):
        # delete highlighted counter Object from the list and save file
        if messagebox.askokcancel('Delete Counter', 'Deleting this counter is irreversible do you want to continue'):
            self.closeToplevel()
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

                self.counters.append(counter)

                entry_name.delete(0, 'end')
                make_counter.destroy()
                self.refreshListBox()
        # Child window for the name of the Counter
        make_counter = Toplevel(self.rootW)

        # Entry for the name
        entry_name = Entry(make_counter, font=self.font[32], width=24, text='Name')
        entry_name.grid(row=0, column=0, columnspan=2, pady=5, padx=3)
        # cancel go back to main window
        cancel = Button(make_counter, font=self.font[20], width=14, text='CANCEL', command=make_counter.destroy)
        cancel.grid(row=1, column=0, padx=(0, 3), pady=(0, 5))
        # confirm new Counter see next1 Func
        next1 = Button(make_counter, font=self.font[20], width=14, text='CONTINUE', command=next1)
        next1.grid(row=1, column=1, padx=(0, 3), pady=(0, 5))

        entry_name.focus_force()

    def openOptions(self, _event):
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
                self.gui2.root.deiconify()
                self.gui2.root.focus_force()
                show_pokemon.config(text='pokemon chance ON')
            else:
                self.gui2.root.withdraw()
                show_pokemon.config(text='pokemon chance OFF')

        # check if a selection is made otherwise don't open option menu
        if self.selection:
            print(self.counter.id)
            option_menu = Toplevel(self.rootW)

            show_pokemon = Button(option_menu, text='pokemon chance OFF', font=self.font[16], command=showPokWindow)
            show_pokemon.pack(pady=(0, 20), fill='x')

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
            print(self.counter.id)
            self.gui2.update(self.counter, chainLost=True)
            self.selection = event.widget.curselection()

    def keyUp(self, char):
        print(f'pressed {char.char}')
        if char.char == '+' or char.char == ' ':
            self.counter.value += self.counter.jump
            self.gui2.update(self.counter)
        elif char.char == '-':
            self.counter.value -= self.counter.jump
            self.gui2.update(self.counter, dec=True)
        self.score.config(text=str(self.counter.value), font=self.font[75])
        self.overlayCount.config(text=str(self.counter.value), font=self.font[75])

    def save(self):
        save_file = open('counters.txt', 'w')
        for c in self.counters:
            save_file.write(f'{c.id} {c.name.replace(" ", "_")} {c.value} {c.jump}\n')
        save_file.close()
        save_file = open('methods.txt', 'w')
        for m in self.gui2.method_list:
            save_file.write(f'{m.method_id} {m.odds}\n')

    def saveQuit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.save()
            self.rootW.destroy()
            self.gui2.root.destroy()
