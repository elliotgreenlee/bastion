from prompt_toolkit.validation import Validator, ValidationError


yn_answers = ['y', 'n', 'yes', 'no']
commands = ['mkfs', 'open', 'ls', 'read', 'write', 'seek', 'close',
            'mkdir', 'rmdir', 'tree', 'cd', 'cat', 'import', 'export']


class YesNoValidator(Validator):

    def validate(self, document):
        text = document.text

        if text:
            if text not in yn_answers:
                raise ValidationError(message='This input is not yes, no, y, or n.',
                                      cursor_position=0)


class CommandValidator(Validator):
    def validate(self, document):
        text = document.text

        if text:
            if text not in commands:
                raise ValidationError(message='This input is not a valid command.',
                                      cursor_position=0)

