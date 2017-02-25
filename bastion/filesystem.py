import pickle
import os
import sys
import uuid
from datetime import datetime
from collections import defaultdict


class FileSystemAllocation:
    """Was originally planning on using this to track "allocations" in memory,
    meaning files that span several blocks."""
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size


class FileSystem:
    CONST_FILE_SYSTEM_NAME = "file_system.bastion"
    TOTAL_BLOCKS = 250
    BLOCK_SIZE = 4096

    def __init__(self):
        self.exists = self.on_disk()
        self.fd = 0
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child('..', self.root.parent)

        self.free_list = [FileSystemAllocation(20971520, 83886080)]  # 20 MB in, size 80 MB

    def initialize(self):
        """If the filesystem does not exist yet or we are
        overwriting the existing filesystem, run this function."""

        if self.on_disk():
            os.remove(self.CONST_FILE_SYSTEM_NAME)

        # Overwrite old values
        self.exists = False
        self.fd = 0
        self.open_files = []
        self.root = Directory(None, "/")
        self.root.parent = self.root
        self.root.children = []
        self.root.add_child('..', self.root.parent)

        self.free_list = [FileSystemAllocation(20971520, 83886080)]  # 20 MB in, size 80 MB

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
        print self.open_files
        sys.stdout.flush()
        for file in self.open_files:
            if str(fd) == str(file[0]):
                return file[2], file[1]

    def find_open_file(self, name):
        for file in self.open_files:
            if name == file[2].name:
                return file[2]

    def get_free_space(self, size):
        """
            Return offset where space starts, return None otherwise
        """

        # TODO: make sure this is correct

        # find size that works in free_list
        chosen_space = None
        for free_space in self.free_list:
            if free_space.size >= size:
                chosen_space = free_space

        # if no size works, return -1
        if chosen_space is None:
            return -1

        chosen_offset = chosen_space.offset
        chosen_size = chosen_space.size

        # remove free_space from the free_list
        self.free_list.remove(chosen_space)

        # append the non needed part of the piece back to free_list
        self.free_space(chosen_offset + size, chosen_size - size)

        # return the required piece
        return chosen_offset

    def load_from_disk(self, offset, size):
        # TODO: Make sure this is correct
        # load file at offset of length size into temporary string content
        with open(self.CONST_FILE_SYSTEM_NAME, 'rwb') as f:
            f.seek(offset)
            content = f.read(size)

        return content

    def write_to_disk(self, offset, content):
        """
            Write content (bytes) to offset, return None if not possible.
        """

        # TODO: Make sure this is correct (it should overwrite what is there)
        # put content at offset
        with open(self.CONST_FILE_SYSTEM_NAME, 'rwb') as f:
            f.seek(offset)
            f.write(content)

    def free_space(self, offset, size):
        """
            Go to offset and delete up to size
        """

        # TODO: Check to make sure these are right.

        # append (offset, size) to the free_list
        self.free_list.append(FileSystemAllocation(offset, size))
        combine = True
        while combine:
            combine = False
            self.free_list.sort(key=lambda x: x[0])
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
        self.content = ''
        self.offset = 0
        self.date = str(datetime.now())

        self.fsa = FileSystemAllocation(offset, 4096)
