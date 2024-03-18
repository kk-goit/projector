import unittest
from unittest.mock import MagicMock
from santashelper.classes.HelpWorker import HelpWorker
from santashelper.classes.AddressBook import AddressBook
from santashelper.classes.Fields import IncorrectFormatException
from santashelper.classes.Record import Record

class TestHelpWorker(unittest.TestCase):

    def setUp(self):
        self.worker = HelpWorker()
        self.book = AddressBook()

    def test_add_contact(self):
        args = ["John Doe", "1234567890"]
        self.worker.add_contact(args, self.book)
        self.assertTrue("John Doe" in [rec.name.value for rec in self.book.get_all_contacts()])

    def test_add_contact_invalid_info(self):
        self.worker.add_contact(["John Doe"], self.book)
        try:
            self.book.get_all_contacts()
        except KeyError as e:
            self.assertEqual(e.args[0], "No contacts in address book")
    
    def test_add_single_contact(self):
        self.worker.add_contact(["John Doe", '1231231233'], self.book)
        self.assertIn("John Doe", [rec.name.value for rec in self.book.get_all_contacts()])
        
    def test_add_contact_valid_phone(self):
        # Перевірка додавання контакту з коректним номером телефону
        args = ["John Doe", "1234567890"]
        self.assertEqual(self.worker.add_contact(args, self.book), "Contact added.")
        self.assertIn("John Doe", [rec.name.value for rec in self.book.get_all_contacts()])

    def test_add_contact_valid_email(self):
        # Перевірка додавання контакту з коректною електронною адресою
        args = ["John Doe", "john@example.com"]
        self.assertEqual(self.worker.add_contact(args, self.book), "Contact added.")
        self.assertIn("John Doe", [rec.name.value for rec in self.book.get_all_contacts()])

    def test_add_contact_valid_birthday(self):
        # Перевірка додавання контакту з коректною датою народження
        args = ["John Doe", "01.01.2010"]
        self.assertEqual(self.worker.add_contact(args, self.book), "Contact added.")
        self.assertIn("John Doe", [rec.name.value for rec in self.book.get_all_contacts()])
    
class TestHelpWorkerChangeContact(unittest.TestCase):
    def setUp(self):
        self.worker = HelpWorker()
        self.book = AddressBook()
        self.worker.add_contact(["John Doe", "1234567890"], self.book)

    def test_change_contact_valid_phone(self):
        # Перевірка зміни номеру телефону
        args = ["John Doe", "0987654321"]
        self.assertEqual(self.worker.change_contact(args, self.book), "Contact updated.")
        self.assertEqual(self.book.find("John Doe").phones[0], "0987654321")

    def test_change_contact_invalid_phone(self):
        # Перевірка спроби зміни на некоректний номер телефону
        args = ["John Doe", "invalid_phone"]
        try:
            self.worker.change_contact(args, self.book)
        except IncorrectFormatException as e:
            self.assertEqual(e.args[0], "Phone must have 10 digits")
        self.assertEqual(self.book.find("John Doe").phones[0], "1234567890")  # Перевіряємо, що номер залишився незмінним

    def test_change_contact_not_found(self):
        # Перевірка спроби зміни контакту, який не знайдено
        args = ["Jane Smith", "0987654321"]
        try:
            self.worker.change_contact(args, self.book)
        except KeyError as e:
            self.assertEqual(e.args[0], "Contact with name Jane Smith not found")
    
    def test_change_contact_missing_args(self):
        # Перевірка спроби зміни контакту без передачі аргументів
        try:
            self.worker.change_contact([], self.book)
        except IndexError as e:
            self.assertEqual(e.args[0], "Give me name and new phone please.")

class TestHelpWorkerDeleteContact(unittest.TestCase):
    def setUp(self):
        self.worker = HelpWorker()
        self.book = AddressBook()
    
    def test_delete_contact(self):
        rec = Record("John Doe")
        self.book.add_record(rec)
        self.worker.delete_contact(["John Doe"], self.book)
        self.assertNotIn(rec, self.book.values())

    def test_delete_contact_not_found(self):
        expected_output = "Contact with name John not found"
        try:
            self.worker.delete_contact(["John"], self.book)
        except KeyError as e:
            self.assertEqual(str(e), expected_output)

class TestBirthdayValidation(unittest.TestCase):
    def setUp(self):
        self.worker = HelpWorker()
        self.book = AddressBook()

    def test_validate_age_invalid(self):
        self.worker.add_contact(["Lucas"], self.book)
        try:
            self.worker.add_birthday(["Lucas", "01.01.2000"], self.book)
        except IncorrectFormatException as e:    
            self.assertEqual(e.args[0], "Alas, it seems this little one has outgrown their childlike wonder")

if __name__ == "__main__":
    unittest.main()