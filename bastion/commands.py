from .filesystem import *


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
    def __init__(self, shell, filename, flag):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.filename = filename
        self.flag = flag

    def run(self):
        existing = self.shell.current_directory.find_child(self.filename)
        if existing is not None and isinstance(existing.child, Directory):
            print('open: ' + self.filename + ': This is a directory')
            return

        if self.file_system.find_open_name(self.filename) is not None:
            print('open: ' + self.filename + ': This file is already open')
            return

        # If reading mode
        if self.flag == 'r':
            if existing is None:
                print('open: ' + self.filename + ': No such file')
                return
            else:
                self.file_system.add_open_file(OpenFile(existing.child.fd, 'r', existing))
                print('Success, fd = ' + str(existing.child.fd))

        # If writing mode
        elif self.flag == 'w':
            # Get disk space
            offset = self.file_system.get_free_space(4096)
            if offset == -1:
                print('open: There is not enough space on disk for a new file')
                return

            # Create new file
            new_fd = self.file_system.get_new_fd()
            new_file = File(self.shell.current_directory, self.filename, new_fd, offset)

            # Remove existing file of same name if it exists
            if existing is not None:
                self.shell.current_directory.children.remove(existing)

            self.shell.current_directory.add_child(Child(self.filename, new_file))
            self.file_system.add_open_file(OpenFile(new_file.fd, 'w', new_file))
            print('Success, fd = ' + str(new_file.fd))

        else:
            print('usage: open: ' + self.flag + ' is not a valid flag')

        return


# Read <size> bytes from the file associated with <fd>, from
# current file offset. The current file offset will move forward
# <size> bytes after read.
# Example: read 5 10 shell returns the contents of the file
# (assuming it has been written)
class Read():
    def __init__(self, shell, fd, size):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.fd = fd
        self.size = size

    def run(self):
        # find file based on fd
        open_file = self.file_system.find_open_fd(self.fd)
        if open_file is None or open_file.mode != 'r':
            print('read: ' + self.fd + ': that file is not open for reading')
            return

        if open_file.file.offset + self.size > open_file.file.size:
            print('read: ' + self.fd + ': that file only has ' + str(open_file.file.size - open_file.file.offset) + ' bytes left')
            return

        print(open_file.file.content[open_file.file.offset: open_file.file.offset + self.size])
        open_file.file.offset += self.size
        return


# Write <string> into file associated with <fd>, from current
# file offset. The current file offset will move forward the
# size of the string after write. Here <string> must be formatted
# as a string. If the end of the file is reached, the size of the
# file will be increased.
# Example: write 5 "hello, world"
class Write():
    def __init__(self, shell, fd, string):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.fd = fd
        self.string = string

    def run(self):
        # find file based on fd
        open_file = self.file_system.get_open_fd(self.fd)
        if open_file is None or open_file.mode != 'w':
            print('write: ' + self.fd + ': that file is not open for writing')
            return

        if len(open_file.file.content) + len(self.string) > open_file.file.size:
            open_file.file.size += 4096

        new_content = open_file.file.content[0:open_file.file.offset] + self.string
        open_file.file.offset += len(self.string)
        new_content += open_file.file.content[open_file.file.offset:]
        open_file.file.content = new_content

        return


# Move the current file offset associated with <fd> to a new file
# offset at <offset>. The <offset> means the number of bytes from
# the beginning of the file.
# Example: seek 5 10
class Seek():
    def __init__(self, shell, fd, offset):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.fd = fd
        self.offset = offset

    def run(self):
        # find file based on fd
        open_file = self.file_system.get_open_fd(self.fd)
        if open_file is None:
            print('seek: ' + self.fd + ': that file is not open')
            return

        if open_file.file.offset + self.offset > open_file.file.size:
            print('seek: ' + self.fd + ': that file only has ' + str(open_file.file.size - open_file.file.offset) + ' bytes left')
            return

        open_file.file.offset += self.offset
        return


# Close the file associated with <fd>.
# Example: close 5
class Close():
    def __init__(self, shell, fd):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.fd = fd

    def run(self):
        close_file = self.file_system.get_open_fd(self.fd)
        if close_file is None:
            print('close: ' + self.fd + ': that file is not open')
            return

        self.file_system.open_files.remove(close_file)
        return


# Create a sub-directory <dirname> under the current directory.
# Example: mkdir foo
class MKDIR():
    def __init__(self, shell, dirname):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.dirname = dirname

    def run(self):
        # Check if directory already exists
        existing = self.shell.current_directory.find_child(self.dirname)
        if existing is not None:
            print('mkdir: ' + self.dirname + ': File exists')
            return

        new_directory = Directory(self.shell.current_directory, self.dirname)  # create new directory
        self.shell.current_directory.add_child(Child(self.dirname, new_directory))
        return


# Remove the sub-directory <dirname>.
# Example: rmdir foo
class RMDIR():
    def __init__(self, shell, dirname):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.dirname = dirname

    def run(self):

        deletion = self.shell.current_directory.find_child(self.dirname)
        if deletion is None:
            print('rmdir: ' + self.dirname + ': No such file or directory')
            return

        # Check if trying to remove parent
        if self.dirname == '..':
            print('rmdir: ' + self.dirname + ': Cannot remove that directory')
            return

        self.shell.current_directory.children.remove(deletion)
        return


# Change the current directory to <dirname>.
# Example: cd ../../foo/bar
class CD():
    def __init__(self, shell, dirname):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.dirname = dirname

    def run(self):
        dirlist = str.split(self.dirname, '/')

        move = self.recursive_cd(self.shell.current_directory, dirlist)
        if move is None:
            print('cd: ' + self.dirname + ': Not a directory')
            return

        self.shell.current_directory = move

        return

    def recursive_cd(self, current_directory, dirlist):
        if len(dirlist) == 0:
            return current_directory

        move = current_directory.find_child(dirlist[0])
        if move is None or not isinstance(move.child, Directory):
            return None
        else:
            return self.recursive_cd(move.child, dirlist[1:])


# Show the content of the current directory. No parameters
# need to be supported.
class LS():
    def __init__(self, shell):
        self.shell = shell
        self.file_system = self.shell.file_system

    def run(self):
        for child in self.shell.current_directory.children:
            print child.name
        return


# Show the content of the file.
# Example: cat foo
class CAT():
    def __init__(self, shell, filename):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.filename = filename

    def run(self):
        catted = self.shell.current_directory.find_child(self.filename)
        # see if it exists, see if it is a file
        if catted is None or not isinstance(catted.child, File):
            print('cat: ' + self.filename + ': Not a file')
            return

        print catted.child.content
        # TODO: print self.file_system.load_from_disk(catted.child.fsa.offset, catted.child.fsa.size)
        return


# List the contents of the current directory in a
# tree-format. For each file listed, its date file
# size should be included.
# To understand this command better, you may refer
# to this command output under the command line shell
# in a Windows system.
class Tree():
    def __init__(self, shell):
        self.shell = shell
        self.file_system = self.shell.file_system

    def run(self):
        self.tree_print(self.shell.current_directory, 0)

        return

    def tree_print(self, directory, level):
        # tree_print iterates through each child.
        for child in directory.children:

            # if file, print based on level
            if isinstance(child.child, File):
                for i in range(0, level):
                    print '\t',
                print child.name, child.child.fsa.size, child.child.date

            # if directory, print based on level, call tree_print(directory, level+1)
            if isinstance(child.child, Directory):
                for i in range(0, level):
                    print '\t',
                print child.name

                # Don't recurse upwards
                if child.name != '..':
                    self.tree_print(child.child, level+1)


# Import a file from the host machine file system to
# the current directory.
# Example: import /d/foo.txt foo.txt
class Import():
    def __init__(self, shell, srcname, destname):
        self.shell = shell
        self.file_system = self.shell.file_system

        # Arguments
        self.srcname = srcname
        self.destname = destname

    def run(self):
        return


# Export a file from the current directory to the host
# machine file system.
# Example: export foo.txt /d/foo.txt
class Export():
    def __init__(self, shell, srcname, destname):
        self.shell = shell
        self.file_system = self.shell.file_system

        self.srcname = srcname
        self.destname = destname

    def run(self):
        return
