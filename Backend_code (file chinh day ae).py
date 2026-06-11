from datetime import datetime

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
        pass

    def load_from_json(self, file_path):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def log_action(self, action):
        pass

    # ==================================================
    # HÀM DÙNG CHUNG (KHÔNG AI SỞ HỮU)
    # ==================================================

    def change_directory(self, folder_name):
        pass

    def go_back(self):
        pass

    def get_current_directory(self):
        pass

    def find_node_by_path(self, path):
        pass
