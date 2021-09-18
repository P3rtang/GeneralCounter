import tkinter as tk
from PIL import ImageTk, Image


class CounterOption:
    def __init__(self, class_ui):
        """
        Ui layout for basic extra options to change parameters of any Counter
        :param UI.Ui class_ui:
        """
        self.adv_time_setter = None
        self.parent = class_ui
        self.counter = self.parent.counter

        self.option_menu_frame = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)

        # option to change the counter's step size
        tk.Label(self.option_menu_frame, text='set step-size', font=self.parent.font[20]).pack()
        self.set_step_size_entry = tk.Entry(self.option_menu_frame, font=self.parent.font[16], justify='center')
        self.set_step_size_entry.pack()

        # option to change the counter's value
        tk.Label(self.option_menu_frame, text='set count', font=self.parent.font[20]).pack(pady=(10, 0))
        self.set_count_entry = tk.Entry(self.option_menu_frame, font=self.parent.font[16], justify='center')
        self.set_count_entry.pack()

        # frame for reset button and advanced option button
        button_frame1 = tk.Frame(self.option_menu_frame)
        button_frame1.pack(pady=(10, 0))
        # Button to reset the timer to 0
        self.reset_timer_to_zero = tk.Button(button_frame1, text='reset timer',
                                             font=self.parent.font[16], command=self.reset_timer)
        self.reset_timer_to_zero.grid(column=0, row=0)
        self.cog_image_resized = ImageTk.PhotoImage(Image.open('./bin/cog.png').resize((25, 25)))
        self.reset_timer_adv = tk.Label(button_frame1, image=self.cog_image_resized, width=25, height=25)
        self.reset_timer_adv.bind('<Button-1>', self.set_adv_time)
        self.reset_timer_adv.grid(column=1, row=0, padx=(10, 0))

        button_frame2 = tk.Frame(self.option_menu_frame)
        button_frame2.pack(pady=(20, 0))

        apply = tk.Button(button_frame2, text='APPLY', font=self.parent.font[16], command=self.close_menu)

        apply.pack(anchor='e')

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
    def open(self, counter, *_event):
        self.parent.counterList.grid_forget()
        self.counter = counter
        self.parent.pause_run_time()
        self.option_menu_frame.grid(row=0, rowspan=5)
        self.set_count_entry.focus_force()

        self.set_step_size_entry.insert(0, str(self.parent.counter.jump))
        self.set_count_entry.insert(0, str(self.parent.counter.value))

    # close menu
    def close_menu(self, *_event):
        self.counter.value = int(self.set_count_entry.get())
        self.counter.jump = int(self.set_step_size_entry.get())
        self.set_count_entry.delete(0, 'end')
        self.set_step_size_entry.delete(0, 'end')

        self.option_menu_frame.grid_forget()
        self.parent.closed_menu()


class MainOptionMenu:
    def __init__(self, class_ui):
        self.parent = class_ui

        self.option_menu_frame = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)

        self.timer_pause_toggle = tk.BooleanVar()
        timer_pause_checkbox = tk.Checkbutton(self.option_menu_frame, variable=self.timer_pause_toggle)
        timer_pause_checkbox.grid(row=0, column=0)
        tk.Label(self.option_menu_frame, text='Pause timer after', font=self.parent.font[20]).grid(row=0, column=1)

        self.disable_controls_after_toggle = tk.BooleanVar()
        disable_controls_after_checkbox = tk.Checkbutton(self.option_menu_frame,
                                                         variable=self.disable_controls_after_toggle)
        disable_controls_after_checkbox.grid(row=1, column=0)
        tk.Label(self.option_menu_frame, text='Disable controls after', font=self.parent.font[20]).grid(row=1, column=1)

        self.snap_to_taskbar = tk.BooleanVar()
        snap_to_taskbar_checkbox = tk.Checkbutton(self.option_menu_frame, variable=self.snap_to_taskbar)
        snap_to_taskbar_checkbox.grid(row=2, column=0)
        tk.Label(self.option_menu_frame, text='Snap overlay to taskbar',
                 font=self.parent.font[20]).grid(row=2, column=1)

        self.pokemon_hunt_mode_toggle = tk.BooleanVar()
        pokemon_hunt_mode_checkbox = tk.Checkbutton(self.option_menu_frame, variable=self.pokemon_hunt_mode_toggle)
        pokemon_hunt_mode_checkbox.grid(row=3, column=0)
        tk.Label(self.option_menu_frame, text='Show Pokemon Hunt Chance',
                 font=self.parent.font[20]).grid(row=3, column=1)

        button_frame = tk.Frame(self.option_menu_frame)
        button_frame.grid(row=4, columnspan=2, pady=(40, 0), ipadx=150, sticky='we')

        close_menu = tk.Button(button_frame, text='CLOSE', font=self.parent.font[16], command=self.close_menu)

        close_menu.pack(anchor='e')

    def show(self):
        self.parent.counterList.grid_forget()
        self.parent.pause_run_time()
        self.option_menu_frame.grid(row=0, rowspan=5)

    # close menu
    def close_menu(self, *_event):
        self.option_menu_frame.grid_forget()
        self.parent.closed_menu()


if __name__ == '__main__':
    from .Counter import Counter
    from .UI import Ui
    root = tk.Tk()
    CounterOption(Ui(root, [Counter(1, 'test', 0)]))
    root.mainloop()
