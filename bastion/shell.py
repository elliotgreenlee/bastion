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
            try:
                text = raw_input("bastion> \n")
            except EOFError:
                print("Exiting!")
                sys.exit(0)
        else:
            text = raw_input("bastion> \n")
            if not validator(text):
                return None

    except KeyboardInterrupt:
        print("Exiting!")
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
            prompt_input = accept_input()
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
            return

        cmd_str = input_pieces[0]
        number_of_arguments = len(input_pieces) - 1

            # No arguments
            # Incorrect number of arguments
            # Arguments don't work in function
            # Function didn't work

        # Determine command
        if cmd_str == 'mkfs':
            if number_of_arguments != 0:
                print('usage: ' + cmd_str + ': 0 arguments')
                return

            return MKFS(self).run
        elif cmd_str == 'open':
            if number_of_arguments != 2:
                print('usage: ' + cmd_str + ': 2 arguments')
                return

            filename = input_pieces[1]
            flag = input_pieces[2]

            return Open(self, filename, flag).run()
        elif cmd_str == 'read':
            if number_of_arguments != 2:
                print('usage: ' + cmd_str + ': 2 arguments')
                return

            fd = input_pieces[1]
            size = input_pieces[2]

            return Read(self, fd, size).run()
        elif cmd_str == 'write':
            if input_pieces[2][0] != '"' or input_pieces[-1][-1] != '"':
                print('usage: ' + cmd_str + ': 2 arguments, and the string must begin and end with "')
                return

            fd = input_pieces[1]
            string = ' '.join(input_pieces[2:])
            string = string[1:len(string)-1]

            return Write(self, fd, string).run()
        elif cmd_str == 'seek':
            if number_of_arguments != 2:
                print('usage: ' + cmd_str + ': 2 arguments')
                return

            fd = input_pieces[1]
            offset = input_pieces[2]

            return Seek(self, fd, offset).run()
        elif cmd_str == 'close':
            if number_of_arguments != 1:
                print('usage: ' + cmd_str + ': 1 arguments')
                return

            fd = input_pieces[1]

            return Close(self, fd).run()
        elif cmd_str == 'mkdir':
            if number_of_arguments != 1:
                print('usage: ' + cmd_str + ': 1 arguments')
                return

            dirname = input_pieces[1]

            return MKDIR(self, dirname).run()
        elif cmd_str == 'rmdir':
            if number_of_arguments != 1:
                print('usage: ' + cmd_str + ': 1 arguments')
                return

            dirname = input_pieces[1]

            return RMDIR(self, dirname).run()
        elif cmd_str == 'cd':
            if number_of_arguments != 1:
                print('usage: ' + cmd_str + ': 1 arguments')
                return

            dirname = input_pieces[1]

            return CD(self, dirname).run()
        elif cmd_str == 'ls':
            if number_of_arguments != 0:
                print('usage: ' + cmd_str + ': 0 arguments')
                return

            return LS(self).run()
        elif cmd_str == 'cat':
            if number_of_arguments != 1:
                print('usage: ' + cmd_str + ': 1 arguments')
                return

            filename = input_pieces[1]

            return CAT(self, filename).run()
        elif cmd_str == 'tree':
            if number_of_arguments != 0:
                print('usage: ' + cmd_str + ': 0 arguments')
                return

            return Tree(self).run()
        elif cmd_str == 'import':
            if number_of_arguments != 2:
                print('usage: ' + cmd_str + ': 2 arguments')
                return

            srcname = input_pieces[1]
            destname = input_pieces[2]

            return Import(self, srcname, destname).run()
        elif cmd_str == 'export':
            if number_of_arguments != 2:
                print('usage: ' + cmd_str + ': 2 arguments')
                return

            srcname = input_pieces[1]
            destname = input_pieces[2]

            return Export(self, srcname, destname).run()
        else:
            print("Command not recognized")
            # TODO: Tell user to try again

