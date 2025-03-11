# %%
import requests
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from io import BytesIO

# API mẫu trả về danh sách dữ liệu
API_URL = "https://jsonplaceholder.typicode.com/todos?_limit=6"

# URL ảnh mẫu
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSN0Y_SeJHZINmA_vwcN_rR71JW9wJXegQWiA&s"

# Hàm gửi request đến API và hiển thị dữ liệu
def fetch_data(root):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        display_data(data, root=root)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")

# Hàm hiển thị ảnh và thông tin lên giao diện
def display_data(data_list, root):
    for idx, data in enumerate(data_list):
        # Tải ảnh từ URL
        img_response = requests.get(IMAGE_URL)
        img_data = img_response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100))  # Resize ảnh
        photo = ImageTk.PhotoImage(img)

        # Hiển thị ảnh
        img_label = Label(root, image=photo)
        img_label.image = photo  # Lưu tham chiếu để tránh bị xóa
        img_label.grid(row=0, column=idx, padx=10, pady=10)

        # Hiển thị thông tin API
        info_text = f"ID: {data['id']}\nTitle: {data['title']}\nCompleted: {data['completed']}"
        info_label = Label(root, text=info_text, wraplength=100, justify="center")
        info_label.grid(row=1, column=idx, padx=10, pady=10)

def show_menu():
    # Tạo cửa sổ chính
    root_menu = tk.Tk()
    root_menu.title("API Data Viewer with Images")
    root_menu.geometry("800x300")

    fetch_data(root= root_menu)

    # Chạy vòng lặp giao diện
    root_menu.mainloop()


