"""
    Bastion shell.
"""

import os
import sys

from prompt_toolkit import prompt

from bastion.filesystem import FileSystem
from bastion.commands import MKFS, Open, Read
from bastion.validators import CommandValidator
from bastion.validators import MkfsValidator


def accept_input(validator=None):
    """
    Accept input and validate it with the validator passed in, if any.

    :param validator:
    :return: str
    """
    try:
        if validator is None:
            text = prompt('bastion> ', vi_mode=True)
        else:
            text = prompt('bastion> ', vi_mode=True, validator=validator)
    except KeyboardInterrupt:
        print('Exitting!')
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
            if not self.file_system.on_disk():
                print("Type mkfs to create a new file system.")
                text = accept_input(validator=MkfsValidator())
                if text == 'mkfs':
                    MKFS(self.file_system, None).run()
            else:
                self.file_system.load_from_disk()
                break

        while True:
            prompt_input = accept_input(validator=CommandValidator())
            self.parse(prompt_input)

    # Parse the next line and call the related command
    def parse(self, prompt_input):
        """
        Parse a single line of input.

        :param prompt_input:
        :return:
        """

        # TODO: ASK IN CLASS IF EACH COMMAND NEEDS TO SUPPORT REDIRECTION, OR JUST sh
        # TODO: Determine if redirection
        # TODO: Determine input location (would this need to open the file?)
        # TODO: Determine output location

        # TODO: determine command

        # TODO: determine command arguments

        # TODO: determine if valid

        # TODO: Call specific command init with arguments
        # file_system, current_directory, input location, output location,
        # and specific command arguments
        # Maybe all commands don't need input location from redirection

        if prompt_input == 'mkfs':
            return MKFS(self.file_system, None).run()
        elif prompt_input == 'open':
            return Open(self.file_system).run()
        elif prompt_input == 'read':
            return Read().run()
