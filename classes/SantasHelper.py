import pickle, cmd
from classes.HelpWorker import *
from classes.AddressBook import *

class SantasHelper(cmd.Cmd):
    intro = "Welcome to the Santa's Helper!\n"
    prompt = "(elf) "
    doc_header = "My commands (type help <topic> for more info):"

    fn = "address-book.dmp"
    book = AddressBook()
    worker = HelpWorker()

    # ---- commands ----
    def do_hello(self, arg):
        "Greeting command"
        print("How can I help you?")
        self.do_help(None)

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
        print(self.worker.delete_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_add(self, arg):
        "Adding new contact with phone, email, birthday and address"
        print(self.worker.add_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_change(self, arg):
        "Change the contact phone"
        print(self.worker.change_contact(self.parse_input(arg), self.book))
        self.save_book()

    def do_add_phone(self, arg):
        "Add phone to the contact"
        print(self.worker.add_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_change_phone(self, arg):
        "Change phone for the contact"
        print(self.worker.change_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_show(self, arg):
        "Show contact from address book"
        print(self.worker.show(self.parse_input(arg), self.book))

    def do_delete_phone(self, arg):
        "Delete phone from the contact"
        print(self.worker.del_phone(self.parse_input(arg), self.book))
        self.save_book()

    def do_phone(self, arg):
        "Show contacts phones"
        print(self.worker.show_phone(self.parse_input(arg), self.book))

    def do_all(self, arg):
        "Print the address book"
        print(self.worker.print_all(self.book))

    def do_birthdays(self, arg):
        "Print birthday on the next week"
        print(self.worker.get_birthdays_per_week(self.book))

    def do_add_birthday(self, arg):
        "Add/Change birthday for the contact"
        print(self.worker.add_birthday(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_birthday(self, arg):
        "Delete birthday from the contact"
        print(self.worker.del_birthday(self.parse_input(arg), self.book))
        self.save_book()

    def do_show_birthday(self, arg):
        "Show birthday fo the contact"
        print(self.worker.show_birthday(self.parse_input(arg), self.book))

    def do_add_address(self, arg):
        "Add address to the contact"
        print(self.worker.add_address(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_address(self, arg):
        "Delete address from the contact"
        print(self.worker.del_address(self.parse_input(arg), self.book))
        self.save_book()

    def do_add_email(self, arg):
        "Add email to the contact"
        print(self.worker.add_email(self.parse_input(arg), self.book))
        self.save_book()

    def do_delete_email(self, arg):
        "Delete email from the contact"
        print(self.worker.del_email(self.parse_input(arg), self.book))
        self.save_book()

    def do_search(self, arg):
        "Search data in contacts"
        print(self.worker.search(self.parse_input(arg), self.book))

    # ---- note commands ----
    def do_add_note(self, arg):
        "Adds a new note"
        print(self.worker.add_note(self.book))
        self.save_book()

    def do_show_note(self, arg):
        "Shows note by provided index"
        print(self.worker.show_note(self.parse_input(arg), self.book))

    def do_show_notes(self, arg):
        "Shows all notes"
        print(self.worker.show_notes(self.parse_input(arg), self.book))

    def do_search_notes(self, arg):
        "Searches for a note which contains a certain string"
        print(self.worker.search_notes(self.parse_input(arg), self.book))

    def do_delete_note(self, arg):
        "Deletes note by provided index"
        print(self.worker.del_note(self.parse_input(arg), self.book))
        self.save_book()

    def do_change_note(self, arg):
        "Changes note by provided index"
        print(self.worker.change_note(self.parse_input(arg), self.book))
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
        except (FileNotFoundError, ModuleNotFoundError):
            pass

    def save_book(self):
        "Dump AdressBook to file"
        with open(self.fn, "wb") as fh:
            pickle.dump(self.book, fh)

    def parse_input(self, arg: str):
        "Parse input line as tuple"
        return arg.split()

