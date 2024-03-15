import re
from datetime import datetime

class IncorrectFormatException(Exception):
    pass

class IncorrectNoteIndexError(Exception):
    pass

class NotesNotFoundError(Exception):
    """Exception raised when notes are not found."""
    pass


class Field:
    __value = None

    def __init__(self, value: str):
        self.value = value

    def parse(self, data: str):
        return data
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, data: str):
        self.__value = self.parse(data)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def parse(self, value: str):
        if len(value) != 10 or not value.isdecimal():
            raise IncorrectFormatException("Phone must have 10 digits")
        return value


class Address(Field):
    pass


class Email(Field):
    def parse(self, value: str):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise IncorrectFormatException('Incorrect email format')
        return value


class Birthday(Field):
    def parse(self, value):
        try:
            return datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise IncorrectFormatException(
                'Birthday must be in format DD.MM.YYYY')

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    
        
class Note(Field):
    def __shorten_value(self) -> str:
        ch_lim = 60
        if len(self.value) <= ch_lim:
            return self.value
        else:
            return self.value[:ch_lim - 3] + '...'

    def get_preview(self) -> str:
        return self.__shorten_value()
        
