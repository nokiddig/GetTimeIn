# cào thư viện
pip install -r _requirements.txt

# Xuât file .exe
pyinstaller --onefile --windowed --icon=icon/clock.png --name=SAT_Input.exe _main.py
Copy /icon vào trong /dist nếu chạy lỗi

#
Quên chưa cho anh chị dùng thử app, a chị thấy cần thiết thì tải ở đây ạ: http://107.98.74.105/SAT_Input.exe
Feature: 
- tính giờ sáng/chiều/cả ngày
- xem ngày, tuần, tgian muộn(hover vào)
- Ko tắt màn hình(ko dùng thì có thể tắt, nếu sleep máy thì cần bấm tắt rồi bật lại cho nó nhận :v)
- Xem đồ ăn trưa (tự động 11h30 hoặc tự bấm show)
- Ẩn hiện bằng double click, kể cả menu trưa.
- Tray icon dùng khi muốn ẩn cửa sổ mà ko tắt hẳn