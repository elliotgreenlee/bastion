import pickle
import os
import uuid
from datetime import datetime
from collections import defaultdict


class FileSystemAllocation:
    """Was originally planning on using this to track "allocations" in memory,
    meaning files that span several blocks."""
    def __init__(self):
        self.blocks = []
        self.total_size = 0


class FileSystemBlock:
    """Was originally planning on using this to track blocks, each 4096 byte
    section."""
    def __init__(self, block_num):
        self.block_num = block_num
        self.used = False


class FileSystem:
    CONST_FILE_SYSTEM_NAME = "file_system.bastion"
    TOTAL_BLOCKS = 250
    BLOCK_SIZE = 4096
    open_files = []

    def __init__(self):
        self.exists = self.on_disk()
        self.total_size = 20971520  # 20 megabytes allocated for overhead
        self.fd = 0
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child('..', self.root.parent)

        self.free_space = defaultdict()
        for i in range(0, 250):
            self.free_space[i] = FileSystemBlock(i)

    def initialize(self):
        """If the filesystem does not exist yet or we are
        overwriting the existing filesystem, run this function."""

        if self.on_disk():
            os.remove(self.CONST_FILE_SYSTEM_NAME)

        # Overwrite old values
        self.exists = False
        self.total_size = 20971520  # 20 megabytes allocated for overhead
        self.fd = 0
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child('..', self.root.parent)

    def on_disk(self):
        if os.path.isfile(self.CONST_FILE_SYSTEM_NAME):
            return True
        else:
            return False

    def get_new_fd(self):
        current_fd = self.fd
        self.fd += 1
        return current_fd

    def get_open_file(self, fd):
        for file in self.open_files:
            if str(fd) == str(file[0]):
                return file[2]

    def get_free_space(self, size):
        """
            Return offset where space starts, return None otherwise
        """

        current_byte_size = os.path.getsize(self.CONST_FILE_SYSTEM_NAME)

        if current_byte_size >= self.total_size:
            return None

        with open(self.CONST_FILE_SYSTEM_NAME, 'rwb') as f:
            f.seek(current_byte_size)

            current_byte_offset = f.tell()

            # Not enough space
            if self.total_size - current_byte_offset < size:
                return None

            return current_byte_offset

    def write_to_disk(self, offset, content):
        """
            Write content (bytes) to offset, return None if not possible.
        """

        current_byte_size = os.path.getsize(self.CONST_FILE_SYSTEM_NAME)

        # Filesystem is full
        if current_byte_size >= self.total_size:
            return None

        with open(self.CONST_FILE_SYSTEM_NAME, 'rwb') as f:
            f.seek(offset)

            if self.total_size - offset < len(content):
                return None

            f.write(content)

    def free_space(self, offset, size):
        """
            Go to offset and delete up to size
        """

        with open(self.CONST_FILE_SYSTEM_NAME, 'rwb') as f:
            f.seek(offset)

            # File is now at offset, must delete that content somehow


class Directory:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.children = []
        self.add_child('..', parent)

    def add_child(self, name, child):
        self.children.append((name, child))

    def find_child(self, name):
        for child in self.children:
            if name == child[0]:
                return child[1]


class File:
    def __init__(self, parent, name, fd):
        self.name = name
        self.parent = parent
        self.fd = fd
        self.size = 4096
        self.content = ''
        self.offset = 0
        self.date = str(datetime.now())
