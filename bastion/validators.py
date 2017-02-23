"""
    Input validation classes.
"""



yn_answers = ['y', 'n', 'yes', 'no']
commands = ['mkfs', 'open', 'ls', 'read', 'write', 'seek', 'close',
            'mkdir', 'rmdir', 'tree', 'cd', 'cat', 'import', 'export']



def validate_yes_no(text):
    if text:
        if text not in yn_answers:
            print('This input is not yes, no, y, or n.')
            return False
        return True


def validate_command(text):
    if text:
        if text not in commands:
            print('This input is not a valid command.')
            return False
        return True


def validate_mkfs(text):
    if text:
        if text != 'mkfs':
            print('Please call mkfs when the file system does not yet exist')
            return False
        return True

