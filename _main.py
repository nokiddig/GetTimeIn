# %%
# import os

# # Cài đặt từ requirements.txt
# os.system("pip install -r _requirements.txt")

# %%
import CountTime, MouseMoverApp, SalaryCal, ShowMenu, ImageBase64

import threading
import base64, io
from PIL import Image
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from datetime import datetime, timedelta, time
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QFont, QIcon, QMouseEvent, QAction, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMenu, QMessageBox
import sys, os

# Example usage
time_calculator = CountTime.TimeCalculator()
print (time_calculator.late)

#==========
mouse_mover = MouseMoverApp.MouseMoverApp()
mouse_mover.start_moving()
# #================================

# %%
def submit_time_in(hour: int, minute: int):
    global work_mode_index, end_time_str
    try:
        # Kiểm tra giá trị hợp lệ
        if 0 <= hour < 24 and 0 <= minute < 60:
            time_calculator.set_start_time(hour=hour, minute= minute)
            end_time_str = time_calculator.cal_end_time(work_mode_index)
        else:
            messagebox.showerror("Lỗi", "Giờ phải trong khoảng 0-23 và phút trong khoảng 0-59.")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")



# %%
  
class InputTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nhập Giờ và Phút")
        self.setFixedSize(180, 120)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        # Nhãn và ô nhập giờ
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Giờ:"))
        self.hour_entry = QLineEdit()
        row1.addWidget(self.hour_entry)
        row1.setStretch(0, 1)
        row1.setStretch(1, 1)
        layout.addLayout(row1)

        # Nhãn và ô nhập phút
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Phút:"))
        self.minute_entry = QLineEdit()
        row2.addWidget(self.minute_entry)
        row2.setStretch(0, 1)
        row2.setStretch(1, 1)
        layout.addLayout(row2)

        # Nút xác nhận
        confirm_button = QPushButton("OK")
        confirm_button.clicked.connect(self.submit_time_in)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def submit_time_in(self):
        try:
            hour = int(self.hour_entry.text())
            minute = int(self.minute_entry.text())
            print(f"Nhập thành công: {hour} giờ {minute} phút")  # Xử lý dữ liệu tại đây
            submit_time_in(hour, minute)
            # show message box
            if (time_calculator.is_late()):
                QMessageBox.about(self, "Hỏng", f"Bạn đến muộn {time_calculator.late} rồi cưng ạ")
            else:
                QMessageBox.about(self, "Tuyệt vời", f"Chúc bạn một ngày làm việc hiệu quả~")
            self.accept()  # Đóng cửa sổ khi nhấn OK
        except ValueError:
            print("Lỗi: Vui lòng nhập số hợp lệ")

# Mở dialog từ một function
def input_time_in():
    dialog = InputTimeDialog()
    dialog.exec()

# %%
# Danh sách các chế độ và chỉ số hiện tại
work_modes = ['CẢ NGÀY', 'SÁNG', 'SÁNG TRƯA', 'CHIỀU']
work_mode_index = 0

# chế độ bật tắt mouse mover
screen_modes = ["BẬT SCR", "TẮT SCR"]
screen_mode_index = 0

# Lấy giờ ra về từ chế độ hiện tại
mode = work_modes[work_mode_index]
end_time_str = time_calculator.cal_end_time(work_mode_index)

# %%
def get_icon(imageBase64):
    image_data = base64.b64decode(imageBase64)  # Chuyển base64 sang dạng binary
    image = Image.open(io.BytesIO(image_data))  # Load ảnh bằng PIL

    # Chuyển từ PIL Image sang QPixmap
    qimage = image.toqimage()
    pixmap = QPixmap.fromImage(qimage)

    # Tạo QIcon từ pixmap
    icon = QIcon(pixmap)
    return icon

# %%
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 120
        self.height = 60
        self.init_ui()
        self.init_feature()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("padding: 0px; margin: 0px; background-color: white;")
        self.setWindowFlags(self.windowFlags() | Qt.Tool) #hide on taskbar
        self.setAttribute(Qt.WA_QuitOnClose, True)
        # Lấy kích thước màn hình chính
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Tính toán vị trí góc dưới phải
        x = screen_geometry.width() - self.size().width()
        y = screen_geometry.height() - self.size().height() - 30
        self.move(x, y)  # Di chuyển widget đến vị trí tính toán

    def init_ui(self):
        # Hàng 1: 2 Button
        self.work_mode_btn = QPushButton(work_modes[work_mode_index])
        self.scr_mode_btn = QPushButton(screen_modes[screen_mode_index])
        btn_font = self.work_mode_btn.font()
        btn_font.setPointSize(8) 
        self.work_mode_btn.setFont(btn_font)
        self.scr_mode_btn.setFont(btn_font)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0,0,0,0)
        row1.addWidget(self.work_mode_btn)
        row1.addWidget(self.scr_mode_btn)

        # Hàng 2: Text lớn
        row2 = QHBoxLayout()
        
        lab_img_countdown = QLabel()
        icon_countdown = get_icon(ImageBase64.COUNTDOWN_BASE64)
        lab_img_countdown.setPixmap(icon_countdown.pixmap(20, 20))  # Icon đi kèm

        self.lab_remain_time = QLabel("00:00:00")
        self.lab_remain_time.setFont(QFont("Arial", 14, QFont.Bold))

        row2.addStretch(1)
        row2.addWidget(lab_img_countdown)
        row2.addWidget(self.lab_remain_time)
        row2.addStretch(1)

        # Hàng 3: 2 phần tử text với icon
        row3 = QHBoxLayout()
        row3.setContentsMargins(0, 0, 0, 0)

        # Phần tử 1: Icon đến + Text
        lab_img_start = QLabel()
        icon_start = get_icon(ImageBase64.COME_BASE64)
        lab_img_start.setPixmap(icon_start.pixmap(15, 20))  # Load icon
        self.lab_start_time = QLabel("00:00")
        self.lab_start_time.setFont(QFont("Arial", 10))

        container1 = QHBoxLayout()
        container1.setContentsMargins(0, 0, 0, 0)
        container1.addStretch(1)
        container1.addWidget(lab_img_start)
        container1.addWidget(self.lab_start_time)
        container1.addStretch(1)

        widget1 = QWidget()
        widget1.setLayout(container1)

        # Phần tử 2: Icon đi + Text
        lab_img_out = QLabel()
        icon_out = get_icon(ImageBase64.OUT_BASE64)
        lab_img_out.setPixmap(icon_out.pixmap(15, 20))  # Load icon
        self.lab_end_time = QLabel("00:00")
        self.lab_end_time.setFont(QFont("Arial", 10))

        container2 = QHBoxLayout()
        container2.setContentsMargins(0, 0, 0, 0)
        container2.addStretch(1)
        container2.addWidget(lab_img_out)
        container2.addWidget(self.lab_end_time)
        container2.addStretch(1)

        widget2 = QWidget()
        widget2.setLayout(container2)

        row3.addWidget(widget1)
        row3.addWidget(widget2)

        # Layout chính
        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        self.setLayout(layout)
        self.setFixedSize(self.width, self.height)

    #Hàm tính và hiển thị thời gian còn lại
    def auto_refresh_ui(self):
        now = datetime.now()
        #show lunch
        if now.hour == 11 and now.minute == 30 and now.second == 0:
            self.lunch_menu()
        elif now.hour == 17 and now.minute == 0 and now.second == 0:
            QMessageBox.about(self, "Hi Nghẹo", "Tuyệt vời")
        
        # Thiết lập thời gian ra về theo giờ phút, giữ nguyên ngày hiện tại
        end_time = datetime.strptime(end_time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )

        # Cập nhật nhãn thời gian
        self.lab_end_time.setText(f"{end_time.strftime('%H:%M')}")
        self.lab_start_time.setText(f"{time_calculator.start_time.strftime('%H:%M')}")
        
        #Tgian còn lại
        if end_time>now:
            remaining_time = end_time - now
            self.lab_remain_time.setText(f"{str(remaining_time).split('.')[0]}")
        else:
            remaining_time = now - end_time
            self.lab_remain_time.setText(f"+{str(remaining_time).split('.')[0]}")


    def init_feature(self):
        self.work_mode_btn.clicked.connect(self.switch_work_mode)
        self.scr_mode_btn.clicked.connect(self.switch_screen_mode)
        self.timer = QTimer(self)  
        self.timer.timeout.connect(self.auto_refresh_ui)  # Gán hàm update
        self.timer.start(1000)
        self.create_tray_icon()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        print("Double click")
        self.hide_window()

    # Hàm cập nhật chế độ làm việc
    def switch_work_mode(self):
        print("Switch work mode")
        global work_mode_index, end_time_str
        work_mode_index = (work_mode_index + 1) % len(work_modes)
        self.work_mode_btn.setText(work_modes[work_mode_index])
        end_time_str = time_calculator.cal_end_time(work_mode_index)

    # Hàm cập nhật chế độ screen
    def switch_screen_mode(self):
        print("Switch screen mode")
        global screen_modes, screen_mode_index, mouse_mover
        screen_mode_index = 1 - screen_mode_index
        self.scr_mode_btn.setText(screen_modes[screen_mode_index])

        mode_on = 0
        if screen_mode_index == mode_on:
            mouse_mover.start_moving()
        else:
            mouse_mover.stop_moving() 

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:  
            self.show_context_menu(event.globalPosition().toPoint())

    # Sự kiện khi kéo chuột
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    # Sự kiện khi nhả chuột
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.offset = None

     # Hiển thị menu chuột phải
    def show_context_menu(self, pos: QPoint):
        print("right click")
        menu = QMenu(self)

        # Các tùy chọn
        action_input_time_in = QAction("Input Time In", self)
        action_lunch_menu = QAction("Lunch Menu", self)
        action_hide_window = QAction("Hide Window", self)
        action_quit_app = QAction("Quit App", self)

        # Gán sự kiện
        action_input_time_in.triggered.connect(input_time_in)
        action_lunch_menu.triggered.connect(self.lunch_menu)
        action_hide_window.triggered.connect(self.hide_window)
        action_quit_app.triggered.connect(self.quit_app)

        # Thêm vào menu
        menu.addAction(action_input_time_in)
        menu.addAction(action_lunch_menu)
        menu.addAction(action_hide_window)
        menu.addAction(action_quit_app)

        # Hiển thị menu
        menu.exec(pos)

    def lunch_menu(self):
        lunch_menu = ShowMenu.ShowMenuWindow()
        lunch_menu.show()
    
    def hide_window(self):
        self.hide()

    def show_app(self):
        self.show()  
    
    def create_tray_icon(self):
        global window
        
        # Sử dụng hình ảnh icon.png thay vì tạo hình chữ nhật màu xanh
        icon_path = "icon/clock.png"
        image = Image.open(icon_path)

        # Tạo menu cho tray icon
        menu = Menu(
            MenuItem("Show", self.show_app),
            MenuItem("Exit", self.quit_app)
        )

        # Khởi tạo tray icon với hình ảnh
        self.tray_icon = Icon("SAT_Input", image, "SAT Input", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def quit_app(self):
        self.tray_icon.stop()
        QApplication.instance().quit()  # Thoát ứng dụng

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


