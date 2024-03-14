import unittest
from datetime import datetime
from addressbook import *

class TestAddressBook(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()