import tkinter as tk
from PIL import ImageTk


class CounterOption:
    def __init__(self, class_ui):
        """
        Ui layout for basic extra options to change parameters of any Counter
        :param UI.Ui class_ui:
        """
        self.adv_time_setter = None
        self.parent = class_ui

        self.option_menu = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)
        self.option_menu.grid(row=0, rowspan=5)

        # option to change the counter's step size
        tk.Label(self.option_menu, text='set step-size', font=self.parent.font[20]).pack()
        self.set_step_size_entry = tk.Entry(self.option_menu, font=self.parent.font[16], justify='center')
        self.set_step_size_entry.insert(0, str(self.parent.counter.jump))
        self.set_step_size_entry.pack()

        # option to change the counter's value
        tk.Label(self.option_menu, text='set count', font=self.parent.font[20]).pack(pady=(10, 0))
        self.set_count_entry = tk.Entry(self.option_menu, font=self.parent.font[16], justify='center')
        self.set_count_entry.insert(0, str(self.parent.counter.value))
        self.set_count_entry.pack()
        self.set_count_entry.focus_force()

        # frame for reset button and advanced option button
        button_frame1 = tk.Frame(self.option_menu)
        button_frame1.pack(pady=(10, 0))
        # Button to reset the timer to 0
        self.reset_timer_to_zero = tk.Button(button_frame1, text='reset timer',
                                             font=self.parent.font[16], command=self.reset_timer)
        self.reset_timer_to_zero.grid(column=0, row=0)
        self.cog_image_resized = ImageTk.PhotoImage(self.parent.option_image.resize((25, 25)))
        self.reset_timer_adv = tk.Label(button_frame1, image=self.cog_image_resized, width=25, height=25)
        self.reset_timer_adv.bind('<Button-1>', self.set_adv_time)
        self.reset_timer_adv.grid(column=1, row=0, padx=(10, 0))

        button_frame2 = tk.Frame(self.option_menu)
        button_frame2.pack(pady=(20, 0))

        cancel = tk.Button(button_frame2, text='CANCEL', font=self.parent.font[16], command=self.close)
        apply = tk.Button(button_frame2, text='APPLY', font=self.parent.font[16], command=self.apply_option)

        cancel.grid(row=0, column=0, ipadx=8, sticky='w')
        apply.grid(row=0, column=1, ipadx=17, sticky='e')

    def reset_timer(self, time=0):
        if not self.adv_time_setter:
            self.parent.counter.active_time = time
        else:
            self.parent.counter.active_time = self.adv_time_setter.get()
            self.adv_time_setter.close()

    def set_adv_time(self, _event):
        from .TimeSetter import TimeSetter
        self.adv_time_setter = TimeSetter(self.parent.rootW)

    # save and apply chosen options
    def apply_option(self):
        if not self.set_count_entry.get().isnumeric() or not self.set_step_size_entry.get().isnumeric():
            tk.Label(self.option_menu, text='No valid input', font=self.parent.font[20]).pack()
        else:
            self.parent.counter.value = int(self.set_count_entry.get())
            self.parent.counter.jump = int(self.set_step_size_entry.get())

        self.option_menu.destroy()
        self.parent.show_counter_listbox()

    def close(self):
        self.option_menu.destroy()
        self.parent.show_counter_listbox()


class MainOptionMenu:
    def __init__(self, class_ui):
        self.parent = class_ui

        self.option_menu_frame = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)
        self.option_menu_frame.grid(row=0, rowspan=5)

        self.timer_pause_toggle = tk.IntVar()
        timer_pause_checkbox = tk.Checkbutton(self.option_menu_frame, variable=self.timer_pause_toggle)
        timer_pause_checkbox.pack()

        tk.Label(self.option_menu_frame, text='Pause timer after', font=self.parent.font[20]).pack()

        button_frame = tk.Frame(self.option_menu_frame)
        button_frame.pack()

        cancel = tk.Button(button_frame, text='CANCEL', font=self.parent.font[16], command=self.close)
        apply = tk.Button(button_frame, text='APPLY', font=self.parent.font[16], command=self.apply_option)

        cancel.grid(row=0, column=0, ipadx=8, sticky='w')
        apply.grid(row=0, column=1, ipadx=17, sticky='e')

    # save and apply chosen options
    def apply_option(self):
        self.option_menu_frame.destroy()
        self.parent.show_counter_listbox()

    def close(self):
        self.option_menu_frame.destroy()
        self.parent.show_counter_listbox()


if __name__ == '__main__':
    from .CounterClass import Counter
    from .UI import Ui
    root = tk.Tk()
    CounterOption(Ui(root, [Counter(1, 'test', 0)]))
    root.mainloop()
