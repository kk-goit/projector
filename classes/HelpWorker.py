from classes.AddressBook import *

def input_error(msg):
    "Inclosed exceptions decorator"
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError):
                return msg
            except (IncorrectFormatException,
                    IncorrectNoteIndexError,
                    NotesNotFoundError,
                    KeyError) as err:
                return err

        return inner
    return decorator
    
    
class HelpWorker:
    @input_error("Give me name and info please.")
    def add_contact(self, args, contacts: AddressBook):
        name, info = args
        record = Record(name)

        try:
            record.add_phone(info)
        except IncorrectFormatException:
            try: 
                record.add_email(info)
            except IncorrectFormatException:
                try:
                    record.add_birthday(info)
                except IncorrectFormatException:
                    raise IncorrectFormatException(f"{info} is not a phone number, email or birthday")

        contacts.add_record(record)
        return "Contact added."


    @input_error("Give me name and new phone please.")
    def change_contact(self, args, contacts: AddressBook):
        name, no = args
        rec = contacts.find(name)
        rec.change_phone(no)
        return "Contact updated."

    @input_error("Give me name please.")
    def delete_contact(self, args, contacts: AddressBook):
        name = args[0]
        contacts.delete(name)
        return "Contact deleted."
    
    @input_error("Contact not found.")
    def show(self, args, contacts: AddressBook):
        name = args[0]
        return contacts.find(name)

    @input_error("Give me name and phone to add please.")
    def add_phone(self, args, contacts: AddressBook):
        name, phone = args
        rec = contacts.find(name)
        rec.add_phone(phone)
        return f"New phone added to {name}"

    @input_error("Give me name, old phone, and new phone please.")
    def change_phone(self, args, contacts: AddressBook):
        name, old_phone, new_phone = args
        rec = contacts.find(name)
        rec.edit_phone(old_phone, new_phone)
        return f"Phone for {name} changed from {old_phone} to {new_phone}"


    @input_error("Give me name and phone to delete please.")
    def del_phone(self, args, contacts: AddressBook):
        name, phone = args
        rec = contacts.find(name)
        rec.remove_phone(phone)
        return f"Phone {phone} deleted from the contact {name}"


    @input_error("Give me name and address please.")
    def add_address(self, args, contacts: AddressBook):
        name = args[0]
        # користувач може вводити адресу через пробіл
        # тому обєднуємо решту аргументів в одну строку
        address = ' '.join(map(str, args[1:]))
        rec = contacts.find(name)
        rec.add_address(address)
        return "Address added."


    @input_error("Give me name please.")
    def del_address(self, args, contacts: AddressBook):
        name = args[0]
        rec = contacts.find(name)
        rec.remove_address()
        return "Address deleted."


    @input_error("Give me name and birthday please.")
    def add_birthday(self, args, contacts: AddressBook):
        name, bd = args
        rec = contacts.find(name)
        rec.add_birthday(bd)
        return "Birthday added."


    @input_error("Give me name please.")
    def del_birthday(self, args, contacts: AddressBook):
        name = args[0]
        rec = contacts.find(name)
        rec.remove_birthday()
        return f"Birthday deleted from the contact {name}"


    @input_error("")
    def get_birthdays_per_week(self, contacts: AddressBook):
        return contacts.get_birthdays_per_week()


    def print_all(self, contacts: AddressBook):
        chunk_size=5
        items = list(contacts.values())
        total_items = len(items)
        if not total_items:
            return "Address book is empty."
        start_index = 0

        while start_index < total_items:
            end_index = min(start_index + chunk_size, total_items)
            current_chunk = items[start_index:end_index]

            for value in current_chunk:
                print(value)

            if end_index < total_items:
                input("Press Enter to continue...")

            start_index = end_index
        return "End of addres book"


    @input_error("Give me name please.")
    def show_phone(self, args, contacts: AddressBook):
        name = args[0]
        return str(contacts.find(name))


    @input_error("Give me name and email please.")
    def add_email(self, args, contacts: AddressBook):
        name, email = args
        rec = contacts.find(name)
        rec.add_email(email)
        return "Email added."


    @input_error("Give me name please.")
    def del_email(self, args, contacts: AddressBook):
        name = args[0]
        rec = contacts.find(name)
        rec.remove_email()
        return f"Email deleted from the contact {name}"


    @input_error("Give me name please.")
    def show_birthday(self, args, contacts: AddressBook):
        name = args[0]
        rec = contacts.find(name)
        if rec.birthday is None:
            return "Birthday doesn't setted."
        return f"{name}'s birthday is {rec.birthday}"


    @input_error("Give me argument for search.")
    def search(self, args, contacts: AddressBook):
        search_arg = args[0]
        if len(search_arg) < 3:
            return "Search string must be at least 3 characters long."
        result = contacts.search(search_arg)
        return '\n'.join([str(rec) for rec in result])


    @input_error("")
    def add_note(self, book: AddressBook):
        text = input('Note text:')
        index = book.add_note(text)
        return f"Added note with index {index}"


    @input_error("Give me note index please.")
    def show_note(self, args, book: AddressBook):
        index = args[0]
        return book.notes.show(index)


    @input_error("")
    def show_notes(self, args, book: AddressBook):
        return book.notes.list()


    @input_error("Give text to search please.")
    def search_notes(self, args, book: AddressBook):
        search_str = args[0]
        return book.notes.search(search_str)


    @input_error("Give me note index please.")
    def del_note(self, args, book: AddressBook):
        index = args[0]
        book.notes.delete(index)
        return f"Note with index {index} deleted"


    @input_error("Give me note index please.")
    def change_note(self, args, book: AddressBook):
        index = args[0]
        new_text = input('Enter a new text: ')
        book.notes.change_note(index, new_text)
        return f"Note with index {index} changed"


