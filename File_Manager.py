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
