from collections import UserDict,defaultdict
from datetime import datetime

class BookValueError(ValueError):
    pass


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        self.validate(value)
        super().__init__(value)

    def validate(self, value: str):
        if len(value) != 10 or not value.isdecimal():
            raise BookValueError("Phone must have 10 digits")
        

class Birthday(Field):
    def __init__(self, value: str):
        parts = value.split(".")
        if len(parts) != 3:
            raise BookValueError("Birthday must be in format DD.MM.YYYY")
        self.birthdate = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date: str):
        self.birthday = Birthday(date)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str, default = None):
        for itm in self.phones:
            if str(itm) == phone:
                return itm
        return default

    def remove_phone(self, phone:str):
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
        res += f", birthday: {self.birthday}" if self.birthday else ""
        return res


class AddressBook(UserDict):
    def add_record(self, rec: Record):
        self.data[str(rec.name)] = rec

    def find(self, name: str):
        rec = self.data.get(name)
        if rec is None:
            raise KeyError(name)
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
    

if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("12.03.2001")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    print(book)
    print(book.get_birthdays_per_week())

