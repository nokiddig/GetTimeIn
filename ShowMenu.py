# %%
# from PySide6.QtWidgets import QLabel, QDialog, QVBoxLayout
# from PySide6.QtGui import QPixmap, QImage
# from PySide6.QtCore import Qt
# from PIL import Image
# from io import BytesIO

# class HoverableImage(QLabel):
#     def __init__(self, img_data, parent=None):
#         super().__init__(parent)
#         self.img_data = img_data
#         self.popup = None

#         # Xử lý ảnh từ bytes
#         img = Image.open(BytesIO(self.img_data))
#         img = img.resize((parent.col_width, parent.col_width))  # Resize ảnh ban đầu
#         img = img.convert("RGBA")  # Đảm bảo có kênh alpha

#         # Chuyển ảnh từ PIL sang QImage
#         img_qt = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
#         pixmap = QPixmap.fromImage(img_qt)
#         self.setPixmap(pixmap)

#     def enterEvent(self, event):
#         """Khi hover vào ảnh, hiển thị ảnh phóng to."""
#         if self.popup is None:
#             self.popup = QDialog(self, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#             self.popup.setAttribute(Qt.WA_TranslucentBackground)
#             self.popup.setStyleSheet("background: transparent;")

#             layout = QVBoxLayout(self.popup)
#             label = QLabel(self.popup)
            
#             # Xử lý ảnh phóng to
#             img = Image.open(BytesIO(self.img_data))
#             img = img.resize((300, 300))  # Kích thước phóng to
#             img = img.convert("RGBA")

#             img_qt = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)
#             pixmap = QPixmap.fromImage(img_qt)
#             label.setPixmap(pixmap)

#             layout.addWidget(label)
#             self.popup.setLayout(layout)
#             self.popup.setFixedSize(300, 300)

#             # Đặt vị trí popup gần ảnh gốc
#             self.popup.move(self.mapToGlobal(self.rect().bottomRight()))
#             self.popup.show()

#     def leaveEvent(self, event):
#         """Khi rời chuột khỏi ảnh, đóng popup."""
#         if self.popup:
#             self.popup.close()
#             self.popup = None

# # ==== Sử dụng lớp HoverableImage trong layout ====
# img_label = HoverableImage(img_response.content, self)
# image_layout.addWidget(img_label)

# %%
import sys
import requests
from io import BytesIO
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PIL import Image, ImageQt
from datetime import datetime

# API mẫu trả về danh sách dữ liệu
day_str = datetime.now().strftime("%Y-%m-%d")
API_URL = "http://107.113.53.166/"
MENU_API = f"{API_URL}api/menu/get-menu?date={day_str}"
DEFAULT_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN0Y_SeJHZINmA_vwcN_rR71JW9wJXegQWiA&s"

class ShowMenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 900
        self.height = 300
        self.col_width = 150
        self.setWindowTitle("API Data Viewer with Images")
        self.setGeometry(100, 100, self.width, self.height)

        # Layout chính
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def fetch_data(self):
        """ Gửi request đến API và hiển thị dữ liệu """
        try:
            value_field = "value"
            response = requests.get(MENU_API, verify=False)
            response.raise_for_status()
            data = response.json()[value_field]
            self.display_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")

    def display_data(self, data_list):
        """ Hiển thị ảnh và thông tin API lên giao diện """
        image_layout = QHBoxLayout()
        text_layout = QHBoxLayout()

        for data in data_list:
            # Tải ảnh từ URL
            try:
                image_url = data["image"] 
                img_response = requests.get(f"{API_URL}{image_url}", verify=False)
            except Exception as e:
                img_response = requests.get(DEFAULT_IMAGE_URL, verify=False)
            img_data = img_response.content
            
            # Mở ảnh bằng PIL, resize và chuyển thành QImage
            img = Image.open(BytesIO(img_data))
            img = img.resize((self.col_width, self.col_width))  # Resize ảnh
            img = img.convert("RGBA")  # Đảm bảo ảnh có kênh alpha (nếu cần)

            # Chuyển ảnh từ PIL sang QImage
            img_qt = QImage(img.tobytes(), img.width, img.height, QImage.Format_RGBA8888)

            # Chuyển QImage sang QPixmap
            pixmap = QPixmap.fromImage(img_qt)

            # Hiển thị ảnh
            img_label = QLabel(self)
            img_label.setPixmap(pixmap)
            image_layout.addWidget(img_label)

            # Hiển thị từng thông tin riêng biệt trên các QLabel
            corner_label = QLabel(f"Corner: {data['corner']}", self)
            main_label = QLabel(f"Main: {data['main']}", self)
            dishes_label = QLabel(f"Dishes: {data['dishes']}", self)
            kcal_label = QLabel(f"Kcal: {data['kcal']}", self)

            # Căn chỉnh kích thước, nếu cần
            corner_label.setFixedWidth(self.col_width)
            main_label.setFixedWidth(self.col_width)
            dishes_label.setFixedWidth(self.col_width)
            kcal_label.setFixedWidth(self.col_width)

            # Thêm các QLabel vào layout
            text_layout.addWidget(corner_label)
            text_layout.addWidget(main_label)
            text_layout.addWidget(dishes_label)
            text_layout.addWidget(kcal_label)

        self.main_layout.addLayout(image_layout)
        self.main_layout.addLayout(text_layout)

    def show(self):
        super().show()
        self.fetch_data()


# %%
# app = QApplication(sys.argv)
# lunch_menu = ShowMenuWindow()
# lunch_menu.show()
# app.exec()


