import sys
import os
from pathlib import Path
from PyQt6 import QtWidgets, uic
from DoiTenFile import MyWindow
from Backend_code import FileSystemTree

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
        

        self.fs = FileSystemTree()

        # ==========================
        # KẾT NỐI SIGNAL
        # ==========================

        self.connect_signals()

        # ==========================
        # LOAD DỮ LIỆU BAN ĐẦU
        # ==========================

        # self.load_data()



    # ==================================================
    # KẾT NỐI TOÀN BỘ NÚT BẤM
    # ==================================================

    def connect_signals(self):
        """
        Gom toàn bộ connect vào đây.

        Mục đích:
        - Dễ đọc
        - Dễ sửa
        - __init__ gọn hơn

        Ví dụ:
        self.btnSave.clicked.connect(self.save_data)
        """



    # ==================================================
    # REFRESH GIAO DIỆN
    # ==================================================

    def refresh_all(self):
        """
        Hàm tổng.

        Gọi:
            refresh_tree_view()
            refresh_table_view()
            refresh_path()

        Mỗi khi dữ liệu thay đổi
        chỉ cần gọi:

            self.refresh_all()
        """



    def refresh_tree_view(self):
        """
        Đổ toàn bộ cây thư mục lên TreeView.

        Dữ liệu lấy từ:

            self.fs.root

        Sử dụng:

            QStandardItemModel

        Hàm tree_ui() của bạn
        sẽ cực kỳ hữu ích ở đây.
        """



    def refresh_table_view(self):
        """
        Hiển thị danh sách con
        của current_working_dir.

        Hiển thị:

            Name
            Type
            Size
            Created At

        Đây chính là chức năng ls.
        """



    def refresh_path(self):
        """
        Hiển thị đường dẫn hiện tại.

        Ví dụ:

            C:/Documents/Python

        lên txtPath.
        """



    # ==================================================
    # ĐIỀU HƯỚNG THƯ MỤC
    # ==================================================

    def go_home(self):
        """
        Nút Home.

        current_working_dir = root

        Sau đó refresh.
        """



    def go_back(self):
        """
        Nút Back.

        Gọi:

            self.fs.go_back()

        Sau đó refresh.
        """



    def change_directory(self, node):
        """
        Đổi thư mục hiện tại.

        current_working_dir = node

        Sau đó refresh.
        """



    # ==================================================
    # THAO TÁC FILE/FOLDER
    # ==================================================

    def add_folder(self):
        """
        btnAddFolder

        Hỏi tên thư mục mới.

        Gọi:

            self.fs.add_folder(...)

        Sau đó refresh.
        """



    def add_file(self):
        """
        btnAddFile

        Hỏi:

            tên file
            dung lượng

        Gọi:

            self.fs.create_file(...)

        Sau đó refresh.
        """



    def rename_node(self):
        """
        Đổi tên node đang chọn.

        Có thể:

            QInputDialog

        hoặc

            form DoiTenFile

        Gọi:

            self.fs.rename_node(...)
        """



    def delete_node(self):
        """
        Xóa node đang chọn.

        Gọi:

            self.fs.rm_rf(...)

        vì rm_rf xử lý được
        cả file và folder.

        Nên hỏi xác nhận trước.
        """



    # ==================================================
    # TÌM KIẾM
    # ==================================================

    def search_by_name(self):
        """
        Tìm kiếm theo txtSearch.

        Gọi:

            self.fs.search_by_name()

        Sau đó hiển thị kết quả
        lên TableView.
        """



    def search_by_filter(self):
        """
        Dùng cboFilter.

        Ví dụ:

            Folder
            .txt
            .pdf

        Gọi:

            search_by_extension()
            search_by_type()

        tùy lựa chọn.
        """



    # ==================================================
    # TREEVIEW
    # ==================================================

    def on_tree_clicked(self, index):
        """
        Khi click TreeView.

        Lấy node tương ứng.

        Đổi current_working_dir.

        Refresh TableView.
        """



    # ==================================================
    # TABLEVIEW
    # ==================================================

    def on_table_double_clicked(self, index):
        """
        Double click.

        Nếu là folder:

            change_directory()

        Nếu là file:

            không làm gì
            hoặc hiện thông tin.
        """



    def get_selected_node(self):
        """
        Hàm cực kỳ quan trọng.

        Trả về node đang chọn.

        Sau này:

            rename
            delete
            info

        đều dùng hàm này.
        """



    # ==================================================
    # JSON
    # ==================================================

    def save_data(self):
        """
        btnSave

        Gọi:

            self.fs.save_to_json()

        Sau đó hiện:

            Saved successfully
        """



    def load_data(self):
        """
        btnOpen

        Gọi:

            self.fs.load_from_json()

        Sau đó refresh.
        """



    # ==================================================
    # THÔNG TIN
    # ==================================================

    def show_info(self):
        """
        btnAllInfo

        Hiển thị:

            tên
            loại
            kích thước
            ngày tạo
            đường dẫn

        của node đang chọn.
        """



    def search_by_size(self):
        """
        btnSearchbysize

        Hỏi:

            min size
            max size

        Gọi:

            self.fs.search_by_size()
        """



    # ==================================================
    # HELP
    # ==================================================

    def show_contact(self):
        """
        btnContact

        Hiển thị thông tin nhóm.
        """


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    giao_dien_chinh = MainApp()
    giao_dien_chinh.show()
    sys.exit(app.exec())