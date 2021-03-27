import threading
from pynput.mouse import Button
from pynput.keyboard import Listener, KeyCode


delay = 0.03
button = Button.left
start_stop_key = KeyCode(char='+')
exit_key = KeyCode(char='-')


class ClickMouse(threading.Thread):
    def __init__(self, overlay):
        super(ClickMouse, self).__init__()
        self.window = overlay

    def add_key(self):
        self.window.keyUp("<KeyRelease event state=Mod1 keysym=plus keycode=107 char='+' x=1299 y=698>")

    def min_key(self):
        self.window.keyUp("<KeyRelease event state=Mod1 keysym=plus keycode=107 char='-' x=1299 y=698>")

    def on_press(self, key):
        if key == start_stop_key:
            self.window.add_key()
        elif key == exit_key:
            self.window.min_key()

    with Listener(on_press=on_press) as listener:
        listener.join()
