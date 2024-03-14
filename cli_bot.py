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
            except IncorrectFormatException as err:
                return err
            except ValueError:
                return msg 
            except IndexError:
                return msg 
            except KeyError as name:
                return f"Contact with name {name} not found"
        
        return inner
    return decorator

@input_error("Give me name and phone please.")
def add_contact(args, contacts: AddressBook):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error("Give me name and new phone please.")
def change_contact(args, contacts: AddressBook):
    name, no = args
    rec = contacts.find(name)
    rec.change_phone(no)
    return "Contact updated."

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

@input_error("Give me name please.")
def show_birthday(args, contacts: AddressBook):
    name = args[0]
    rec = contacts.find(name)
    if rec.birthday is None:
        return "Birthday don't setted."
    return f"{name}'s birthday is {rec.birthday}"

@input_error("Give me argument for search.")
def search(args, contacts: AddressBook):
    search_arg = args[0]
    if len(search_arg) < 3:
        return "Search string must be at least 3 characters long."
    result = contacts.search(search_arg) 
    return '\n'.join([str(rec) for rec in result])

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
        print("Good bye!")
        self.close_book()
        return True
    
    def do_close(self, arg):
        "Stop work and good bye"
        return self.do_exit(arg)
    
    def do_delete(self, arg):
        "Delete the contact"
        print(del_contact(self.parse_input(arg), self.book))
    
    def do_add(self, arg):
        "Adding new contact with phone"
        print(add_contact(self.parse_input(arg), self.book))

    def do_change(self, arg):
        "Change the contact phone"
        print(change_contact(self.parse_input(arg), self.book))

    def do_phone(self, arg):
        "Show contacts phones"
        print(show_phone(self.parse_input(arg), self.book))

    def do_all(self, arg):
        "Print the address book"
        print(print_all(self.book))

    def do_birthdays(self, arg):
        "Print birthday on the next week"
        print(self.book.get_birthdays_per_week())

    def do_add_birthday(self, arg):
        "Add/Change birthday for the contact"
        print(add_birthday(self.parse_input(arg), self.book))

    def do_show_birthday(self, arg):
        "Show birthday fo the contact"
        print(show_birthday(self.parse_input(arg), self.book))
        
    def do_add_address(self, arg):
        "Add address for the contact"
        print(add_address(self.parse_input(arg), self.book))
        
    def do_delete_address(self, arg):
        "Delete the contact address"
        print(del_address(self.parse_input(arg), self.book))

    def do_search(self, arg):
        "Search data in contacts"
        print(search(self.parse_input(arg), self.book))    

    # ---- preprocessors ----
    def preloop(self):
        with open(self.fn, "rb") as fh:
            self.book = pickle.load(fh)

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
    def close_book(self):
        "Dump AdressBook to file"
        with open(self.fn, "wb") as fh:
            pickle.dump(self.book, fh)

    def parse_input(self, arg: str):
        "Parse input line as tuple"
        return arg.split()


if __name__ == "__main__":
    PDP11Bot().cmdloop()
