from classes.Record import *
from classes.Notes import *

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
            raise IncorrectFormatException("No contacts in address book")
        else:
            return contacts

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
        for rec in self.get_all_contacts():
            if rec.birthday is None:
                continue
            birthday = rec.birthday.value.date().replace(year=cur_year)
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
        
