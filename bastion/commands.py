from .filesystem import *
from bastion.validators import validate_yes_no


# TODO: pass shell to every function, it has the file system

# Make a new file system, i.e., format the disk so that it
# is ready for other file system operations.
class MKFS():
    def __init__(self, shell):
        self.shell = shell
        self.file_system = self.shell.file_system

    def run(self):
        self.file_system.initialize()


# Open a file with the given <flag>, return a file
# descriptor <fd> associated with this file.
# <flag>: 1: "r"; 2: "w"
# The current file offset will be 0 when the file is opened.
# If a file does not exist, and it is opened for "w", then
# it will be created with a size of 0. This command should
# print an integer as the fd of the file.
# Example: open foo w shell returns SUCCESS, fd=5
class Open():
    def __init__(self, shell, args):
        filename = ""
        flag = ""

    def run(self):
        return


# Read <size> bytes from the file associated with <fd>, from
# current file offset. The current file offset will move forward
# <size> bytes after read.
# Example: read 5 10 shell returns the contents of the file
# (assuming it has been written)
class Read():
    def __init__(self, shell, args):
        fd = ""
        size = ""

    def run(self):
        return


# Write <string> into file associated with <fd>, from current
# file offset. The current file offset will move forward the
# size of the string after write. Here <string> must be formatted
# as a string. If the end of the file is reached, the size of the
# file will be increased.
# Example: write 5 "hello, world"
class Write():
    def __init__(self, shell, args):
        fd = ""
        string = ""

    def run(self):
        return


# Move the current file offset associated with <fd> to a new file
# offset at <offset>. The <offset> means the number of bytes from
# the beginning of the file.
# Example: seek 5 10
class Seek():
    def __init__(self, shell, args):
        fd = ""
        offset = ""

    def run(self):
        return


# Close the file associated with <fd>.
# Example: close 5
class Close():
    def __init__(self, shell, args):
        fd = ""

    def run(self):
        return


# Create a sub-directory <dirname> under the current directory.
# Example: mkdir foo
class MKDIR():
    def __init__(self, shell, args):
        dirname = ""

    def run(self):
        # Check if directory already exists
        exists = False
        for child in self.current_directory.children:
            if self.dirname == child.name:
                exists = True

        new_directory = Directory(self.current_directory, self.dirname)  # create new directory
        self.current_directory.add_child(new_directory)
        return


# Remove the sub-directory <dirname>.
# Example: rmdir foo
class RMDIR():
    def __init__(self, shell, args):
        dirname = ""

    def run(self):
        return


# Change the current directory to <dirname>.
# Example: cd ../../foo/bar
class CD():
    def __init__(self, shell, args):
        dirname = ""

    def run(self):
        return


# Show the content of the current directory. No parameters
# need to be supported.
class LS():
    def __init__(self, shell):

    def run(self):
        return


# Show the content of the file.
# Example: cat foo
class CAT():
    def __init__(self, shell, args):
        filename = ""

    def run(self):
        return


# List the contents of the current directory in a
# tree-format. For each file listed, its date file
# size should be included.
# To understand this command better, you may refer
# to this command output under the command line shell
# in a Windows system.
class Tree():
    def __init__(self, shell):

    def run(self):
        return


# Import a file from the host machine file system to
# the current directory.
# Example: import /d/foo.txt foo.txt
class Import():
    def __init__(self, shell, args):
        srcname = ""
        destname = ""

    def run(self):
        return


# Export a file from the current directory to the host
# machine file system.
# Example: export foo.txt /d/foo.txt
class Export():
    def __init__(self, shell, args):
        srcname = ""
        destname = ""

    def run(self):
        return
