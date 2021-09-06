import tkinter as tk
import CounterClass as cC
import UI as UI


class CounterOption:
    def __init__(self, classUI):

        self.parent = classUI

        self.option_menu = tk.Frame(self.parent.body, highlightbackground="black", highlightthickness=5)
        self.option_menu.grid(row=0, rowspan=5)

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
        self.option_menu.destroy()
        self.parent.start()

    def close(self):
        self.option_menu.destroy()
        self.parent.start()


if __name__ == '__main__':
    root = tk.Tk()
    CounterOption(UI.Ui(root, [cC.Counter(1, 'test', 0)]))
    root.mainloop()
