import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal

# 1. Định vị thư mục hiện tại và đường dẫn đến file .ui của Dialog
BASE_DIR = Path(__file__).resolve().parent
# CHÚ Ý: Đã điền đúng tên file .ui của bạn (Long - đổi tên file.ui)
UI_PATH = BASE_DIR / 'Long - đổi tên file.ui'

# 2. Tạo lớp giao diện kế thừa từ QDialog
class MyWindow(QtWidgets.QDialog):
    # Tạo một tín hiệu tùy chỉnh để gửi tên file mới về giao diện chính (nếu cần)
    tin_hieu_doi_ten_xong = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # 3. Nạp file UI của Dialog (ép kiểu sang chuỗi để tránh lỗi)
        uic.loadUi(str(UI_PATH), self)
        
        # --- KẾT NỐI CÁC THÀNH PHẦN TRÊN DIALOG TẠI ĐÂY ---
        # Ví dụ kết nối nút bấm để kiểm tra chức năng:
        # Giả sử nút bấm của bạn tên là btn_xac_nhan
        # self.btn_xac_nhan.clicked.connect(self.nut_xac_nhan_clicked)

    def nut_xac_nhan_clicked(self):
        # Ví dụ: Lấy dữ liệu người dùng nhập từ ô txt_ten_moi
        # ten_moi = self.txt_ten_moi.text()
        
        # Phát tín hiệu gửi tên mới về file chính
        # self.tin_hieu_doi_ten_xong.emit(ten_moi)
        
        # Đóng dialog sau khi bấm xác nhận
        self.accept() 


