import calendar
import datetime as dt
from collections import UserDict, defaultdict

from .Record import *
from .Notes import *


class AddressBook(UserDict[Name, Record]):
    def __init__(self):
        super().__init__()
        self.notes = Notes()

    def add_record(self, rec: Record):
        self.data[str(rec.name)] = rec

    def add_note(self, text: str):
        return self.notes.add(Note(text))

    def get_all_contacts(self):
        contacts = list(self.data.values())
        if len(contacts) == 0:
            raise KeyError("No contacts in address book")
        else:
            return contacts

    def find(self, name: str):
        rec = self.data.get(name)
        if rec is None:
            raise KeyError(f"Contact with name {name} not found")
        return rec

    def delete(self, name: str):
        try:
            self.data.pop(name)
        except KeyError:
            raise KeyError(f"Contact with name {name} not found")

    def get_birthdays_per_days(self, delta: int):
        upcoming_birthdays = defaultdict(list)
        today = dt.datetime.today().date()
        for rec in self.get_all_contacts():
            if rec.birthday is None:
                continue
            birthday = rec.birthday.value.date()
            try:  # can be ValueError here if the birthday is on February 29
                next_birthday = birthday.replace(year=today.year)
            except ValueError:
                next_birthday = dt.datetime(today.year, 2, 28)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            if next_birthday.weekday() == 5:
                next_birthday = next_birthday + dt.timedelta(days=2)
            if next_birthday.weekday() == 6:
                next_birthday = next_birthday + dt.timedelta(days=1)

            delta_days = (next_birthday - today).days

            if 0 <= delta_days < delta:
                day_of_the_week = next_birthday.weekday()
                user_name = rec.name.value
                upcoming_birthdays[(next_birthday, day_of_the_week)].append(user_name)

        if not upcoming_birthdays:
            return f"No upcoming birthdays for {delta} days"

        sorted_result = dict(sorted(upcoming_birthdays.items()))
        result = ""
        for cong_day, names in sorted_result.items():
            result += "{:<10}({}): ".format(calendar.day_name[cong_day[1]], cong_day[0].strftime("%d.%m.%Y"))
            result += ", ".join(names) + "\n"
        
        return result.strip("\n")

    def __str__(self):
        if len(self.data):
            return "\n".join(map(str, self.get_all_contacts()))
        else:
            return "No contacts in address book"

    def search(self, search_str: str):
        found_contacts = []

        for rec in self.get_all_contacts():
            user_info = str(rec.name)
            if rec.phones:
                user_info += ", " + ", ".join(str(phone) for phone in rec.phones)
            if rec.birthday is not None:
                user_info += ", " + str(rec.birthday)
            if rec.email is not None:
                user_info += ", " + str(rec.email)
            if rec.address is not None:
                user_info += ", " + str(rec.address)

            if search_str.lower() in user_info.lower():
                found_contacts.append(rec)

        if not found_contacts:
            raise IncorrectFormatException("No contacts found")

        return found_contacts
    
    def get_contact_names(self):
        "return List of contact names"
        return list(map(str, self.data.keys()))
