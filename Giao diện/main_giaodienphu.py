import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal

# 1. Định vị thư mục hiện tại và đường dẫn đến file .ui của Dialog
BASE_DIR = Path(__file__).resolve().parent


# CHÚ Ý: cái đám này là đừng dẫn đến file ui nhé!
UI1_PATH = BASE_DIR / 'Long - đổi tên file.ui'
UI2_PATH = BASE_DIR / 'Long - xác nhận xóa.ui'
UI3_PATH = BASE_DIR / 'Long - xem thuộc tính.ui'
UI4_PATH = BASE_DIR / 'Lỗi.ui'
UI5_PATH = BASE_DIR / 'Tạo file.ui'
UI6_PATH = BASE_DIR / 'Tạo thư mục.ui'
UI7_PATH = BASE_DIR / 'tree_panel.ui'

# 2. Tạo các lớp giao diện kế thừa từ QDialog

class Doi_Ten_File(QtWidgets.QDialog):
    # Tạo một tín hiệu tùy chỉnh để gửi tên file mới về giao diện chính (nếu cần)
    tin_hieu_doi_ten_xong = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        # 3. Nạp file UI của Dialog (ép kiểu sang chuỗi để tránh lỗi)
        uic.loadUi(str(UI1_PATH), self)
        
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

class Xac_Nhan_Xoa(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI2_PATH), self)
        # Kết nối các nút bấm tại đây 
    
    # tương tự ở trên nhé ae

class Xem_Thuoc_Tinh(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI3_PATH), self)
        # Kết nối các nút bấm tại đây 
    
class Loi(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI4_PATH), self)
        # Kết nối các nút bấm tại đây
    

class Tao_File(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI5_PATH), self)
        # Kết nối các nút bấm tại đây

class Tao_Thu_Muc(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI6_PATH), self)
        # Kết nối các nút bấm tại đây

class Tree_Panel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI7_PATH), self)
        # Kết nối các nút bấm tại đây

