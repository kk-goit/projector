import unittest
import random

from santashelper.classes.Record import Record
from santashelper.classes.Fields import IncorrectFormatException, NotFoundError


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
        self.record.add_birthday("01.01.2014")
        self.assertIsNotNone(self.record.birthday)
        self.assertEqual(str(self.record.birthday), "01.01.2014")
    
    def test_add_birthday_with_validation_error(self):
        with self.assertRaises(IncorrectFormatException) as context:
            self.record.add_birthday("13.13.23233")
        self.assertEqual(str(context.exception), "Birthday must be in format DD.MM.YYYY")
        
        
    def test_remove_birthday(self):
        self.record.add_birthday("01.01.2016")
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
        self.record.add_birthday("01.01.2010")
        
        expected_str = "Contact name: John Doe, phones: 1234567890; 9876543210, email: john.doe@example.com, address: 123 Main St, City, Country, birthday: 01.01.2010"
        self.assertEqual(str(self.record), expected_str)
    
    def test_str_representation2(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")
        
        expected_str = "Contact name: John Doe, phones: 1234567890; 9876543210"
        self.assertEqual(str(self.record), expected_str)

    def test_add_wishlist_items(self):
        items = ['iPhone', 'Nike Air Force', 'Watch']
        self.record.add_wishlist_items(items)
        self.assertEqual(len(self.record.wishlist), len(items))
        for item, wishlist_item in zip(items, self.record.wishlist):
            self.assertEqual(wishlist_item, item)

    def test_add_wishlist_items_empty_list(self):
        items = []
        self.record.add_wishlist_items(items)
        self.assertEqual(len(self.record.wishlist), 0)

    def test_show_wishlist(self):
        items = ['iPhone', 'Nike Air Force', 'Watch']
        self.record.add_wishlist_items(items)
        expected_str = ", ".join(items)
        self.assertEqual(self.record.show_wishlist(), expected_str)

    def test_show_wishlist_empty(self):
        with self.assertRaises(NotFoundError):
            self.record.show_wishlist()

    def test_generate_wishlist(self):
        self.record.generate_wishlist("John Doe")
        self.assertEqual(len(self.record.wishlist), 1)
        top_10_items = ['iPhone', 'Nike Air Force', 'Watch', 'Lego', 'Barbie doll', 'PS5', 'Drone', 'Disney Toy', 'Bike', 'Board Game']
        self.assertIn(self.record.wishlist[0], top_10_items)

    def test_generate_wishlist_existing(self):
        items = ['iPhone', 'Nike Air Force', 'Watch']
        self.record.add_wishlist_items(items)
        with self.assertRaises(IncorrectFormatException):
            self.record.generate_wishlist("John Doe")    