# Auto clicker using pynput 2019-04-26
# 3rd version. Originally there were two files. One for the left mouse and one for the right.
# This version contains both, is cleaner, and has some new features.

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import sys


def get_delay():
    is_valid = False
    while not is_valid:
        try:
            delay = float(input("Enter a decimal for the delay between clicks: "))
            is_valid = True
        except ValueError:
            print("That is not a valid number.")
    return delay


def get_choice(choices):
    choice = ""
    while choice not in choices:
        choice = input("Press '[' to auto click left or ']' to auto click right: ")
    return choice


delay = get_delay()

button_choice = get_choice(['[', ']'])
if button_choice == '[':
    button = Button.left
elif button_choice == ']':
    button = Button.right
elif button_choice == '/':
    exit()


start_stop_key = KeyCode(char='o')
exit_key = KeyCode(char='/')

class ClickMouse(threading.Thread):
    clicks = 0

    def __init__(self, button):
        super(ClickMouse, self).__init__()
        self.button = button
        self.running = False
        self.program_running = True


    def start_clicking(self):
        self.running = True
        print("Activated")


    def stop_clicking(self):
        self.running = False
        print("Deactivated")


    def exit(self):
        self.stop_clicking()
        self.program_running = False


    def run(self):
        output = ""
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(delay)
                self.clicks += 1
            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(button)
click_thread.start()
print("Press the O key to start/stop auto clicking. Press '/' to terminate...")


def on_press(key):
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == exit_key:
        click_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()

listener.stop()

print("Clicked {} times".format(click_thread.clicks))
input("Press enter to exit...")
