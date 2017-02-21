"""
    Bastion shell.
"""

import os
import sys

from prompt_toolkit import prompt

from bastion.filesystem import FileSystem
from bastion.commands import MKFS
from bastion.commands import call_command
from bastion.validators import CommandValidator
from bastion.validators import MkfsValidator


def accept_input(validator=None):
    try:
        text = prompt('bastion> ', vi_mode=True, validator=validator)
    except KeyboardInterrupt:
        print('Exitting!')
        sys.exit(0)
    return text


class Shell(object):
    def __init__(self):
        self.current_line = ""
        self.file_system = self.get_file_system()
        self.file_system_exists = self.file_system.exists
        self.current_directory = self.file_system.root

    @staticmethod
    def get_file_system():
        file_system = FileSystem()
        return file_system

    def run(self):
            while True:
                if not self.file_system.exists:
                    print("Type mkfs to create a new file system.")
                    text = accept_input(validator=MkfsValidator())
                    call_command(text, self.file_system)
                input = accept_input(validator=CommandValidator())
                self.parse(input)

    # Parse the next line and call the related command
    def parse(self, input):
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
        pass
