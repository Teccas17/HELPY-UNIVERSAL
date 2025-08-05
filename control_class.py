import configparser
import os
import time
import serial
import win32api
import win32con

# Load settings from config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

USE_MAKCU = config.getboolean('Settings', 'use_makcu', fallback=False)
MAKCU_PORT = config.get('Settings', 'makcu_port', fallback='COM3')

class MakcuInterface:
    def __init__(self, com_port=MAKCU_PORT, baudrate=4000000):
        try:
            self.serial = serial.Serial(port=com_port, baudrate=baudrate, timeout=0)
            time.sleep(2)
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
        self.send_command(f"CLICK {button.upper()}")

    def release(self, button='left'):
        self.send_command(f"RELEASE {button.upper()}")

class Control:
    def __init__(self):
        self.use_makcu = USE_MAKCU
        self.makcu = MakcuInterface() if self.use_makcu else None

    def move_mouse(self, dx, dy):
        if self.use_makcu and self.makcu:
            self.makcu.move(dx, dy)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)

    def click_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.click(button)
        else:
            down = win32con.MOUSEEVENTF_LEFTDOWN if button == 'left' else win32con.MOUSEEVENTF_RIGHTDOWN
            up = win32con.MOUSEEVENTF_LEFTUP if button == 'left' else win32con.MOUSEEVENTF_RIGHTUP
            win32api.mouse_event(down, 0, 0, 0, 0)
            win32api.mouse_event(up,   0, 0, 0, 0)

    def press_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.click(button)
        else:
            down = win32con.MOUSEEVENTF_LEFTDOWN if button == 'left' else win32con.MOUSEEVENTF_RIGHTDOWN
            win32api.mouse_event(down, 0, 0, 0, 0)

    def release_mouse(self, button='left'):
        if self.use_makcu and self.makcu:
            self.makcu.release(button)
        else:
            up = win32con.MOUSEEVENTF_LEFTUP if button == 'left' else win32con.MOUSEEVENTF_RIGHTUP
            win32api.mouse_event(up, 0, 0, 0, 0)

