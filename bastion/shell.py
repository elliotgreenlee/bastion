from bastion.filesystem import FileSystem


class Shell(object):
    def __init__(self):
        self.current_line = ""
        self.file_system = self.get_file_system()
        self.current_directory = self.file_system.root
        return

    # Load or create a new file system
    def get_file_system(self):
        file_system = FileSystem()
        while not file_system.exists:
            print ">> Type mkfs to create a new file system \n"
            print ">>"
            self.parse(self.read_next_line())

        return file_system

    # The main loop of shell
    def run(self):
        while True:
            print ">> "
            self.parse(self.read_next_line())

    # Read in the next line of input from the console
    def read_next_line(self):
        # TODO: Read in a line of user input
        return ""

    # Parse the next line and call the related command
    def parse(self, next_line):
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
        return
