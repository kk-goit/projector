import unittest

from santashelper.classes.Record import Record
from santashelper.classes.AddressBook import AddressBook
from santashelper.classes.Fields import IncorrectFormatException

class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()
        self.record1 = Record("John Doe")
        self.record2 = Record("Jane Smith")
        
    def test_add_record(self):
        self.address_book.add_record(self.record1)
        self.assertEqual(len(self.address_book), 1)
        
    def test_find(self):
        self.address_book.add_record(self.record1)
        found_record = self.address_book.find("John Doe")
        self.assertEqual(found_record, self.record1)
        
    def test_delete(self):
        self.address_book.add_record(self.record1)
        self.address_book.delete("John Doe")
        self.assertEqual(len(self.address_book), 0)
        
    def test_delete_unexisting(self):
        self.address_book.add_record(self.record1)
        self.address_book.delete("John Doe")
        self.assertEqual(len(self.address_book), 0)
        
    def test_str_empty_address_book(self):
        expected_output = "No contacts in address book"
        self.assertEqual(str(self.address_book), expected_output)
        
    def test_str_one_record(self):
        self.address_book.add_record(self.record1)
        expected_output = "Contact name: John Doe"
        self.assertEqual(str(self.address_book), expected_output)
        
    def test_str_multiple_records(self):
        self.address_book.add_record(self.record1)
        self.address_book.add_record(self.record2)
        expected_output = "Contact name: John Doe\nContact name: Jane Smith"
        self.assertEqual(str(self.address_book), expected_output)
        
    def test_str_one_record_with_phone(self):
        self.record1.add_phone("1234567890")
        self.address_book.add_record(self.record1)
        expected_output = "Contact name: John Doe, phones: 1234567890"
        self.assertEqual(str(self.address_book), expected_output)
        
    def test_str_one_record_with_address(self):
        self.record1.add_address("123 Main St")
        self.address_book.add_record(self.record1)
        expected_output = "Contact name: John Doe, address: 123 Main St"
        self.assertEqual(str(self.address_book), expected_output)
        
    def test_str_one_record_with_email(self):
        self.record1.add_email("john@example.com")
        self.address_book.add_record(self.record1)
        expected_output = "Contact name: John Doe, email: john@example.com"
        self.assertEqual(str(self.address_book), expected_output)
        
    # TODO implement
    def test_get_birthdays_per_week(self):
        pass
        
        # Add assertions for birthdays per week
        
class TestSearchAddressBook(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()
        record1 = Record("John Doe")
        record1.add_phone("1234567890")
        record1.add_birthday("01.01.1990")
        record1.add_email("john.doe@example.com")
        record1.add_address("123 Main St")
        self.address_book.add_record(record1)

        record2 = Record("Alice Smith")
        record2.add_phone("9876543210")
        record2.add_email("alice.smith@example.com")
        record2.add_address("456 Elm St")
        self.address_book.add_record(record2)

        record3 = Record("Bob Johnson")
        record3.add_phone("5555555555")
        record3.add_birthday("12.12.1980")
        self.address_book.add_record(record3)

    def test_search_with_name(self):
        search_results = self.address_book.search("Doe")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "John Doe")

    def test_search_with_phone(self):
        search_results = self.address_book.search("123")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "John Doe")

    def test_search_with_birthday(self):
        search_results = self.address_book.search("1990")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "John Doe")

    def test_search_with_email(self):
        search_results = self.address_book.search("john.doe@example.com")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "John Doe")

    def test_search_with_address(self):
        search_results = self.address_book.search("Main St")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "John Doe")

    def test_search_case_insensitive(self):
        search_results = self.address_book.search("ALICE")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name.value, "Alice Smith")

    def test_search_no_results(self):
        with self.assertRaises(IncorrectFormatException):
            self.address_book.search("XYZ")
