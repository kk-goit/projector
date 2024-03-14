from collections import UserDict, defaultdict
from datetime import datetime
import re


class IncorrectFormatException(Exception):
    pass


class IncorrectNoteIndexErr(Exception):
    pass


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __init__(self, value: str):
        self.validate(value)
        super().__init__(value)

    def validate(self, value: str):
        if len(value) != 10 or not value.isdecimal():
            raise IncorrectFormatException("Phone must have 10 digits")


class Address(Field):
    pass


class Email(Field):
    def __init__(self, value: str):
        self.validate(value)
        super().__init__(value)

    def validate(self, value: str): 
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise IncorrectFormatException('Incorrect email format')


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(self.parse(value))

    def parse(self, value):
        try:
            return datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise IncorrectFormatException(
                'Birthday must be in format DD.MM.YYYY')

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_birthday(self, date: str):
        self.birthday = Birthday(date)

    def remove_birthday(self):
        self.birthday = None

    def add_address(self, address: str):
        self.address = Address(address)

    def remove_address(self):
        self.address = None

    def add_email(self, email: str):
        self.email = Email(email)

    def remove_email(self):
        self.email = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str, default=None):
        for itm in self.phones:
            if str(itm) == phone:
                return itm
        return default

    def remove_phone(self, phone: str):
        itm = self.find_phone(phone)
        if itm:
            self.phones.remove(itm)

    def edit_phone(self, old, new):
        phone = self.find_phone(old)
        if phone:
            phone.validate(new)
            phone.value = new

    def change_phone(self, phone: str):
        if len(self.phones) > 0:
            self.phones[0] = Phone(phone)
        else:
            self.add_phone(phone)

    def __str__(self):
        res = f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"
        res += f", email: {self.email}" if self.email else ""
        res += f", address: {self.address}" if self.address else ""
        res += f", birthday: {self.birthday}" if self.birthday else ""
        return res


class Note(Field):
    def __init__(self, value: str, index: int):
        super().__init__(value)
        self.index = index

    def __shorten_value(self) -> str:
        ch_lim = 30
        if len(self.value) <= ch_lim:
            return self.value
        else:
            return self.value[:ch_lim - 3] + '...'

    def get_index(self) -> int:
        return self.index

    def get_preview(self) -> str:
        return self.__shorten_value()


class Notes():
    def __init__(self):
        self.data: list[Note] = []

    def __get_by_index(self, index: str) -> Note:
        try:
            index = int(index)
            if index > 0:
                for note in self.data:
                    if note.get_index() == index:
                        return note
                raise KeyError(f"There is no note with an index {index}")
            else:
                raise IncorrectNoteIndexErr("Index can't be < 1.")
        except ValueError:
            raise IncorrectNoteIndexErr("Index should be an integer.")


    def add(self, note: Note):
        self.data.append(note)

    def delete(self, index: int):
        note_to_del = self.__get_by_index(index)
        for i, note in enumerate(self.data):
            if note == note_to_del:
                del self.data[i]

    def get_last_index(self) -> int:
        max_index = 0
        for note in self.data:
            note_index = note.get_index()
            if note_index > max_index:
                max_index = note_index

        return max_index

    def list(self, data: list[Note] = None):
        data = data if data else self.data
        if len(data) > 0:
            listed = ""
            for note in data:
                listed += f"{note.get_index()} - {note.get_preview()}\n"
            return listed
        else:
            print("Unable to locate any notes.")  # TODO; make it better for search

    def search(self, substr: str):
        matched: list[Note] = []
        for note in self.data:
            if substr in str(note):
                matched.append(note)

        return self.list(matched)

    def show(self, index: str):
        return str(self.__get_by_index(index))


class AddressBook(UserDict[Name, Record]):
    def __init__(self, initial_data=None):
        super().__init__(initial_data)
        self.notes = Notes()

    def add_record(self, rec: Record):
        self.data[rec.name] = rec

    def add_note(self, text: str):
        note_index = self.notes.get_last_index() + 1
        note = Note(text, note_index)
        self.notes.add(note)

        return note

    def find(self, name: str):
        rec = self.data.get(name)
        if rec is None:
            raise KeyError(f"Contact with name {name} not found")
        return rec

    def delete(self, name: str):
        self.data.pop(name)

    def get_birthdays_per_week(self):
        week_birthdays = defaultdict(list)
        week_days_names = ("Monday","Tuesday","Wednesday","Thursday","Friday")
        cur_year = datetime.today().year
        cur_date = datetime.today().date()
        cur_week_day = cur_date.weekday()
        for rec in self.data.values():
            if rec.birthday is None:
                continue
            birthday = rec.birthday.birthdate.date().replace(year=cur_year)
            if birthday < cur_date:
                birthday = birthday.replace(year=birthday.year+1)
            delta_days = (birthday - cur_date).days
            if delta_days >= 7:
                continue # birthday to far
            week_day = birthday.weekday()
            if week_day > 4:
                if cur_week_day in [0,6]:
                    continue # will be congraduate at next week
                week_day = 0
            week_birthdays[week_days_names[week_day]].append(str(rec.name))

        res = ""
        for day in week_birthdays.keys():
            res += "{}: {}\n".format(day, ", ".join(week_birthdays[day]))
        return res.rstrip()

    def __str__(self):
        return "\n".join(map(str, self.data.values()))
