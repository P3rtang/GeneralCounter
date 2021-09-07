import tkinter as tk


class TimeSetter:
    """
    Object that adds a tkinter TopLevel with a basic clock to select a date and time
    :param tk.Tk() tk_root:
    """

    def __init__(self, tk_root, date=False):
        self.dates_enabled = date

        self.sub_root = tk.Toplevel(tk_root)

        hour_frame = tk.Frame(self.sub_root)
        hour_frame.grid(column=0, row=0)
        min_frame = tk.Frame(self.sub_root)
        min_frame.grid(column=2, row=0)
        sec_frame = tk.Frame(self.sub_root)
        sec_frame.grid(column=4, row=0)
        tk.Label(self.sub_root, text=':', font=('Helvetica', 30)).grid(column=1, row=0)
        tk.Label(self.sub_root, text=':', font=('Helvetica', 30)).grid(column=3, row=0)

        self.up_key_hour = tk.Button(hour_frame, text='▲',
                                     command=lambda time_diff=3600: self.change_time_by(time_diff))
        self.up_key_hour.pack(fill='both')
        self.set_hour_entry = tk.Entry(hour_frame, font=('Helvetica', 30), width=2)
        self.set_hour_entry.insert(0, '00')
        self.set_hour_entry.pack()
        self.down_key_hour = tk.Button(hour_frame, text='▼',
                                       command=lambda time_diff=-3600: self.change_time_by(time_diff))
        self.down_key_hour.pack(fill='both')

        self.up_key_min = tk.Button(min_frame, text='▲', command=lambda time_diff=60: self.change_time_by(time_diff))
        self.up_key_min.pack(fill='both')
        self.set_min_entry = tk.Entry(min_frame, font=('Helvetica', 30), width=2)
        self.set_min_entry.insert(0, '00')
        self.set_min_entry.pack()
        self.down_key_min = tk.Button(min_frame, text='▼', command=lambda time_diff=-60: self.change_time_by(time_diff))
        self.down_key_min.pack(fill='both')

        self.up_key_sec = tk.Button(sec_frame, text='▲', command=lambda time_diff=1: self.change_time_by(time_diff))
        self.up_key_sec.pack(fill='both')
        self.set_sec_entry = tk.Entry(sec_frame, font=('Helvetica', 30), width=2)
        self.set_sec_entry.insert(0, '00')
        self.set_sec_entry.pack()
        self.down_key_sec = tk.Button(sec_frame, text='▼', command=lambda time_diff=-1: self.change_time_by(time_diff))
        self.down_key_sec.pack(fill='both')

    def get(self):
        return int(self.set_sec_entry.get()) + int(self.set_min_entry.get())*60 + int(self.set_hour_entry.get())*3600

    def close(self):
        self.sub_root.destroy()

    def change_time_by(self, secs: int):
        current_selected_time = int(self.set_sec_entry.get()) +\
                                int(self.set_min_entry.get())*60 +\
                                int(self.set_hour_entry.get())*3600
        new_selected_time = current_selected_time + secs

        self.set_sec_entry.delete(0, 'end')
        self.set_sec_entry.insert(0, f'{new_selected_time % 60:02d}')
        self.set_min_entry.delete(0, 'end')
        self.set_min_entry.insert(0, f'{new_selected_time // 60 % 60:02d}')
        self.set_hour_entry.delete(0, 'end')
        self.set_hour_entry.insert(0, f'{new_selected_time // 3600:02d}')


if __name__ == '__main__':
    root = tk.Tk()
    ts = TimeSetter(root)
    root.mainloop()
