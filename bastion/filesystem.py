import pickle


class FileSystem:
    CONST_FILE_SYSTEM_NAME = "file_system.p"
    open_files = []

    def __init__(self, filesystem=None):
        try:
            if filesystem is not None:
                pickle_load = open(filesystem, 'rb')
            else:
                pickle_load = self.load(self.find())
            self.total_size = pickle_load.total_sizes
            self.children = pickle_load.children
            self.root = pickle_load.root
            self.exists = True
        except IOError:
            self.total_size = 0
            self.children = []
            self.root = Directory(None, "/")
            self.exists = False

    def find(self):
        return open(self.CONST_FILE_SYSTEM_NAME, "rb")

    def load(self, pickle_file):
        pickle_load = pickle.load(pickle_file)
        return pickle_load

    # New file system is already created on failed opening. This function saves
    # the information after the user gives consent.
    def create(self):
        pickle.dump(self, open(self.CONST_FILE_SYSTEM_NAME, "wb"))
        return

    def add_child(self, child):
        self.children.append(child)


class Directory:
    def __init__(self, parent, name):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class File:
    def __init__(self, parent):
        self.name = ""
        self.parent = parent
        self.fd = 0
        self.size = 0
        self.content = ""  # Binary?
        self.offset = 0
