import sys
import os

# 1. Định nghĩa đường dẫn tuyệt đối đến thư mục chứa file Main.py
# Bạn có thể thay bằng đường dẫn thư mục thực tế của bạn nếu muốn cố định hẳn
thư_mục_chứa_code = r"C:\Users\User\Desktop\NHOM-5_KTLTNC"

# 2. Thêm thư mục này vào hệ thống tìm kiếm của Python để nó nhận diện được file Main.py
if thư_mục_chứa_code not in sys.path:
    sys.path.append(thư_mục_chứa_code)

from PyQt6.QtWidgets import QApplication, QMainWindow

# 3. Bây giờ Python có thể import trực tiếp file Main.py mà không lo lỗi đường dẫn
from Main import Ui_MainWindow 

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Nạp giao diện từ file Main.py vào cửa sổ
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # --- NƠI KẾT NỐI LOGIC NÚT BẤM ---
        # Kiểm tra xem nút bấm của bạn tên gì trong Qt Designer (Ví dụ: pushButton)
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(self.xu_ly_nut_bam)

    def xu_ly_nut_bam(self):
        print("Nút đã hoạt động hoàn hảo trên file .py!")
        # Nếu giao diện của bạn có một cái nhãn chữ tên là 'label'
        if hasattr(self.ui, 'label'):
            self.ui.label.setText("Kết nối giao diện thành công rực rỡ!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

