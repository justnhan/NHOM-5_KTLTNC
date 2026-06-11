
class Node:
    def __init__(self, name, is_folder=True, size=0):
        self.name = name              
        self.is_folder = is_folder    
        self.size = size             
        self.parent = None            
        self.children_head = None     
        self.next_sibling = None     

class DuplicateNameError(Exception):
    pass
class InvalidPathError(Exception):
    pass
class FolderManager:
    @staticmethod
    def _find_child_by_name(parent_node, name):
        current = parent_node.children_head
        while current is not None:
            if current.name == name:
                return current
            current = current.next_sibling
        return None
    
    @staticmethod
    def mkdir(current_node, name):
        if FolderManager._find_child_by_name(current_node, name) is not None:
            raise DuplicateNameError(f"Lỗi: Tên '{name}' đã tồn tại trong thư mục này!")
        new_folder = Node(name, is_folder=True, size=0)
        new_folder.parent = current_node  
        if current_node.children_head is None:
            current_node.children_head = new_folder
        else:
            new_folder.next_sibling = current_node.children_head
            current_node.children_head = new_folder
        
        print(f"Đã tạo thư mục: {name}")
        return new_folder

    @staticmethod
    def rename_folder(current_node, old_name, new_name):
        target_node = FolderManager._find_child_by_name(current_node, old_name)
        if target_node is None or not target_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{old_name}'!")
        if old_name != new_name and FolderManager._find_child_by_name(current_node, new_name) is not None:
            raise DuplicateNameError(f"Lỗi: Tên mới '{new_name}' đã tồn tại!")
        target_node.name = new_name
        print(f"Đã đổi tên thư mục '{old_name}' thành '{new_name}'")

    @staticmethod
    def delete_folder(current_node, name):
        target_node = FolderManager._find_child_by_name(current_node, name)
        if target_node is None or not target_node.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{name}' cần xóa!")
        FolderManager._deep_delete(target_node)
        prev = None
        curr = current_node.children_head
        while curr is not None:
            if curr == target_node:
                if prev is None:
                    current_node.children_head = curr.next_sibling
                else:
                    prev.next_sibling = curr.next_sibling
                break
            prev = curr
            curr = curr.next_sibling
        target_node.parent = None
        target_node.next_sibling = None
        print(f"Đã xóa hoàn toàn thư mục '{name}' và các dữ liệu bên trong.")

    @staticmethod
    def _deep_delete(node):
        current_child = node.children_head
        while current_child is not None:
            next_sibling = current_child.next_sibling
            if current_child.is_folder:
                FolderManager._deep_delete(current_child)
            current_child.parent = None
            current_child.children_head = None
            current_child.next_sibling = None
            current_child = next_sibling
        node.children_head = None

    @staticmethod
    def _clone_tree(source_node):
        new_node = Node(source_node.name, source_node.is_folder, source_node.size)
        curr_child = source_node.children_head
        last_added_child = None
        while curr_child is not None:
            cloned_child = FolderManager._clone_tree(curr_child)
            cloned_child.parent = new_node 
            if new_node.children_head is None:
                new_node.children_head = cloned_child
            else:
                last_added_child.next_sibling = cloned_child
            last_added_child = cloned_child
            curr_child = curr_child.next_sibling
        return new_node

    @staticmethod
    def copy_folder(current_node, src_name, dest_node):
        src_folder = FolderManager._find_child_by_name(current_node, src_name)
        if src_folder is None or not src_folder.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục nguồn '{src_name}'!")
        if FolderManager._find_child_by_name(dest_node, src_name) is not None:
            raise DuplicateNameError(f"Lỗi: Thư mục đích đã có cấu trúc trùng tên '{src_name}'!")
        cloned_folder = FolderManager._clone_tree(src_folder)
        cloned_folder.parent = dest_node 
        if dest_node.children_head is None:
            dest_node.children_head = cloned_folder
        else:
            cloned_folder.next_sibling = dest_node.children_head
            dest_node.children_head = cloned_folder
        print(f"Đã sao chép thư mục '{src_name}' thành công.")

    @staticmethod
    def move_folder(current_node, src_name, dest_node):
        src_folder = FolderManager._find_child_by_name(current_node, src_name)
        if src_folder is None or not src_folder.is_folder:
            raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{src_name}'!")
        if FolderManager._find_child_by_name(dest_node, src_name) is not None:
            raise DuplicateNameError(f"Lỗi: Thư mục đích đã có cấu trúc trùng tên '{src_name}'!")
        prev = None
        curr = current_node.children_head
        while curr is not None:
            if curr == src_folder:
                if prev is None:
                    current_node.children_head = curr.next_sibling
                else:
                    prev.next_sibling = curr.next_sibling
                break
            prev = curr
            curr = curr.next_sibling
        src_folder.parent = dest_node
        src_folder.next_sibling = None
        if dest_node.children_head is None:
            dest_node.children_head = src_folder
        else:
            src_folder.next_sibling = dest_node.children_head
            dest_node.children_head = src_folder
        print(f"Đã di chuyển thư mục '{src_name}' thành công.")

#Chạy thử
if __name__ == "__main__":
    print("--- HỆ THỐNG MÔ PHỎNG QUẢN LÝ THƯ MỤC BẮT ĐẦU ---")
    root = Node(name="Root_Dir", is_folder=True)

    dir_docs = FolderManager.mkdir(root, "Documents")
    dir_pics = FolderManager.mkdir(root, "Pictures")

    dir_bt = FolderManager.mkdir(dir_docs, "Assignments")
    FolderManager.rename_folder(root, "Pictures", "Photos")
    
    print("\n--- Tiến hành di chuyển thư mục ---")
    FolderManager.move_folder(dir_docs, "Assignments", dir_pics)
    
    print("\n--- Tiến hành sao chép thư mục ---")
    FolderManager.copy_folder(dir_pics, "Assignments", dir_docs)
    
    print("\n--- Tiến hành xóa thư mục ---")
    FolderManager.delete_folder(dir_pics, "Assignments")
    
    print("\n--- Thử nghiệm kiểm tra bẫy lỗi trùng tên ---")
    ten_can_tao = "Documents"
    if FolderManager._find_child_by_name(root, ten_can_tao) is not None:
        print(f"Hệ thống thông báo: Tên '{ten_can_tao}' đã tồn tại rồi, không tạo nữa đâu!")
    else:
        FolderManager.mkdir(root, ten_can_tao)
    print("\n--- KẾT THÚC CHƯƠNG TRÌNH TEST ---")