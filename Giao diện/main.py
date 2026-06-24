import sys
import os
from pathlib import Path
from PyQt6 import QtWidgets, uic
from DoiTenFile import MyWindow

# 1. Lấy đường dẫn của thư mục chứa file CHINH.py hiện tại
BASE_DIR = Path(__file__).resolve().parent

# 2. Tạo đường dẫn chính xác đến file .ui của bạn
# CHÚ Ý: Hãy thay 'giao_dien_chinh.ui' thành đúng tên file ui chính của bạn
UI_PATH = BASE_DIR / 'CHINH.ui'

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 3. Nạp file UI bằng biến Path đã ép kiểu sang chuỗi (str)
        uic.loadUi(str(UI_PATH), self)
        
        # --- Nơi kết nối nút bấm sau này ---

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    giao_dien_chinh = MainApp()
    giao_dien_chinh.show()
    form = MyWindow()  # Tạo instance của dialog
    form.show()  # Hiển thị dialog
    sys.exit(app.exec())