from datetime import datetime
import json
import os
from sys import path, prefix

from numpy import size

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
class LinkedList:
    def __init__(self):
        self.head = None  

    def append(self, new_node):
        """Thêm một node mới vào cuối danh sách liên kết"""
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node
        new_node.next = None

    def remove(self, target_node):
        """Xóa một node ra khỏi danh sách liên kết và nối lại con trỏ"""
        if self.head is None:
            return
        if self.head == target_node:
            self.head = self.head.next
            target_node.next = None
            return
        
        pre = None
        curr = self.head
        while curr is not None:
            if curr == target_node:
                pre.next = curr.next
                target_node.next = None
                return
            pre = curr
            curr = curr.next

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
        self.next = None  
        if is_folder:
            self.children = LinkedList()
        else:
            self.children = None

# ==============================================================================
# KHUNG CHƯƠNG TRÌNH FILE SYSTEM TREE CỦA CẢ NHÓM
# ==============================================================================
class FileSystemTree:
    def __init__(self):
        self.root = Node("C:/", True)
        self.current_working_dir = self.root
        self.json_path = os.path.join(os.path.dirname(__file__),"data.json")


    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # các hàm chinhs
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # thực chất là thêm file và folder!
    def mkdir(self, name, is_folder=True, size=0):

        if is_folder:
            return self.add_folder(name)

        return self.create_file(name, size)
    
    def rename_node(self, old_name, new_name):

        if self._find_child_by_name(
            self.current_working_dir,
            new_name
        ) is not None:

            raise DuplicateNameError(
                f"Tên '{new_name}' đã tồn tại."
            )

        node = self._find_child_by_name(
            self.current_working_dir,
            old_name
        )

        if node is None:

            raise InvalidPathError(
                f"Không tìm thấy '{old_name}'."
            )

        node.name = new_name

        return node
    # thực chất là delete node nhé mn!
    def rm_rf(self, name):
        del_node = self._find_child_by_name(self.current_working_dir, name)

        if del_node is None:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{name}' cần xóa!")
        if del_node.is_folder:
            self._deep_delete(del_node)

        self.current_working_dir.children.remove(del_node)
        del_node.parent = None
        print(f"Đã xóa hoàn toàn thư mục '{name}' và dữ liệu bên trong.")

    def ls(self):
        result = []

        current = self.current_working_dir.children.head

        while current:
            result.append(current)
            current = current.next

        return result

    def tree(self, node=None, prefix="", is_last=True):

        if node is None:
            node = self.root

        ket_qua = ""

        if node == self.root:
            ket_qua += node.name + "\n"
        else:
            nhanh = "L-- " if is_last else "|-- "
            ket_qua += prefix + nhanh + node.name + "\n"

        if node.is_folder and node.children:

            children = []

            current = node.children.head

            while current:
                children.append(current)
                current = current.next

            for i, child in enumerate(children):

                child_is_last = (i == len(children) - 1)

                if node == self.root:
                    child_prefix = ""
                else:
                    child_prefix = prefix + ("    " if is_last else "|   ")

                ket_qua += self.tree(
                    child,
                    child_prefix,
                    child_is_last
                )

        return ket_qua

    def tree_ui(self, node=None, level=0, result=None):

        if result is None:
            result = []

        node = node or self.root

        result.append((node, level))

        if node.is_folder:

            current = node.children.head

            while current:

                self.tree_ui(
                    current,
                    level + 1,
                    result
                )

                current = current.next

        return result

    def _dfs(self, node, condition, results):  
        if condition(node):
            results.append(node)

        if node.is_folder and node.children:
            current = node.children.head
            while current:
                self._dfs(current, condition, results)
                current = current.next

    def search_by_name(self, name):
        results = []
        self._dfs(self.root, lambda n: n.name == name, results)
        return results

    def get_size(self, folder=None):
        node = folder or self.current_working_dir
    
        if not node.is_folder:
            return node.size
    
        tong = 0
        node_con = node.children.head
    
        while node_con:
            tong += self.get_size(node_con)
            node_con = node_con.next
    
        return tong

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #các hàm phụ
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    # ==================================================
    # NGƯỜI 1 - QUẢN LÝ THƯ MỤC 
    # ==================================================
    def add_folder(self, name):
        if self._find_child_by_name(self.current_working_dir, name) is not None:
            raise DuplicateNameError(f"Lỗi: Tên thư mục '{name}' đã tồn tại!")
        
        new_folder = Node(name=name, is_folder=True, size=0, parent=self.current_working_dir)

        self.current_working_dir.children.append(new_folder)
        print(f"Đã tạo thư mục: {name}")
        return new_folder
    
    def rename_folder(self, old_name, new_name):
        target_node = self._find_child_by_name(self.current_working_dir, old_name)
        if target_node is None or not target_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{old_name}'!")
        if old_name != new_name and self._find_child_by_name(self.current_working_dir, new_name) is not None:
            raise DuplicateNameError(f"Lỗi: Tên mới '{new_name}' đã tồn tại!")
        target_node.name = new_name
        print(f"Đã đổi tên thư mục '{old_name}' thành '{new_name}'")

    def _deep_delete(self, node):
        if node.children is not None:
            child = node.children.head

            while child is not None:
                next_node = child.next
                if child.is_folder:
                    self._deep_delete(child)
                child.parent = None
                child.children = None
                child.next = None
                child = next_node
            node.children.head = None 

    #-----------
    # PHẦN NGOÀI
    #-----------

    def _clone_tree(self, source_node, new_parent):
        cloned_node = Node(name=source_node.name, is_folder=source_node.is_folder, size=source_node.size, parent=new_parent)
        if source_node.is_folder and source_node.children is not None:
            child = source_node.children.head
            while child is not None:
                cloned_child = self._clone_tree(child, cloned_node)
                cloned_node.children.append(cloned_child)
                child = child.next
        return cloned_node
    
    def copy_folder(self, source_name, destination_name):
        src_node = self._find_child_by_name(self.current_working_dir, source_name)
        dest_node = self._find_child_by_name(self.current_working_dir, destination_name)
        if src_node is None or not src_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục nguồn '{source_name}'!")
        if dest_node is None or not dest_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục đích '{destination_name}'!")
        if self._find_child_by_name(dest_node, source_name) is not None:
            raise DuplicateNameError(f"Lỗi: Thư mục đích đã có phần tử tên '{source_name}'!")
        cloned_folder = self._clone_tree(src_node, dest_node)
        dest_node.children.append(cloned_folder)
        print(f"Đã sao chép thư mục '{source_name}' vào '{destination_name}' thành công.")

    def move_folder(self, source_name, destination_name):
        src_node = self._find_child_by_name(self.current_working_dir, source_name)
        dest_node = self._find_child_by_name(self.current_working_dir, destination_name)
        if src_node is None or not src_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục nguồn '{source_name}'!")
        if dest_node is None or not dest_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục đích '{destination_name}'!")
        if self._find_child_by_name(dest_node, source_name) is not None:
            raise DuplicateNameError(f"Lỗi: Thư mục đích đã có phần tử tên '{source_name}'!")
        self.current_working_dir.children.remove(src_node)
        src_node.parent = dest_node
        dest_node.children.append(src_node)
        print(f"Đã di chuyển thư mục '{source_name}' vào '{destination_name}' thành công.")

    # ==================================================
    # NGƯỜI 2 - QUẢN LÝ FILE (File Manager)
    # ==================================================


    def create_file(self, name, size):
        if self._find_child_by_name(self.current_working_dir, name) is not None:
            raise DuplicateNameError(f"Lỗi: Tên file '{name}' đã tồn tại!")
    
        new_file = Node(name, False, size, self.current_working_dir)
        self.current_working_dir.children.append(new_file)
    
        return new_file
 
    def rename_file(self, old_name, new_name):
         current = self.current_working_dir.children.head
     
         # Kiểm tra tên mới có bị trùng không
         while current:
             if current.name == new_name:
                 raise DuplicateNameError(
                     f"Tên '{new_name}' đã tồn tại."
                 )
             current = current.next
     
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == old_name and not current.is_folder:
                 current.name = new_name
                 return current
             current = current.next
     
         raise InvalidPathError(f"Không tìm thấy file '{old_name}'.")
       

        # ==================================================
    
        # ==================================================
    
    #-----------
    # PHẦN NGOÀI
    #-----------
    def copy_file(self, source_name, destination_name):
         source = None
         current = self.current_working_dir.children.head
     
         while current:
             if current.name == source_name and not current.is_folder:
                 source = current
                 break
             current = current.next
     
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
             current = current.next
     
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
             current = current.next
     
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
             current = current.next
     
         file_node.name = destination_name
     
         return file_node
 
 
    # ==================================================
    # NGƯỜI 3 - TÌM KIẾM & SẮP XẾP
    # ==================================================

    def search_by_extension(self, extension):
        results = []
        self._dfs(self.root, lambda n: not n.is_folder and n.name.endswith(extension), results)
        return results

    def search_by_size(self, min_size, max_size):
        results = []
        self._dfs(self.root, lambda n: not n.is_folder and min_size <= n.size <= max_size, results)
        return results

    
    # có lẽ là không cần nhé!
    
    # def sort_by_name(self, folder=None):
    #     folder = folder or self.current_working_dir
    #     if not folder.is_folder:
    #         raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
    #     children = []
    #     current = folder.children.head
    #     while current:
    #         children.append(current)
    #         current = current.next
    #     children.sort(key=lambda n: n.name)
    #     folder.children.head = None
    #     for child in children:
    #         folder.children.append(child)

    # def sort_by_size(self, folder=None):
    #     folder = folder or self.current_working_dir
    #     if not folder.is_folder:
    #         raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
    #     children = []
    #     current = folder.children.head
    #     while current:
    #         children.append(current)
    #         current = current.next
    #     children.sort(key=lambda n: n.size)
    #     folder.children.head = None
    #     for child in children:
    #         folder.children.append(child)

    # def sort_by_created_date(self, folder=None):
        folder = folder or self.current_working_dir
        if not folder.is_folder:
            raise ValueError("Chỉ có thể sắp xếp trong thư mục.")
        children = []
        current = folder.children.head
        while current:
            children.append(current)
            current = current.next
        children.sort(key=lambda n: n.created_at)
        folder.children.head = None
        for child in children:
            folder.children.append(child)

    # ==================================================
    # NGƯỜI 4 - THỐNG KÊ & HIỂN THỊ CÂY
    # ==================================================
 
    def count_files(self, folder=None):
        node = folder or self.current_working_dir
    
        if not node.is_folder:
            return 1
    
        so_file = 0
        node_con = node.children.head
    
        while node_con:
            so_file += self.count_files(node_con)
            node_con = node_con.next
    
        return so_file 
    
    def get_path(self, node):
        path = []
    
        while node:
            path.append(node.name)
            node = node.parent
    
        path.reverse()
    
        if len(path) == 1:
            return "C:/"
    
        return "C:/" + "/".join(path[1:])



    # ==================================================
    # NGƯỜI 5 - SAVE/LOAD + UNDO/REDO + EXCEPTION
    # ==================================================

    def save_to_json(self):

        data = self.node_to_dict(
            self.root
        )

        with open(self.json_path, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )


    def load_from_json(self):

        with open(
            self.json_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        self.root = self.dict_to_node(
            data
        )

        self.current_working_dir = (
            self.root
        )


    # ==================================================
    # HÀM DÙNG CHUNG (KHÔNG AI SỞ HỮU)
    # ==================================================
    def _find_child_by_name(self, parent_node, name):
        """Tìm kiếm một node con trực tiếp bằng cách duyệt danh sách liên kết"""
        if parent_node.children is None or parent_node.children.head is None:
            return None
        current = parent_node.children.head
        while current is not None:
            if current.name == name:
                return current
            current = current.next
        return None
    
    def change_directory(self, node):
        self.current_working_dir = node

    def go_back(self):
        if self.current_working_dir.parent:

            self.current_working_dir = (
                self.current_working_dir.parent
            )

    def find_node_by_path(self, path):

        if path == "C:/":
            return self.root

        path_parts = path.removeprefix("C:/").split("/")

        current_node = self.root

        for part in path_parts:
            found_node = None
            child_node = current_node.children.head
            while child_node:
                if child_node.name == part:
                    found_node = child_node
                    break

                child_node = child_node.next

            if found_node is None:
                raise InvalidPathError(
                    f"Invalid path: {path}"
                )
            current_node = found_node
        return current_node
    
    def node_to_dict(self, node):

        data = {
            "name": node.name,
            "is_folder": node.is_folder,
            "size": node.size,
            "created_at": node.created_at.isoformat()
        }

        if node.is_folder:

            data["children"] = []

            child = node.children.head

            while child:

                data["children"].append(
                    self.node_to_dict(child)
                )

                child = child.next

        return data
    
    def dict_to_node(self, data, parent=None):

        new_node = Node(
            data["name"],
            data["is_folder"],
            data["size"],
            parent
        )

        if "created_at" in data:

            new_node.created_at = (
                datetime.fromisoformat(
                    data["created_at"]
                )
            )

        if new_node.is_folder:

            for child_data in data.get(
                "children",
                []
            ):

                child_node = self.dict_to_node(
                    child_data,
                    new_node
                )

                new_node.children.append(
                    child_node
                )

        return new_node