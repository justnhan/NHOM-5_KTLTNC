import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUiType

# Load file .ui thành Class giao diện trước khi chạy code
current_dir = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseClass = loadUiType("CHINH.ui")

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # Khởi tạo giao diện từ file .ui vừa load
        
        # Viết code logic
        self.pushButton.clicked.connect(self.xu_ly_nut_bam)

    def xu_ly_nut_bam(self):
        self.label.setText("PyQt6 load trực tiếp thành công!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())