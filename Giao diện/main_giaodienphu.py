import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal

# 1. Định vị thư mục hiện tại và đường dẫn đến file .ui của Dialog
BASE_DIR = Path(__file__).resolve().parent


# CHÚ Ý: cái đám này là đừng dẫn đến file ui nhé!
UI1_PATH = BASE_DIR / 'Long - đổi tên file.ui'
UI3_PATH = BASE_DIR / 'Long - xem thuộc tính.ui'
UI5_PATH = BASE_DIR / 'Tạo file.ui'
UI6_PATH = BASE_DIR / 'Tạo thư mục.ui'
UI7_PATH = BASE_DIR / 'tree_panel.ui'

# 2. Tạo các lớp giao diện kế thừa từ QDialog

class Doi_Ten_File(QtWidgets.QDialog):
    # Tạo một tín hiệu tùy chỉnh để gửi tên file mới về giao diện chính (nếu cần)
    tin_hieu_doi_ten_xong = pyqtSignal(str)

    def __init__(self, parent_node, old_name):
        super().__init__()

        uic.loadUi(str(UI1_PATH), self)

        self.parent_node = parent_node
        self.old_name = old_name

        self.buttonBox.accepted.connect(self.xac_nhan)

        self.buttonBox.rejected.connect(self.reject)

    def xac_nhan(self):

        ten_moi = self.txtNewname.text().strip()

        # Tên rỗng
        if not ten_moi:
            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Tên không được để trống!"
            )
            return

        # Trùng tên cũ
        if ten_moi == self.old_name:
            QtWidgets.QMessageBox.information(
                self,
                "Thông báo",
                "Tên mới phải khác tên cũ! À thật ra thì không khác cũng đc:)"
            )
        

        # Trùng tên cùng cấp
        node_con = self.parent_node.children.head

        while node_con:

            if (
                node_con.name == ten_moi
                and node_con.name != self.old_name
            ):
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Tên đã tồn tại!"
                )
                return

            node_con = node_con.next

        # Hợp lệ -> gửi về MainWindow
        self.tin_hieu_doi_ten_xong.emit(
            ten_moi
        )

        self.accept()



    
    # tương tự ở trên nhé ae

class Xem_Thuoc_Tinh(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI3_PATH), self)
        # Kết nối các nút bấm tại đây 
    

class Tao_File(QtWidgets.QDialog):

    tao_file_xong = pyqtSignal(str,int)

    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI5_PATH), self)
        # Kết nối các nút bấm tại đây

        self.btnOK.clicked.connect(
            self.xac_nhan
        )

        self.btnKOK.clicked.connect(
            self.huy
        )

    def xac_nhan(self):

        ten = self.txtName.text().strip()
        loai = self.cboLoai.currentText()
        size = self.txtSize.text().strip()
        don_vi = self.cboCo.currentText()

        if not ten:
            QtWidgets.QMessageBox.warning(self,"Lỗi","Tên file không được để trống!")
            return

        try:

                size = float(size)

                if size <= 0:

                    QtWidgets.QMessageBox.warning(
                        self,
                        "Lỗi",
                        "Kích thước phải lớn hơn 0!"
                    )

                    return

        except ValueError:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Kích thước không hợp lệ!"
                )

                return

        ten_file = f"{ten}.{loai}"


        if don_vi == "KB":
                size_kb = int(size)
        elif don_vi == "MB":
                size_kb = int(size * 1024)
        elif don_vi == "GB":
                size_kb = int(size * 1024 * 1024)
        else:
            size_kb = int(size)
        self.tao_file_xong.emit(ten_file,size_kb)
        self.accept()
    def huy(self):

        QtWidgets.QMessageBox.information(
            self,
            "Thông báo",
            "Đã hủy tạo file."
        )

        self.reject()

class Tao_Thu_Muc(QtWidgets.QDialog):
    tao_thu_muc_xong = pyqtSignal(str)
    def __init__(self, parent_node):
        super().__init__()
        uic.loadUi(str(UI6_PATH), self)

        self.parent_node = parent_node
        
        self.btnOK.clicked.connect(
            self.xac_nhan)
        self.btnKOK.clicked.connect(
            self.huy)
        
    def xac_nhan(self):

        ten_thu_muc = (
            self.txtName.text().strip()
        )

        if not ten_thu_muc:

            QtWidgets.QMessageBox.warning(
                self,
                "Lỗi",
                "Tên thư mục không được để trống!"
            )

            return

        node_con = (
            self.parent_node.children.head
        )

        while node_con:

            if node_con.name == ten_thu_muc:

                QtWidgets.QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Tên thư mục đã tồn tại!"
                )

                return

            node_con = node_con.next

        self.tao_thu_muc_xong.emit(
            ten_thu_muc
        )

        self.accept()

    def huy(self):

        QtWidgets.QMessageBox.information(
            self,
            "Thông báo",
            "Đã hủy tạo thư mục."
        )

        self.reject()



class Tree_Panel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UI7_PATH), self)
        # Kết nối các nút bấm tại đây
