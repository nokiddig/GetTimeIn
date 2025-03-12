# %%
import pyautogui
import time
import threading
from pynput.mouse import Controller, Button

class MouseMoverApp:
    def __init__(self):
        self.is_running = False
        self.move_thread = None

    def move_mouse_every_minute(self, milisecond = 299):
        """Di chuyển chuột mỗi phút nếu is_running là True."""
        mouse = Controller()
        while self.is_running:
            mouse.scroll(0, 1)
            time.sleep(0.001)
            mouse.scroll(0, -1)
            time.sleep(milisecond)

    def start_moving(self):
        """Bắt đầu di chuyển chuột."""
        if not self.is_running:
            self.is_running = True
            # Chạy di chuyển chuột trong luồng khác để không làm đơ giao diện
            self.move_thread = threading.Thread(target=self.move_mouse_every_minute)
            self.move_thread.daemon = True
            self.move_thread.start()

    def stop_moving(self):
        """Dừng di chuyển chuột."""
        self.is_running = False


