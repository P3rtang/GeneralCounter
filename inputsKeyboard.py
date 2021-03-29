import threading
from pynput.mouse import Button
from pynput.keyboard import Listener, KeyCode
import tkinter


delay = 0.03
button = Button.left
start_stop_key = KeyCode(char='+')
exit_key = KeyCode(char='-')


class ClickMouse(threading.Thread):
    def __init__(self, root):
        super(ClickMouse, self).__init__()
        self.window = root
        with Listener(on_press=self.on_press) as listener:
            self.window.update()
            listener.join()

    def add_key(self):
        self.window.keyUp("<KeyRelease event state=Mod1 keysym=plus keycode=107 char='+' x=1299 y=698>")
        print('key+')

    def min_key(self):
        self.window.keyUp("<KeyRelease event state=Mod1 keysym=plus keycode=107 char='-' x=1299 y=698>")
        print('key-')

    def on_press(self, key):
        if key == start_stop_key:
            self.add_key()
        elif key == exit_key:
            self.min_key()

if '__name__' == '__main__':
    root = tkinter.Tk()
    click = ClickMouse(root)
    root.mainloop()
