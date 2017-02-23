from .filesystem import *
from bastion.validators import validate_yes_no


def call_command(cmd_str, args):
    if cmd_str == 'mkfs':
        return MKFS(*args).run()
    elif cmd_str == 'open':
        return Open(*args).run()
    elif cmd_str == 'read':
        return Read(*args).run()


class Command(object):
    def __init__(self, file_system, prompt_input, prompt_output=None):
        self.file_system = file_system
        self.prompt_input = prompt_input
        self.prompt_output = prompt_output

    def run(self):
        pass


# Make a new file system, i.e., format the disk so that it
# is ready for other file system operations.
class MKFS(Command):
    def __init__(self, file_system, prompt_input):
        super(MKFS, self).__init__(file_system, prompt_input)

    def run(self):
        from bastion.shell import accept_input
        if self.file_system.on_disk():
            while True:
                print("Are you sure you want to clear the old file system? (y/n)")
                prompt_input = accept_input(validator=validate_yes_no)
                if prompt_input is None:
                    continue
                if prompt_input in ['yes', 'y']:
                    self.file_system.initialize()
                    break
                elif prompt_input in ['no', 'n']:
                    print("Not overwriting filesystem.")
                    break
        else:
            self.file_system.initialize()


# Open a file with the given <flag>, return a file
# descriptor <fd> associated with this file.
# <flag>: 1: "r"; 2: "w"
# The current file offset will be 0 when the file is opened.
# If a file does not exist, and it is opened for "w", then
# it will be created with a size of 0. This command should
# print an integer as the fd of the file.
# Example: open foo w shell returns SUCCESS, fd=5
class Open(Command):
    def __init__(self, args):
        super().__init__(*args)
        filename = ""
        flag = ""

    def run(self):
        return


# Read <size> bytes from the file associated with <fd>, from
# current file offset. The current file offset will move forward
# <size> bytes after read.
# Example: read 5 10 shell returns the contents of the file
# (assuming it has been written)
class Read(Command):
    def __init__(self, args):
        super().__init__(*args)
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
class Write(Command):
    def __init__(self):
        Command.__init__()
        fd = ""
        string = ""

    def run(self):
        return


# Move the current file offset associated with <fd> to a new file
# offset at <offset>. The <offset> means the number of bytes from
# the beginning of the file.
# Example: seek 5 10
class Seek(Command):
    def __init__(self):
        Command.__init__()
        fd = ""
        offset = ""

    def run(self):
        return


# Close the file associated with <fd>.
# Example: close 5
class Close(Command):
    def __init__(self):
        Command.__init__()
        fd = ""

    def run(self):
        return


# Create a sub-directory <dirname> under the current directory.
# Example: mkdir foo
class MKDIR(Command):
    def __init__(self):
        Command.__init__()
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
class RMDIR(Command):
    def __init__(self):
        Command.__init__()
        dirname = ""

    def run(self):
        return


# Change the current directory to <dirname>.
# Example: cd ../../foo/bar
class CD(Command):
    def __init__(self):
        Command.__init__()
        dirname = ""

    def run(self):
        return


# Show the content of the current directory. No parameters
# need to be supported.
class LS(Command):
    def __init__(self):
        Command.__init__()

    def run(self):
        return


# Show the content of the file.
# Example: cat foo
class CAT(Command):
    def __init__(self):
        Command.__init__()
        filename = ""

    def run(self):
        return


# List the contents of the current directory in a
# tree-format. For each file listed, its date file
# size should be included.
# To understand this command better, you may refer
# to this command output under the command line shell
# in a Windows system.
class Tree(Command):
    def __init__(self):
        Command.__init__()

    def run(self):
        return


# Import a file from the host machine file system to
# the current directory.
# Example: import /d/foo.txt foo.txt
class Import(Command):
    def __init__(self):
        Command.__init__()
        srcname = ""
        destname = ""

    def run(self):
        return


# Export a file from the current directory to the host
# machine file system.
# Example: export foo.txt /d/foo.txt
class Export(Command):
    def __init__(self):
        Command.__init__()
        srcname = ""
        destname = ""

    def run(self):
        return
