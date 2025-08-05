# makcu_interface.py
import serial
import time

class MakcuInterface:
    def __init__(self, com_port='COM3', baudrate=4000000):
        try:
            self.serial = serial.Serial(port=com_port, baudrate=baudrate, timeout=0)
            time.sleep(2)  # wait for device to initialize
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
