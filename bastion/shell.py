from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


from bastion.filesystem import FileSystem
from bastion.commands import MKFS
from bastion.commands import call_command
from bastion.validators import CommandValidator


def accept_input(history=None, validator=None):
    text = prompt('bastion> ', history=history, auto_suggest=AutoSuggestFromHistory(), vi_mode=True, validator=validator)
    return text




class Shell(object):
    def __init__(self):
        self.history = InMemoryHistory()
        self.current_line = ""
        self.file_system = self.get_file_system()
        self.current_directory = self.file_system.root

    def get_file_system(self):
        file_system = FileSystem()
        if not file_system.exists:
            print("Type mkfs to create a new file system.")
            while True:
                text = accept_input(history=self.history, validator=CommandValidator)
                call_command(text, self.file_system)

        return file_system

    def run(self):
        while True:
            input = accept_input(history=self.history, validator=CommandValidator)
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
