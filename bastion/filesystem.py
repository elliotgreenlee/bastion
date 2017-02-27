import os
from datetime import datetime


class FileSystemAllocation:
    """Was originally planning on using this to track "allocations" in memory,
    meaning files that span several blocks."""
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size


class FileSystem:
    CONST_FILE_SYSTEM_NAME = "file_system.bastion"
    BLOCK_SIZE = 4096

    def __init__(self):
        self.exists = self.on_disk()
        self.fd = 0
        self.available_fds = []
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child(Child('..', self.root.parent))

        self.free_list = [FileSystemAllocation(0, 104857600)]  # 100 MB

    def initialize(self):
        """If the filesystem does not exist yet or we are
        overwriting the existing filesystem, run this function."""

        if self.on_disk():
            os.remove(self.CONST_FILE_SYSTEM_NAME)

        open(self.CONST_FILE_SYSTEM_NAME, 'a')

        # Overwrite old values
        self.exists = False
        self.fd = 0
        self.available_fds = []
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child(Child('..', self.root.parent))

        self.free_list = [FileSystemAllocation(0, 104857600)]  # 100 MB

    def on_disk(self):
        if os.path.isfile(self.CONST_FILE_SYSTEM_NAME):
            return True
        else:
            return False

    def get_new_fd(self):
        if len(self.available_fds) == 0:
            current_fd = self.fd
            self.fd += 1
        else:
            current_fd = self.available_fds[0]
            self.available_fds.remove(self.available_fds[0])
        return current_fd

    def find_open_fd(self, fd):
        for open_file in self.open_files:
            if str(fd) == str(open_file.fd):
                return open_file

    def find_open_name(self, name):
        for open_file in self.open_files:
            if name == open_file.file.name:
                return open_file

    def add_open_file(self, open_file):
        self.open_files.append(open_file)

    def get_free_space(self, size):
        """
            Return offset where space starts, return None otherwise
        """

        # find size that works in free_list
        chosen_space = None
        for free_space in self.free_list:
            if free_space.size >= size:
                chosen_space = free_space
                break

        # if no size works, return -1
        if chosen_space is None:
            return -1

        chosen_offset = chosen_space.offset
        chosen_size = chosen_space.size

        # remove free_space from the free_list
        self.free_list.remove(chosen_space)

        # append the non needed part of the piece back to free_list
        self.free_list.append(FileSystemAllocation(chosen_offset + size, chosen_size - size))

        # return the required piece
        return chosen_offset

    def load_from_disk(self, offset, size):
        # load file at offset of length size into temporary string content
        with open(self.CONST_FILE_SYSTEM_NAME, 'r+') as f:
            f.seek(offset)
            content = f.read(size)
            f.close()

        return content

    def write_to_disk(self, offset, content):
        """
            Write content (bytes) to offset, return None if not possible.
        """

        # put content at offset
        with open(self.CONST_FILE_SYSTEM_NAME, 'r+') as f:
            f.seek(offset)
            f.write(content)
            f.close()

    def free_space(self, offset, size):
        """
            Go to offset and delete up to size
        """

        # append (offset, size) to the free_list
        self.free_list.append(FileSystemAllocation(offset, size))
        combine = True
        while combine:
            combine = False
            self.free_list.sort(key=lambda x: x.offset)
            # Iterate through each free_space in free_list
            for i in range(1, len(self.free_list)):
                free_space = self.free_list[i-1]
                next_free_space = self.free_list[i]

                if free_space.offset + free_space.size == next_free_space.offset:
                    free_space.size += next_free_space.size
                    # remove next_free_space from free_list
                    self.free_list.remove(next_free_space)
                    combine = True
                    # break out of inner loop
                    break


class OpenFile:
    def __init__(self, fd, mode, file):
        self.fd = fd
        self.mode = mode
        self.file = file


class Directory:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.children = []
        self.add_child(Child('..', parent))

    def add_child(self, child):
        self.children.append(child)

    def find_child(self, name):
        for child in self.children:
            if name == child.name:
                return child


class Child:
    def __init__(self, name, child):
        self.name = name
        self.child = child


class File:
    def __init__(self, parent, name, fd, offset):
        self.name = name
        self.parent = parent
        self.fd = fd
        self.content_size = 0
        self.offset = 0
        self.date = str(datetime.now())

        self.fsa = FileSystemAllocation(offset, 4096)
