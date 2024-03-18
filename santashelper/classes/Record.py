import random

from collections import UserDict, defaultdict
from .Fields import *

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.wishlist = []

    def add_birthday(self, date: str):
        self.birthday = Birthday(date)

    def remove_birthday(self):
        self.birthday = None

    def add_address(self, address: str):
        self.address = Address(address)

    def remove_address(self):
        self.address = None

    def add_email(self, email: str):
        self.email = Email(email)

    def remove_email(self):
        self.email = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str, default=None):
        for itm in self.phones:
            if str(itm) == phone:
                return itm
        return default

    def remove_phone(self, phone: str):
        itm = self.find_phone(phone)
        if itm:
            self.phones.remove(itm)

    def edit_phone(self, old, new):
        phone = self.find_phone(old)
        if phone:
            phone.value = new

    def change_phone(self, phone: str):
        if len(self.phones) > 0:
            self.phones[0] = Phone(phone)
        else:
            self.add_phone(phone)

    def add_wishlist_items(self, items):
        self.wishlist = [WishlistItem(item) for item in items]

    def show_wishlist(self):
        if not self.wishlist:
            raise NotFoundError("No items in wishlist")
        return ', '.join([str(item) for item in self.wishlist])

    def generate_wishlist(self, name):
        if self.wishlist:
            raise IncorrectFormatException("Wishlist is already exist")
        top_10_items = ['iPhone', 'Nike Air Force', 'Watch', 'Lego', 'Barbie doll', 'PS5', 'Drone', 
        'Disney Toy', 'Bike', 'Board Game']
        random.shuffle(top_10_items)
        self.wishlist = [WishlistItem(top_10_items[0])]             

    def __str__(self):
        res = f"Contact name: {self.name}"
        res += f", phones: {'; '.join(p.value for p in self.phones)}" if len(self.phones) else ""
        res += f", email: {self.email}" if self.email else ""
        res += f", address: {self.address}" if self.address else ""
        res += f", birthday: {self.birthday}" if self.birthday else ""
        return res

