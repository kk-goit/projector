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

@input_error("Give me name and birthday please.")
def add_birthday(args, contacts: AddressBook):
    name, bd = args
    rec = contacts.find(name)
    rec.add_birthday(bd)
    return "Birthday added."

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

class PDP11Bot(cmd.Cmd):
    intro = "Welcome to the assistant bot!\n"
    prompt = "(pdp-11) "
    fn = "address-book.dmp"
    book = None

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
        print(self.book)

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

    def close_book(self):
        "Dump AdressBook to file"
        with open(self.fn, "wb") as fh:
            pickle.dump(self.book, fh)

    def parse_input(self, arg: str):
        "Parse input line as tuple"
        return arg.split()


if __name__ == "__main__":
    PDP11Bot().cmdloop()
