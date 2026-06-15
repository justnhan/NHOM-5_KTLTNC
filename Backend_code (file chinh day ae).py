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
        current = self.current_working_dir.children.head
    
        while current:
            if current.name == name:
                raise DuplicateNameError(f"File '{name}' đã tồn tại.")
            current = current.next_sibling
    
        new_file = Node(name, False, size, self.current_working_dir)
        self.current_working_dir.children.append(new_file)
    
        return new_file
    
    
     def delete_file(self, name):
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == name and not current.is_folder:
                 self.current_working_dir.children.remove(current)
                 return True
             current = current.next_sibling
     
         raise InvalidPathError(f"Không tìm thấy file '{name}'.")
     
     
     def rename_file(self, old_name, new_name):
         current = self.current_working_dir.children.head
     
         # Kiểm tra tên mới có bị trùng không
         while current:
             if current.name == new_name:
                 raise DuplicateNameError(
                     f"Tên '{new_name}' đã tồn tại."
                 )
             current = current.next_sibling
     
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == old_name and not current.is_folder:
                 current.name = new_name
                 return current
             current = current.next_sibling
     
         raise InvalidPathError(f"Không tìm thấy file '{old_name}'.")
     
     
     def copy_file(self, source_name, destination_name):
         source = None
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == source_name and not current.is_folder:
                 source = current
                 break
             current = current.next_sibling
     
         if source is None:
             raise InvalidPathError(
                 f"Không tìm thấy file '{source_name}'."
             )
     
         current = self.current_working_dir.children.head
         while current:
             if current.name == destination_name:
                 raise DuplicateNameError(
                     f"Tên '{destination_name}' đã tồn tại."
                 )
             current = current.next_sibling
     
         copied_file = Node(
             destination_name,
             False,
             source.size,
             self.current_working_dir
         )
     
         self.current_working_dir.children.append(copied_file)
     
         return copied_file
     
     
     def move_file(self, source_name, destination_name):
         file_node = None
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == source_name and not current.is_folder:
                 file_node = current
                 break
             current = current.next_sibling
     
         if file_node is None:
             raise InvalidPathError(
                 f"Không tìm thấy file '{source_name}'."
             )
     
         current = self.current_working_dir.children.head
         while current:
             if current.name == destination_name:
                 raise DuplicateNameError(
                     f"Tên '{destination_name}' đã tồn tại."
                 )
             current = current.next_sibling
     
         file_node.name = destination_name
     
         return file_node
    # ==================================================
    # NGƯỜI 3 - TÌM KIẾM & SẮP XẾP
    # ==================================================

    def _dfs(self, node, condition, results):
        if condition(node):
            results.append(node)
        if node.is_folder and node.children:
            current = node.children.head
            while current:
                self._dfs(current, condition, results)
                current = current.next_sibling

    def search_by_name(self, name):
        results = []
        self._dfs(self.root, lambda n: n.name == name, results)
        return results

    def search_by_extension(self, extension):
        results = []
        self._dfs(self.root, lambda n: not n.is_folder and n.name.endswith(extension), results)
        return results

    def search_by_size(self, min_size, max_size):
        results = []
        self._dfs(self.root, lambda n: not n.is_folder and min_size <= n.size <= max_size, results)
        return results

    
    
    def sort_by_name(self, folder=None):
        folder = folder or self.current_working_dir
        if not folder.is_folder:
            raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
        children = []
        current = folder.children.head
        while current:
            children.append(current)
            current = current.next_sibling
        children.sort(key=lambda n: n.name)
        folder.children.head = None
        for child in children:
            folder.children.append(child)

    def sort_by_size(self, folder=None):
        folder = folder or self.current_working_dir
        if not folder.is_folder:
            raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
        children = []
        current = folder.children.head
        while current:
            children.append(current)
            current = current.next_sibling
        children.sort(key=lambda n: n.size)
        folder.children.head = None
        for child in children:
            folder.children.append(child)

    def sort_by_created_date(self, folder=None):
        folder = folder or self.current_working_dir
        if not folder.is_folder:
            raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
        children = []
        current = folder.children.head
        while current:
            children.append(current)
            current = current.next_sibling
        children.sort(key=lambda n: n.created_at)
        folder.children.head = None
        for child in children:
            folder.children.append(child)

    # ==================================================
    # NGƯỜI 4 - THỐNG KÊ & HIỂN THỊ CÂY
    # ==================================================
    
    def get_size(self, folder=None):
        folder = folder or self.current_working_dir
    
        if not folder.is_folder:
            return folder.size
    
        tong = 0
        node_con = folder.children.head
    
        while node_con:
            tong += self.get_size(node_con)
            node_con = node_con.next_sibling
    
        return tong
    
    
    def count_files(self, folder=None):
        folder = folder or self.current_working_dir
    
        if not folder.is_folder:
            return 1
    
        dem = 0
        node_con = folder.children.head
    
        while node_con:
            dem += self.count_files(node_con)
            node_con = node_con.next_sibling
    
        return dem
    
    
    def count_folders(self, folder=None):
        folder = folder or self.current_working_dir
    
        if not folder.is_folder:
            return 0
    
        dem = 1
    
        node_con = folder.children.head
    
        while node_con:
            if node_con.is_folder:
                dem += self.count_folders(node_con)
    
            node_con = node_con.next_sibling
    
        return dem
    
    
    def tree(self, folder=None, level=0):
        folder = folder or self.current_working_dir
    
        ket_qua = "    " * level + folder.name + "\n"
    
        if folder.is_folder:
            node_con = folder.children.head
    
            while node_con:
                ket_qua += self.tree(node_con, level + 1)
                node_con = node_con.next_sibling
    
        return ket_qua
    
    
    def get_full_path(self, node):
        duong_dan = []
    
        while node:
            duong_dan.append(node.name)
            node = node.parent
    
        duong_dan.reverse()
    
        if len(duong_dan) == 1:
            return "/"
    
        return "/" + "/".join(duong_dan[1:])

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

