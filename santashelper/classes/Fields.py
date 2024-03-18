import re
from datetime import datetime

class IncorrectFormatException(Exception):
    pass

class IncorrectNoteIndexError(Exception):
    pass

class NotesNotFoundError(Exception):
    """Exception raised when notes are not found."""
    pass

class NotFoundError(Exception):
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
        value = re.sub("[^\d\.]", "", value)
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
            birthdate = datetime.strptime(value, '%d.%m.%Y')
            self._validate_age(birthdate)
            return birthdate
        except ValueError:
            raise IncorrectFormatException(
                'Birthday must be in format DD.MM.YYYY')

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def _validate_age(self, birthdate):
        current_date = datetime.now()
        age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
        if age > 16:
            raise IncorrectFormatException("Alas, it seems this little one has outgrown their childlike wonder")      
 
        
class Note(Field):
    def __init__(self, value: str):
        super().__init__(value)
        self.tags = set()

    def __shorten_value(self) -> str:
        ch_lim = 60
        if len(self.value) <= ch_lim:
            return self.value
        else:
            return self.value[:ch_lim - 3] + '...'

    def get_preview(self) -> str:
        ret = self.__shorten_value()
        if len(self.tags) > 0:
            ret += "; tags: " + ", ".join(self.tags)
        return ret
    
    def __str__(self):
        ret = super().__str__()
        if len(self.tags) > 0:
            ret += "\ntags: " + ", ".join(self.tags)
        return ret


class WishlistItem(Field):
    pass        
