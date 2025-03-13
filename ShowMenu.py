# %%
import sys
import requests
from io import BytesIO
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap
from PIL import Image

# API mẫu trả về danh sách dữ liệu
API_URL = "https://jsonplaceholder.typicode.com/todos?_limit=6"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN0Y_SeJHZINmA_vwcN_rR71JW9wJXegQWiA&s"

class ShowMenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API Data Viewer with Images")
        self.setGeometry(100, 100, 800, 300)

        # Layout chính
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.fetch_data()

    def fetch_data(self):
        """ Gửi request đến API và hiển thị dữ liệu """
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            self.display_data(data)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")

    def display_data(self, data_list):
        """ Hiển thị ảnh và thông tin API lên giao diện """
        image_layout = QHBoxLayout()
        text_layout = QHBoxLayout()

        for data in data_list:
            # Tải ảnh từ URL
            img_response = requests.get(IMAGE_URL)
            img_data = img_response.content

            # Mở ảnh bằng PIL, resize và chuyển thành QPixmap
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100))
            img_qt = QPixmap()
            img_qt.loadFromData(BytesIO(img_data).read())

            # Hiển thị ảnh
            img_label = QLabel(self)
            img_label.setPixmap(img_qt)
            image_layout.addWidget(img_label)

            # Hiển thị thông tin API
            info_text = f"ID: {data['id']}\nTitle: {data['title']}\nCompleted: {data['completed']}"
            info_label = QLabel(info_text, self)
            info_label.setWordWrap(True)
            info_label.setFixedWidth(100)  # Giữ văn bản không bị tràn
            text_layout.addWidget(info_label)

        self.main_layout.addLayout(image_layout)
        self.main_layout.addLayout(text_layout)



