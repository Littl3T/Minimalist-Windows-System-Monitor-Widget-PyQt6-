from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QTimer
import psutil
import sys
import time

def format_speed(bits_per_second):
    if bits_per_second > 1e6:
        return f"{bits_per_second / 1e6:.2f} Mbit/s"
    else:
        return f"{bits_per_second / 1e3:.2f} Kbit/s"

def get_disk_usage():
    disk = psutil.disk_usage("C:\\")
    total = disk.total / 1e9
    used = disk.used / 1e9
    percent = disk.percent
    bar_length = 10 # You can change the size to make it more accurate, but you might need to make the screen size bigger on line 32 for example self.setGeometry(25, 25, 650 (was 450), 180) 
    filled_blocks = int((percent / 100) * bar_length)
    empty_blocks = bar_length - filled_blocks
    progress_bar = "[" + "█" * filled_blocks + " " * empty_blocks + "]"
    return f"{progress_bar} {percent:.1f}% ({used:.1f} / {total:.1f} Go)"

class DesktopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnBottomHint |  
                            Qt.WindowType.Tool)  
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  
        self.setGeometry(25, 25, 450, 180)  
        self.setStyleSheet("color: white; font-size: 17px; font-family: Consolas;")  
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  
        self.update_stats()  

    def update_stats(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        new_net = psutil.net_io_counters()
        new_time = time.time()
        delta_time = new_time - self.last_time
        download_speed = (new_net.bytes_recv - self.last_net.bytes_recv) * 8 / delta_time
        upload_speed = (new_net.bytes_sent - self.last_net.bytes_sent) * 8 / delta_time
        self.last_net = new_net
        self.last_time = new_time
        disk_bar = get_disk_usage()
        text = (f"CPU: {cpu:.1f}%\n"
                f"RAM: {ram:.1f}%\n"
                f"↓ {format_speed(download_speed)}  ↑ {format_speed(upload_speed)}\n"
                f"\nC: {disk_bar}")
        self.label.setText(text)
app = QApplication(sys.argv)
widget = DesktopWidget()
widget.show()
sys.exit(app.exec())
