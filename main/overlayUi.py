# open child window with the current value of the chosen Counter object
from tkinter import *
from typing import Union
from win32api import GetMonitorInfo, MonitorFromPoint


class OverlayUi:
    def __init__(self, root_ui, data: Union[int, str]):
        self.root_ui = root_ui
        self.data = data

        self.is_active = False
        self.styles = []

        # used for mouse values when dragging a window
        self.click_x, self.click_y = 0, 0

        self.overlay = Tk()
        self.overlay_count = Label(self.overlay, font=self.root_ui.font[75])
        self.overlay_count.pack()

        self.overlay.bind('<ButtonPress-1>', self.overlay_mouse_down)
        self.overlay.bind('<B1-Motion>', self.move_overlay_to)
        self.overlay.overrideredirect(True)
        self.overlay.withdraw()

    def update(self, new_data):
        self.data = new_data

        self.overlay_count.config(text=self.data)

    def hide(self):
        self.overlay.withdraw()
        self.is_active = False

    def show(self):
        self.overlay.deiconify()
        print(self.overlay.winfo_screenvisual())

        self.overlay_count.config(text=self.data)
        self.is_active = True

    def change_overlay_colours(self, fg_colour='#000000', bg_colour='#FFFFFF', transparent=False):
        """
        change the appearance of the overlay

        :param fg_colour: colour of the text in the overlay (default= black)
        :param bg_colour: colour of the background (default= white) (ignored if background is transparent)
        :param transparent: make the background transparent (default= False)
        :return: None
        """

        self.overlay_count.config(fg=fg_colour)
        if transparent:
            bg_colour = hex(int(fg_colour.strip("#"), 16) + 1).replace("0x", '#')
            self.overlay_count.config(bg=bg_colour)
            parent = self.overlay
            parent.attributes('-transparentcolor', bg_colour)
        else:
            self.overlay_count.config(bg=bg_colour)

    def move_overlay_to(self, event):
        # get the delta of the mouse start position and its current position
        delta_x, delta_y = event.x - self.click_x, event.y - self.click_y
        # set the new x, y accordingly
        new_x, new_y = self.overlay.winfo_x() + delta_x, self.overlay.winfo_y() + delta_y
        # get screen and taskbar info for snapping
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_full = monitor_info['Monitor']
        monitor_work = monitor_info['Work']
        # get widget size fro snapping to the non-zero side
        w = self.overlay.winfo_width()
        h = self.overlay.winfo_height()
        # choose snap points based on setting
        snap_points = monitor_work if self.root_ui.MainOptions.snap_to_taskbar.get() else monitor_full

        # check whether window is in 10 pixels of snap points
        new_x = 0 if new_x < 10 + snap_points[0] else new_x
        new_y = 0 if new_y < 10 + snap_points[1] else new_y
        new_x = snap_points[2] - w if snap_points[2] - new_x < 10 + w else new_x
        new_y = snap_points[3] - h if snap_points[3] - new_y < 10 + h else new_y

        # place window at current mouse position or snap point
        self.overlay.geometry(f'+{new_x}+{new_y}')

    def overlay_mouse_down(self, event):
        # get the x, y of the mouse starting position
        self.click_x, self.click_y = event.x, event.y


if __name__ == '__main__':
    from CounterRead import CounterRead
    from UI import Ui

    root = Tk()
    counters = CounterRead('..\\saves\\counters.txt').get_list()
    temp_ui = Ui(root, counters)
    overlay_test = OverlayUi(temp_ui, 0)

    root.mainloop()
