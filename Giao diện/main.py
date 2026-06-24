import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from pathlib import Path
from PyQt6.uic import loadUiType
from PyQt6.QtGui import QFont
from PyQt6 import uic


class MyWindow(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        # Lấy thư mục chứa chính file Python này
        current_dir = Path(__file__).parent
        # Ghép nối chính xác tới file CHINH.ui
        ui_path = current_dir / "CHINH.ui"
        
        # Load file UI bằng đường dẫn tuyệt đối vừa tạo
        uic.loadUi(str(ui_path), self)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())