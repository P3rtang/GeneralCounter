import tkinter as tk
import Counter as cC
import UI as UI


class CounterOption:
    def __init__(self, classUI):

        self.parent = classUI

        self.option_menu = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)
        self.option_menu.grid(row=0, rowspan=5)

        self.open_Overlay = tk.Button(self.option_menu, text='', font=self.parent.font[16], command=self.open_overlay)
        self.open_Overlay.pack(pady=(0, 20), fill='x')
        self.open_overlay()

        # extra feature window toggle
        self.show_pokemon = tk.Button(self.option_menu, text='', font=self.parent.font[16], command=self.showPokWindow)
        self.show_pokemon.pack(pady=(0, 20), fill='x')
        self.showPokWindow()

        tk.Label(self.option_menu, text='set step-size', font=self.parent.font[20]).pack()
        self.step_size_entry = tk.Entry(self.option_menu, font=self.parent.font[16], justify='center')
        self.step_size_entry.pack()
        tk.Label(self.option_menu, text='set count', font=self.parent.font[20]).pack()
        self.set_count = tk.Entry(self.option_menu, font=self.parent.font[16], justify='center')
        self.set_count.pack()
        self.set_count.focus_force()

        button_frame = tk.Frame(self.option_menu)
        button_frame.pack()

        cancel = tk.Button(button_frame, text='CANCEL', font=self.parent.font[16], command=self.close)
        apply = tk.Button(button_frame, text='APPLY', font=self.parent.font[16], command=self.applyOption)

        cancel.grid(row=0, column=0, ipadx=8, sticky='w')
        apply.grid(row=0, column=1, ipadx=17, sticky='e')

    # save and apply chosen options
    def applyOption(self):
        # changing the counter values
        self.parent.counter.jump = int(self.step_size_entry.get()) if self.step_size_entry.get() else 1
        self.parent.counter.value = int(self.set_count.get()) if self.set_count.get() else self.parent.counter.value
        # save all counters to './saves/counters.txt'
        self.parent.save()
        self.parent.score.config(text=self.parent.counter.value, font=self.parent.font[75])
        self.option_menu.destroy()
        self.parent.show_counter_listbox()

    def showPokWindow(self):
        if self.show_pokemon['text'] == 'chance OFF':
            self.parent.overlay2.deiconify()
            self.show_pokemon.config(text='chance ON')
            self.parent.update_gui_chance(chain_lost=True)
        else:
            self.parent.overlay2.withdraw()
            self.show_pokemon.config(text='chance OFF')

    def open_overlay(self):
        if self.open_Overlay['text'] == 'overlay OFF':
            self.parent.overlay.deiconify()
            self.open_Overlay.config(text='overlay ON')
        else:
            self.parent.overlay.withdraw()
            self.open_Overlay.config(text='overlay OFF')

    def close(self):
        self.option_menu.destroy()
        self.parent.show_counter_listbox()


if __name__ == '__main__':
    root = tk.Tk()
    CounterOption(UI.Ui(root, [cC.Counter(1, 'test', 0)]))
    root.mainloop()
