from datetime import datetime
import json

# ==============================================================================
# NGOẠI LỆ DÙNG CHUNG CHO HỆ THỐNG
# ==============================================================================
class DuplicateNameError(Exception):
    pass

class InvalidPathError(Exception):
    pass

# ==============================================================================
# CLASS LINKED LIST - TỰ CÀI ĐẶT ĐỂ QUẢN LÝ CÁC NODE CON
# ==============================================================================
class FolderLinkedList:
    def __init__(self):
        self.head = None  

    def append(self, new_node):
        """Thêm một node mới vào cuối danh sách liên kết"""
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next_sibling is not None:
                current = current.next_sibling
            current.next_sibling = new_node
        new_node.next_sibling = None

    def remove(self, target_node):
        """Xóa một node ra khỏi danh sách liên kết và nối lại con trỏ"""
        if self.head is None:
            return
        if self.head == target_node:
            self.head = self.head.next_sibling
            target_node.next_sibling = None
            return
        prev = None
        current = self.head
        while current is not None:
            if current == target_node:
                prev.next_sibling = current.next_sibling
                target_node.next_sibling = None
                return
            prev = current
            current = current.next_sibling

# ==============================================================================
# CLASS NODE CHUNG - Đã chuyển từ mảng [] sang FolderLinkedList()
# ==============================================================================
class Node:
    def __init__(self, name, is_folder, size=0, parent=None):
        self.name = name
        self.is_folder = is_folder
        self.size = size
        self.parent = parent
        self.created_at = datetime.now()
        self.next_sibling = None  
        if is_folder:
            self.children = FolderLinkedList()
        else:
            self.children = None

# ==============================================================================
# KHUNG CHƯƠNG TRÌNH FILE SYSTEM TREE CỦA CẢ NHÓM
# ==============================================================================
class FileSystemTree:
    def __init__(self):
        self.root = Node("/", True)
        self.current_working_dir = self.root
        self.logs = []

    # ==================================================
    # NGƯỜI 1 - QUẢN LÝ THƯ MỤC (Folder Manager)
    # ==================================================
    def add_folder(self, name):
        pass

    def rename_folder(self, old_name, new_name):
        pass

    def delete_folder(self, folder_name):
        pass

    def copy_folder(self, source_name, destination_name):
        pass

    def move_folder(self, source_name, destination_name):
        pass

    # ==================================================
    # NGƯỜI 2 - QUẢN LÝ FILE (File Manager)
    # ==================================================
    def create_file(self, name, size):
        pass

    def delete_file(self, name):
        pass

    def rename_file(self, old_name, new_name):
        pass

    def copy_file(self, source_name, destination_name):
        pass

    def move_file(self, source_name, destination_name):
        pass
    # ==================================================
    # NGƯỜI 3 - TÌM KIẾM & SẮP XẾP
    # ==================================================

    def search_by_name(self, name):
        pass

    def search_by_extension(self, extension):
        pass

    def search_by_size(self, min_size, max_size):
        pass

    def sort_by_name(self):
        pass

    def sort_by_size(self):
        pass

    def sort_by_created_date(self):
        pass

    # ==================================================
    # NGƯỜI 4 - THỐNG KÊ & HIỂN THỊ CÂY
    # ==================================================

    def get_size(self, folder=None):
        pass

    def count_files(self, folder=None):
        pass

    def count_folders(self, folder=None):
        pass

    def tree(self, folder=None, level=0):
        pass

    def get_full_path(self, node):
        pass

    # ==================================================
    # NGƯỜI 5 - SAVE/LOAD + UNDO/REDO + EXCEPTION
    # ==================================================


    def save_to_json(self, file_path):

        du_lieu = self.node_to_dict(
            self.root
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as tep:

            json.dump(
                du_lieu,
                tep,
                indent=4,
                ensure_ascii=False
            )

        self.log_action(
            f"Saved to {file_path}"
        )

    # ==================================================
    # LOAD JSON
    # ==================================================

    def load_from_json(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as tep:

            du_lieu = json.load(tep)

        self.root = self.dict_to_node(
            du_lieu
        )

        self.current_working_dir = (
            self.root
        )

        self.log_action(
            f"Loaded from {file_path}"
        )



    def log_action(self, action):
        thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.logs.append( f"[{thoi_gian}] {action}")

    # ==================================================
    # HÀM DÙNG CHUNG (KHÔNG AI SỞ HỮU)
    # ==================================================

    def change_directory(self, folder_name):
        if folder_name == "/":
            self.current_working_dir = self.root
            return
        
        node_con = (self.current_working_dir.children.head)
        while node_con:
            if (node_con.name == folder_name and node_con.is_folder ):
                self.current_working_dir = node_con
                return

            node_con = node_con.next_sibling

        raise InvalidPathError(f"Folder '{folder_name}' not found.")

    def go_back(self):
        if self.current_working_dir.parent:

            self.current_working_dir = (
                self.current_working_dir.parent
            )

    def get_current_directory(self):
        return self.current_working_dir

    def find_node_by_path(self, path):
        if path == "/":
            return self.root

        danh_sach_ten = (  path.strip("/").split("/"))

        node_hien_tai = self.root

        for ten in danh_sach_ten:
            node_tim_duoc = None
            node_con = (node_hien_tai.children.head)

            while node_con:
                if node_con.name == ten:
                    node_tim_duoc = node_con
                    break

                node_con = ( node_con.next_sibling )

            if node_tim_duoc is None:

                raise InvalidPathError(
                    f"Invalid path: {path}"
                )

            node_hien_tai = node_tim_duoc

        return node_hien_tai
    
    def node_to_dict(self, node):

        du_lieu = {
            "name": node.name,
            "is_folder": node.is_folder,
            "size": node.size
        }

        if node.is_folder:

            du_lieu["children"] = []

            node_con = node.children.head

            while node_con:

                du_lieu["children"].append(
                    self.node_to_dict(node_con)
                )

                node_con = node_con.next_sibling

        return du_lieu

    # ==================================================
    # HÀM HỖ TRỢ CHUYỂN DICTIONARY -> NODE
    # ==================================================

    def dict_to_node(self, du_lieu, node_cha=None):

        node_moi = Node(
            du_lieu["name"],
            du_lieu["is_folder"],
            du_lieu["size"],
            node_cha
        )

        if node_moi.is_folder:

            for du_lieu_con in du_lieu.get(
                "children",
                []
            ):

                node_con = self.dict_to_node(
                    du_lieu_con,
                    node_moi
                )

                node_moi.children.append(
                    node_con
                )

        return node_moi

