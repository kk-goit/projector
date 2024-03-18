import calendar
from datetime import timedelta

from .Record import *
from .Notes import *


class AddressBook(UserDict[Name, Record]):
    def __init__(self):
        super().__init__()
        self.notes = Notes()

    def add_record(self, rec: Record):
        self.data[rec.name] = rec

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

    def get_birthdays_per_week(self, delta: str):
        if delta[0].isdecimal():
            if int(delta[0]) < 11:
                delta = int(delta[0])
        else:
            delta = 10

        upcoming_birthdays = defaultdict(list)
        today = datetime.today().date()
        for rec in self.get_all_contacts():
            if rec.birthday is None:
                continue
            birthday = rec.birthday.value.date()
            try:  # can be ValueError here if the birthday is on February 29
                next_birthday = birthday.replace(year=today.year)
            except ValueError:
                next_birthday = datetime(today.year, 2, 28)

            if next_birthday < today and next_birthday.month == 1:
                next_birthday = next_birthday.replace(year=today.year + 1)

            if next_birthday.weekday() == 5:
                next_birthday = next_birthday + timedelta(days=2)
            if next_birthday.weekday() == 6:
                next_birthday = next_birthday + timedelta(days=1)

            delta_days = (next_birthday - today).days

            if 0 <= delta_days < delta:
                day_of_the_week = next_birthday.weekday()
                user_name = rec.name.value
                upcoming_birthdays[day_of_the_week].append(user_name)

        if not upcoming_birthdays:
            return "No upcoming birthdays"

        sorted_result = dict(sorted(upcoming_birthdays.items()))

        day_today = today.weekday()

        birthdays_this_week = dict(
            filter(lambda week_day: week_day[0] >= day_today, sorted_result.items())
        )
        birthdays_next_week = dict(
            filter(lambda week_day: week_day[0] < day_today, sorted_result.items())
        )

        result = ""
        if birthdays_this_week:
            result += "This week:\n"
            for day, names in birthdays_this_week.items():
                result += f"{calendar.day_name[day]}: {', '.join(names)}\n"

        if birthdays_next_week:
            result += "Next week:\n"
            for day, names in birthdays_next_week.items():
                result += f"{calendar.day_name[day]}: {', '.join(names)}\n"

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
