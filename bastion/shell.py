"""
    Bastion shell.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys

from bastion.filesystem import FileSystem
from bastion.commands import *
from bastion.validators import validate_command
from bastion.validators import validate_mkfs


def accept_input(validator=None):
    """
    Accept input and validate it with the validator passed in, if any.

    :param validator:
    :return: str
    """
    try:
        if validator is None:
            text = raw_input("bastion> ")
        else:
            text = raw_input("bastion> ")
            if not validator(text):
                return None

    except KeyboardInterrupt:
        print("Exitting!")
        sys.exit(0)
    return text


class Shell(object):
    """
    Main class for the shell.
    """

    def __init__(self):
        self.current_line = ""
        self.file_system = self.create_filesystem_object()
        self.current_directory = self.file_system.root

    @staticmethod
    def create_filesystem_object():
        """
        Create an instance of the FileSystem.

        :return: FileSystem
        """
        file_system = FileSystem()
        return file_system

    def run(self):
        """
        Execution loop of the shell.

        :return:
        """
        while True:
            print("Type mkfs to create a new file system.")
            text = accept_input(validator=validate_mkfs)
            if text is None:
                continue
            if text == 'mkfs':
                MKFS(self).run()
                break

        while True:
            prompt_input = accept_input(validator=validate_command)
            if prompt_input is None:
                continue
            self.parse(prompt_input)

    # Parse the next line and call the related command
    def parse(self, prompt_input):
        """
        Parse a single line of input.

        :param prompt_input:
        :return:
        """

        input_pieces = str.split(prompt_input)
        if len(input_pieces) == 0:
            print("no")  # TODO: tell user to try again
            return

        cmd_str = input_pieces[0]
        # TODO: refactor the length of the input_pieces-1 as number_of_arguments
        # TODO: parse arguments and determine type validity

        # Determine command
        if cmd_str == 'mkfs':
            if len(input_pieces) != 1:
                print("no")  # TODO: tell user to try again
                return

            return MKFS(self).run
        elif cmd_str == 'open':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            filename = input_pieces[1]
            flag = input_pieces[2]

            return Open(self, filename, flag).run()
        elif cmd_str == 'read':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            fd = input_pieces[1]
            size = input_pieces[2]

            return Read(self, fd, size).run()
        elif cmd_str == 'write':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            fd = input_pieces[1]
            string = input_pieces[2]

            return Write(self, fd, string).run()
        elif cmd_str == 'seek':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            fd = input_pieces[1]
            offset = input_pieces[2]

            return Seek(self, fd, offset).run()
        elif cmd_str == 'close':
            if len(input_pieces) != 2:
                print("no")  # TODO: tell user to try again
                return

            fd = input_pieces[1]

            return Close(self, fd).run()
        elif cmd_str == 'mkdir':
            if len(input_pieces) != 2:
                print("no")  # TODO: tell user to try again
                return

            dirname = input_pieces[1]

            return MKDIR(self, dirname).run()
        elif cmd_str == 'rmdir':
            if len(input_pieces) != 2:
                print("no")  # TODO: tell user to try again
                return

            dirname = input_pieces[1]

            return RMDIR(self, dirname).run()
        elif cmd_str == 'cd':
            if len(input_pieces) != 2:
                print("no")  # TODO: tell user to try again
                return

            dirname = input_pieces[1]

            return CD(self, dirname).run()
        elif cmd_str == 'ls':
            if len(input_pieces) != 1:
                print("no")  # TODO: tell user to try again
                return

            return LS().run(self)
        elif cmd_str == 'cat':
            if len(input_pieces) != 2:
                print("no")  # TODO: tell user to try again
                return

            filename = input_pieces[1]

            return CAT(self, filename).run()
        elif cmd_str == 'tree':
            if len(input_pieces) != 1:
                print("no")  # TODO: tell user to try again
                return

            return Tree(self).run()
        elif cmd_str == 'import':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            srcname = input_pieces[1]
            destname = input_pieces[2]

            return Import(self, srcname, destname).run()
        elif cmd_str == 'export':
            if len(input_pieces) != 3:
                print("no")  # TODO: tell user to try again
                return

            srcname = input_pieces[1]
            destname = input_pieces[2]

            return Export(self, srcname, destname).run()
        else:
            print("no")
            # TODO: Tell user to try again

