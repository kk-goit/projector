import unittest

from santashelper.classes.Record import Record
from santashelper.classes.Fields import IncorrectFormatException


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("John Doe")
        
    def test_add_phone(self):
        self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "1234567890")
    
    def test_add_phone_with_validation_error(self):
        with self.assertRaises(IncorrectFormatException) as context:
            self.record.add_phone("12345")
        self.assertEqual(str(context.exception), "Phone must have 10 digits")
        
    def test_remove_phone(self):
        self.record.add_phone("1234567890")
        self.record.remove_phone("1234567890")
        self.assertEqual(len(self.record.phones), 0)
        
    def test_edit_phone(self):
        self.record.add_phone("1234567890")
        self.record.edit_phone("1234567890", "9876543210")
        self.assertEqual(self.record.phones[0].value, "9876543210")
        
    def test_add_birthday(self):
        self.record.add_birthday("01.01.2000")
        self.assertIsNotNone(self.record.birthday)
        self.assertEqual(str(self.record.birthday), "01.01.2000")
    
    def test_add_birthday_with_validation_error(self):
        with self.assertRaises(IncorrectFormatException) as context:
            self.record.add_birthday("13.13.23233")
        self.assertEqual(str(context.exception), "Birthday must be in format DD.MM.YYYY")
        
        
    def test_remove_birthday(self):
        self.record.add_birthday("01.01.2000")
        self.record.remove_birthday()
        self.assertIsNone(self.record.birthday)
        
    def test_add_email(self):
        self.record.add_email("john.doe@example.com")
        self.assertIsNotNone(self.record.email)
        self.assertEqual(str(self.record.email), "john.doe@example.com")
        
    def test_add_email_with_validation_error(self):
        with self.assertRaises(IncorrectFormatException) as context:
            self.record.add_email("invalid_email_address")
        self.assertEqual(str(context.exception), "Incorrect email format")
        
    def test_remove_email(self):
        self.record.add_email("john.doe@example.com")
        self.record.remove_email()
        self.assertIsNone(self.record.email)
        
    def test_str_representation(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")
        self.record.add_email("john.doe@example.com")
        self.record.add_address("123 Main St, City, Country")
        self.record.add_birthday("01.01.2000")
        
        expected_str = "Contact name: John Doe, phones: 1234567890; 9876543210, email: john.doe@example.com, address: 123 Main St, City, Country, birthday: 01.01.2000"
        self.assertEqual(str(self.record), expected_str)
    
    def test_str_representation2(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")
        
        expected_str = "Contact name: John Doe, phones: 1234567890; 9876543210"
        self.assertEqual(str(self.record), expected_str)