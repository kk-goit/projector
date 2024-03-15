import pickle, cmd
from addressbook import *


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(msg):
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


@input_error("Give me name and info please.")
def add_contact(args, contacts: AddressBook):
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
def change_contact(args, contacts: AddressBook):
    name, no = args
    rec = contacts.find(name)
    rec.change_phone(no)
    return "Contact updated."

@input_error("Give me name please.")
def delete_contact(args, contacts: AddressBook):
    name = args[0]
    contacts.delete(name)
    return "Contact deleted."


@input_error("Give me name and phone to add please.")
def add_phone(args, contacts: AddressBook):
    name, phone = args
    rec = contacts.find(name)
    rec.add_phone(phone)
    return f"New phone added to {name}"

@input_error("Give me name, old phone, and new phone please.")
def change_phone(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    rec = contacts.find(name)
    rec.edit_phone(old_phone, new_phone)
    return f"Phone for {name} changed from {old_phone} to {new_phone}"


@input_error("Give me name and phone to delete please.")
def del_phone(args, contacts: AddressBook):
    name, phone = args
    rec = contacts.find(name)
    rec.remove_phone(phone)
    return f"Phone {phone} deleted from the contact {name}"


@input_error("Give me name and address please.")
def add_address(args, contacts: AddressBook):
    name = args[0]
    # користувач може вводити адресу через пробіл
    # тому обєднуємо решту аргументів в одну строку
    address = ' '.join(map(str, args[1:]))
    rec = contacts.find(name)
    rec.add_address(address)
    return "Address added."


@input_error("Give me name please.")
def del_address(args, contacts: AddressBook):
    name = args[0]
    rec = contacts.find(name)
    rec.remove_address()
    return "Address deleted."

@input_error("No such name in the address book.")
def del_contact(args, contacts: AddressBook):
    name = args[0]
    contacts.delete(name)
    return "Contact deleted."


@input_error("Give me name and birthday please.")
def add_birthday(args, contacts: AddressBook):
    name, bd = args
    rec = contacts.find(name)
    rec.add_birthday(bd)
    return "Birthday added."


@input_error("Give me name please.")
def del_birthday(args, contacts: AddressBook):
    name = args[0]
    rec = contacts.find(name)
    rec.remove_birthday()
    return f"Birthday deleted from the contact {name}"


@input_error("")
def get_birthdays_per_week(contacts: AddressBook):
    return contacts.get_birthdays_per_week()


def print_all(contacts: AddressBook):
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
def show_phone(args, contacts: AddressBook):
    name = args[0]
    return str(contacts.find(name))


@input_error("Give me name and email please.")
def add_email(args, contacts: AddressBook):
    name, email = args
    rec = contacts.find(name)
    rec.add_email(email)
    return "Email added."


@input_error("Give me name please.")
def del_email(args, contacts: AddressBook):
    name = args[0]
    rec = contacts.find(name)
    rec.remove_email()
    return f"Email deleted from the contact {name}"


@input_error("Give me name please.")
def show_birthday(args, contacts: AddressBook):
    name = args[0]
    rec = contacts.find(name)
    if rec.birthday is None:
        return "Birthday doesn't setted."
    return f"{name}'s birthday is {rec.birthday}"


@input_error("Give me argument for search.")
def search(args, contacts: AddressBook):
    search_arg = args[0]
    if len(search_arg) < 3:
        return "Search string must be at least 3 characters long."
    result = contacts.search(search_arg)
    return '\n'.join([str(rec) for rec in result])


@input_error("")
def add_note(book: AddressBook):
    text = input('Note text:')
    index = book.add_note(text)
    return f"Added note with index {index}"


@input_error("Give me note index please.")
def show_note(args, book: AddressBook):
    index = args[0]
    return book.notes.show(index)


@input_error("")
def show_notes(args, book: AddressBook):
    return book.notes.list()


@input_error("Give text to search please.")
def search_notes(args, book: AddressBook):
    search_str = args[0]
    return book.notes.search(search_str)


@input_error("Give me note index please.")
def del_note(args, book: AddressBook):
    index = args[0]
    book.notes.delete(index)
    return f"Note with index {index} deleted"


@input_error("Give me note index please.")
def change_note(args, book: AddressBook):
    index = args[0]
    new_text = input('Enter a new text: ')
    book.notes.change_note(index, new_text)
    return f"Note with index {index} changed"


class PDP11Bot(cmd.Cmd):
    intro = "Welcome to the assistant bot!\n"
    prompt = "(pdp-11) "
    fn = "address-book.dmp"
    book = AddressBook()

    # ---- commands ----
    def do_hello(self, arg):
        "Greeting command"
        print("How can I help you?")

    def do_exit(self, arg):
        "Stop work and good bye"
        self.save_book()
        print("Good bye!")
        return True

    def do_close(self, arg):
        "Stop work and good bye"
        return self.do_exit(arg)

    def do_delete(self, arg):
        "Delete the contact"
        print(del_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_add(self, arg):
        "Adding new contact with phone, email, birthday and address"
        print(add_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_change(self, arg):
        "Change the contact phone"
        print(change_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete(self, arg):
        "Delete contact"
        print(delete_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_add_phone(self, arg):
        "Add phone to the contact"
        print(add_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_change_phone(self, arg):
        "Change phone for the contact"
        print(change_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_phone(self, arg):
        "Delete phone from the contact"
        print(del_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_phone(self, arg):
        "Show contacts phones"
        print(show_phone(self.parse_input(arg), self.book))

    def do_all(self, arg):
        "Print the address book"
        print(print_all(self.book))

    def do_birthdays(self, arg):
        "Print birthday on the next week"
        print(get_birthdays_per_week(self.book))

    def do_add_birthday(self, arg):
        "Add/Change birthday for the contact"
        print(add_birthday(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_birthday(self, arg):
        "Delete birthday from the contact"
        print(del_birthday(self.parse_input(arg), self.book))
        self.save_book()

    def do_show_birthday(self, arg):
        "Show birthday fo the contact"
        print(show_birthday(self.parse_input(arg), self.book))

    def do_add_address(self, arg):
        "Add address to the contact"
        print(add_address(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_address(self, arg):
        "Delete address from the contact"
        print(del_address(self.parse_input(arg), self.book))
        self.save_book()

    def do_add_email(self, arg):
        "Add email to the contact"
        print(add_email(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_email(self, arg):
        "Delete email from the contact"
        print(del_email(self.parse_input(arg), self.book))
        self.save_book()

    def do_search(self, arg):
        "Search data in contacts"
        print(search(self.parse_input(arg), self.book))

    # ---- note commands ----
    def do_add_note(self, arg):
        "Adds a new note"
        print(add_note(self.book))
        self.save_book()

    def do_show_note(self, arg):
        "Shows note by provided index"
        print(show_note(self.parse_input(arg), self.book))

    def do_show_notes(self, arg):
        "Shows all notes"
        print(show_notes(self.parse_input(arg), self.book))

    def do_search_notes(self, arg):
        "Searches for a note which contains a certain string"
        print(search_notes(self.parse_input(arg), self.book))

    def do_delete_note(self, arg):
        "Deletes note by provided index"
        print(del_note(self.parse_input(arg), self.book))
        self.save_book()

    def do_change_note(self, arg):
        "Changes note by provided index"
        print(change_note(self.parse_input(arg), self.book))
        self.save_book()

    # ---- preprocessors ----
    def preloop(self):
        "Init data before starting command prompt loop"
        self.open_address_book()

    def precmd(self, line: str) -> str:
        "Lowering entered commands"
        words = line.split()
        if len(words) > 0:
            words[0] = words[0].lower()
        return super().precmd(' '.join(words))

    def completenames(self, text: str, *ignored) -> list[str]:
        "Lowering inputed command's chars"
        return super().completenames(text.lower(), *ignored)

    # ---- internal logic ----
    def open_address_book(self):
        "Loading the adress book from file if exists"
        self.book = AddressBook()
        try:
            with open(self.fn, "rb") as file:
                self.book = pickle.load(file)
        except FileNotFoundError:
            pass

    def save_book(self):
        "Dump AdressBook to file"
        with open(self.fn, "wb") as fh:
            pickle.dump(self.book, fh)

    def parse_input(self, arg: str):
        "Parse input line as tuple"
        return arg.split()


if __name__ == "__main__":
    PDP11Bot().cmdloop()
