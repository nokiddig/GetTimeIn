# cào thư viện
pip install -r _requirements.txt

# Xuât file .exe
pyinstaller --onefile --windowed --icon=icon/clock.png --name=SAT_Input.exe _main.py

## Copy /icon vào trong /dist nếu chạy lỗi