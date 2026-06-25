import sys
import os
from pathlib import Path

# 1. Lấy đường dẫn của thư mục chứa file CHINH.py hiện tại
BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent  # Đường dẫn của thư mục cấp lớn hơn

if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from main_giaodienphu import *
from Backend_code import FileSystemTree




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
        self.load_data()

        # ==========================
        # LOAD DỮ LIỆU BAN ĐẦU
        # ==========================

        # self.load_data()



    # ==================================================
    # KẾT NỐI TOÀN BỘ NÚT BẤM
    # ==================================================

    def connect_signals(self):
    # ===== Thanh điều hướng =====

        self.btnHome.clicked.connect(
            self.go_home
        )

        self.btnBack.clicked.connect(
            self.go_back
        )



        self.cboFilter.currentTextChanged.connect(
            self.search_nodes
        )



        self.btnNewfolder.clicked.connect(
            self.add_folder
        )

        self.btnSave.clicked.connect(
            self.save_file
        )

        # ===== Edit =====

        self.btnAddFile.clicked.connect(
            self.add_file
        )

        self.btnAddFolder.clicked.connect(
            self.add_folder
        )

        self.btnRename.clicked.connect(
            self.rename_node
        )

        self.btnDelete.clicked.connect(
            self.delete_node
        )

        # ===== View =====

        self.btnAllinfo.clicked.connect(
            self.show_info
        )

        self.btnSearchbysize.clicked.connect(
            self.search_by_size
        )

        # ===== Help =====

        self.btnContact.clicked.connect(
            self.show_contact
        )

        # ===== Tree View =====

        self.treeView.clicked.connect(
            self.tree_item_clicked
        )

        self.treeView.doubleClicked.connect(
            self.tree_item_double_clicked
        )

        # ===== Table View =====

        self.tableView.clicked.connect(
            self.table_item_clicked
        )

        self.tableView.doubleClicked.connect(
            self.table_item_double_clicked
        )



    # ==================================================
    # REFRESH GIAO DIỆN
    # ==================================================
    def load_data(self):
        try:

            self.load_file()
            self.refresh_all()

        except Exception as e:

            import traceback
            traceback.print_exc()

            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi 2",
                str(e)
            )

    def refresh_all(self):

        self.refresh_table_view()
        self.refresh_tree_view()
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

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Thư mục"])

        def add_folder(parent_item, folder_node):

            item = QStandardItem("📁 " + folder_node.name)

            # Lưu Node thật để xử lý khi click
            item.setData(folder_node)

            parent_item.appendRow(item)

            current = folder_node.children.head

            while current:

                if current.is_folder:
                    add_folder(item, current)

                current = current.next

        root_item = model.invisibleRootItem()

        add_folder(
            root_item,
            self.fs.root  # đổi thành tên biến FileSystemTree của bạn nếu khác
        )

        self.treeView.setModel(model)

        self.treeView.expandAll()

    def refresh_table_view(self):

        model = QStandardItemModel()

        model.setHorizontalHeaderLabels(
            [
                "Tên file",
                "Loại",
                "Kích thước",
                "Thời gian tạo"
            ]
        )

        current = (
            self.fs.current_working_dir.children.head
        )

        while current:

            row = [

                QStandardItem(
                    current.name
                ),

                QStandardItem(
                    "Folder"
                    if current.is_folder
                    else "File"
                ),

                QStandardItem(
                    str(current.size)
                ),

                QStandardItem(
                    current.created_at.strftime("%d/%m/%Y %H:%M:%S")
            )

            ]

            model.appendRow(row)

            current = current.next

        self.tableView.setModel(model)
   
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

    def search_nodes(self):
        """
        Khi cboFilter thay đổi.

        Gọi:

            self.search_by_name()
            self.search_by_filter()

        tùy lựa chọn.
        """
        
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

    def tree_item_clicked(self, index):
        """
        Khi click TreeView.

        Lấy node tương ứng.

        Đổi current_working_dir.

        Refresh TableView.
        """

    def tree_item_double_clicked(self, index):
        """
        Khi double click TreeView.

        Lấy node tương ứng.

        Nếu là folder:

            change_directory()

        Nếu là file:

            không làm gì
            hoặc hiện thông tin.
        """

    # ==================================================
    # TABLEVIEW
    # ==================================================

    def table_item_clicked(self, index):
        """
        Khi click TableView.

        Lấy node tương ứng.

        Đổi current_working_dir.

        Refresh TableView.
        """

    def table_item_double_clicked(self, index):
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

    def save_file(self):
        try:
            self.fs.save_to_json()

            QtWidgets.QMessageBox.information(
                self,
                "Thông báo",
                "Lưu dữ liệu thành công!"
            )

        except Exception as loi:

            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi",
                str(loi)
            )

    def load_file(self):
        try:

            self.fs.load_from_json()

        except Exception as e:

            print("=== LOAD JSON ERROR ===")
            print(type(e).__name__)
            print(e)

            QtWidgets.QMessageBox.critical(
                self,
                "Lỗi",
                str(e)
            )



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