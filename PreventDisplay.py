# %%
import pyautogui
import time
import threading

class MouseMoverApp:
    def __init__(self):
        self.is_running = False
        self.move_thread = None

    def move_mouse_every_minute(self):
        """Di chuyển chuột mỗi phút nếu is_running là True."""
        while self.is_running:
            current_position = pyautogui.position()
            pyautogui.move(1, 0, duration=0.1)  # Di chuyển sang phải
            pyautogui.move(-1, 0, duration=0.1)  # Di chuyển về vị trí cũ
            print(f"Mouse moved at {time.strftime('%H:%M:%S')}")
            time.sleep(290)

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


