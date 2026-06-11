
def _find_child_by_name(self, parent_node, name):
    if parent_node.children is None or parent_node.children.head is None:
        return None
    current = parent_node.children.head
    while current is not None:
        if current.name == name:
            return current
        current = current.next_sibling
    return None

def add_folder(self, name):
    if self._find_child_by_name(self.current_working_dir, name) is not None:
        raise DuplicateNameError(f"Lỗi: Tên thư mục '{name}' đã tồn tại!")
    new_folder = Node(name=name, is_folder=True, size=0, parent=self.current_working_dir)
    self.current_working_dir.children.append(new_folder)
    print(f"Đã tạo thư mục: {name}")
    return new_folder

def rename_folder(self, old_name, new_name):
    """2. ĐỔI TÊN THƯ MỤC"""
    target_node = self._find_child_by_name(self.current_working_dir, old_name)
    if target_node is None or not target_node.is_folder:
        raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{old_name}'!")
    if old_name != new_name and self._find_child_by_name(self.current_working_dir, new_name) is not None:
        raise DuplicateNameError(f"Lỗi: Tên mới '{new_name}' đã tồn tại!")
    target_node.name = new_name
    print(f"Đã đổi tên thư mục '{old_name}' thành '{new_name}'")

def delete_folder(self, folder_name):
    target_node = self._find_child_by_name(self.current_working_dir, folder_name)
    if target_node is None or not target_node.is_folder:
        raise InvalidPathError(f"Lỗi: Không tìm thấy thư mục '{folder_name}' cần xóa!")
    self._deep_delete(target_node)
    self.current_working_dir.children.remove(target_node)
    target_node.parent = None
    print(f"Đã xóa hoàn toàn thư mục '{folder_name}' và dữ liệu bên trong.")

def _deep_delete(self, node):
    if node.children is not None:
        current_child = node.children.head
        while current_child is not None:
            next_sib = current_child.next_sibling
            if current_child.is_folder:
                self._deep_delete(current_child)
            current_child.parent = None
            current_child.children = None
            current_child.next_sibling = None
            current_child = next_sib
        node.children.head = None

def _clone_tree(self, source_node, new_parent):
    cloned_node = Node(name=source_node.name, is_folder=source_node.is_folder, size=source_node.size, parent=new_parent)
    if source_node.is_folder and source_node.children is not None:
        current_child = source_node.children.head
        while current_child is not None:
            cloned_child = self._clone_tree(current_child, cloned_node)
            cloned_node.children.append(cloned_child)
            current_child = current_child.next_sibling
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
