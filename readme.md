pip install _requirements.txt
pyinstaller --onefile --windowed --add-data "icon:icon" --icon=icon/clock.png _main.py