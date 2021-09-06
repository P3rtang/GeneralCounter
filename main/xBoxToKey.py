from inputs import get_gamepad
from keyboard import *
from time import *

while True:
    gamepad = get_gamepad()[0]
    print(gamepad.code)
    if gamepad.code == 'BTN_NORTH' and gamepad.state:
        send('+', do_release=False)
        sleep(0.1)
        send('+', do_press=False)
    elif gamepad.code == 'BTN_SOUTH' and gamepad.state:
        send('-', do_release=False)
        sleep(0.1)
        send('-', do_press=False)
    elif gamepad.code == 'BTN_EAST' and gamepad.state:
        send('*', do_release=False)
        sleep(0.1)
        send('*', do_press=False)
    sleep(0.01)