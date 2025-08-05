import time
import serial
import win32api
import win32con
import configparser
import os

# Load config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

use_makcu = config.getboolean('Settings', 'use_makcu', fallback=False)
makcu_port = config.get('Settings', 'makcu_port', fallback='COM3')

# ---- Makcu Interface ----
class MakcuInterface:
    def __init__(self, com_port='COM3', baudrate=4000000):
        try:
            self.serial = serial.Serial(port=com_port, baudrate=baudrate, timeout=0)
            time.sleep(2)  # allow time for Makcu to initialize
            print(f"[Makcu] Connected on {com_port}")
        except Exception as e:
            print(f"[Makcu] Failed to connect: {e}")
            self.serial = None

    def send_command(self, cmd: str):
        if self.serial and self.serial.is_open:
            self.serial.write((cmd + '\n').encode('utf-8'))

    def move(self, dx: int, dy: int):
        self.send_command(f"MOVE {dx} {dy}")

    def click(self, button='left'):
        if button == 'left':
            self.send_command("CLICK LEFT")
        elif button == 'right':
            self.send_command("CLICK RIGHT")

    def release(self, button='left'):
        if button == 'left':
            self.send_command("RELEASE LEFT")
        elif button == 'right':
            self.send_command("RELEASE RIGHT")


# ---- Control Class ----
class Control:
    def __init__(self, use_makcu=False, makcu_port='COM3'):
        self.use_makcu = use_makcu
        self.makcu = None
        if self.use_makcu:
            self.makcu = MakcuInterface(com_port=makcu_port)

    def move_mouse(self, dx, dy):
        if self.use_makcu and self.makcu:
            self.makcu.move(dx, dy)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)

    def click_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.click(button)
        else:
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def press_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.click(button)
        else:
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    def release_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.release(button)
        else:
            if button == 'left':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif button == 'right':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


