import tkinter as tk
import CounterRead as Cr
from win32api import GetSystemMetrics


def changeFontSize(widgets, size):
    for widget in widgets:
        widget.config(font=("Helvetica", f"{size}", "bold"))


class Archive:
    def __init__(self, tk_root):

        self.archive_counter_read = Cr.CounterRead('./saves/archived.txt')

        self.archive = []

        self.max_char = 10
        # extract all archived counters with the read method
        for c in self.archive_counter_read:
            # filter out the last line which should always be an empty line
            if c != '':
                self.archive.append(c)

        self.root = tk_root
        self.root.grid_propagate(False)

        # add a body to set the size of the window as a fixed value
        self.main_body = tk.Frame(root)
        self.main_body.pack_propagate(False)
        self.main_body.grid(column=0, row=0)

        self.archive_tk_list = tk.Listbox(self.main_body)

        # add a second body to show counter values
        self.main_body2 = tk.Frame(root)
        self.main_body2.pack_propagate(False)
        self.main_body2.grid(column=1, row=0)

        self.archive_tk_scores = tk.Listbox(self.main_body2)

        # add the size of the window to the class
        height = 400
        width = 600

        self.cnf2 = {'height': height,
                     'width': width // 5}

        self.cnf1 = {'height': height,
                     'width': width - self.cnf2['width']}

        # add the location of the window to the class
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)

        self.cur_x = screen_width // 2 - 150
        self.cur_y = screen_height // 2 - 100
        self.root.geometry(f'+{self.cur_x}+{self.cur_y}')

        self.root.bind('<Configure>', self.callback)

        # main_menu implements the top menu bar
        main_menu = tk.Menu(self.root, tearoff=0)
        self.option_dropdown = tk.Menu(self.root)

        main_menu.add_cascade(label='Options', menu=self.option_dropdown)
        self.option_dropdown.add_command(label='Fontsize', command=self.openFontSlider)

        main_menu.add_command(label='Exit', command=self.root.destroy)

        root.config(menu=main_menu)

        self.setWindowSize()

        self.archive_names = archive_element(self.main_body, self.archiveElement(1))
        self.archive_counts = archive_element(self.main_body2, self.archiveElement(2))

        self.archive_names.listB.bind("<<ListboxSelect>>", self.listBoxSelect)
        self.archive_counts.listB.bind("<<ListboxSelect>>", self.listBoxSelect)

    def __repr__(self):
        return_str = ''
        for c in self.archive:
            return_str += str(c) + '\n'
        return return_str

    def show(self):
        self.archive_names.show(self.cnf1)
        self.archive_counts.show(self.cnf2)
        # self.archive_tk_list.place(self.cnf1)
        # self.archive_tk_scores.place(self.cnf2)

    def openFontSlider(self):
        # font slider opens a slider to select the font size of choosing within a range of 10 to 50
        font_size_slider = tk.Toplevel(self.root)
        font_size_slider.overrideredirect(True)
        archive_tk_list_size = tk.Scale(font_size_slider, from_=10, to=50, orient='horizontal',
                                        command=lambda x: changeFontSize((self.archive_names.listB
                                                                          , self.archive_counts.listB)
                                                                         , archive_tk_list_size.get()))

        archive_tk_list_size.grid(column=0, row=0)
        archive_tk_list_size.focus_set()

        font_size_slider.bind('<FocusOut>', lambda x: font_size_slider.destroy())

    def callback(self, _event):
        root_geom = self.root.winfo_geometry().replace('x', '+').split('+')

        self.cur_x = int(root_geom[2])
        self.cur_y = int(root_geom[3])

        width = int(root_geom[0])
        height = int(root_geom[1])
        self.cnf2 = {'height': height,
                     'width': width // 4}
        self.cnf1 = {'height': height,
                     'width': width - self.cnf2['width']}

        changeFontSize((self.archive_names.listB
                        , self.archive_counts.listB)
                       , width // self.max_char)

        self.setWindowSize()
        self.show()

    def setWindowSize(self):
        self.main_body.config(self.cnf1)
        self.main_body2.config(self.cnf2)

        changeFontSize((self.archive_tk_list, self.archive_tk_scores), self.cnf1['width'] // 15)

    def archiveElement(self, index):
        temp = []
        for c in self.archive:
            c = c.split(' ')
            temp.append(c[index].replace('_', ' '))
            if index == 1:
                self.max_char = len(c[1]) if len(c[1]) > self.max_char else self.max_char
        return temp

    def listBoxSelect(self, _event):
        index = self.archive_names.listB.curselection()\
            if self.archive_names.listB.curselection() else self.archive_counts.listB.curselection()
        print(index)
        self.archive_names.listB.activate(index[0])
        self.archive_counts.listB.activate(index[0])


class archive_element:
    def __init__(self, root, archive_element):
        self.archive_element = archive_element

        self.listB = tk.Listbox(root)

        for i, c in enumerate(archive_element):
            self.listB.insert(i, c)

    def show(self, cnf=None):
        self.listB.place(cnf)


if __name__ == '__main__':
    root = tk.Tk()

    archive = Archive(root)

    archive.show()
    root.mainloop()
