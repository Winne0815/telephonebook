import sys
import os
import unittest

testdir = os.path.dirname(__file__)
srcdir = '../telephone_book'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from telephone_book.models import Entry, TelephoneBook


class TestTelephoneBook(unittest.TestCase):
    def setUp(self) -> None:
        self.telephone_book = TelephoneBook("Testbuch", {"max_entries": 3})

        entry_1 = Entry("KLaus")
        entry_1.phone_number = "8723878"

        entry_2 = Entry("Otto")
        entry_2.phone_number = "8723878"

        entry_3 = Entry("Peter")
        entry_3.phone_number = "8723878"

        self.telephone_book.add(entry_1)
        self.telephone_book.add(entry_2)
        self.telephone_book.add(entry_3)

    def test_number_of_entries(self):
        """befinden sich 3 Einträge im Telefonbuch"""
        self.assertEqual(len(self.telephone_book.get_entries()),
                         3, "Es fehlen Testobjekte")

    def test_delete_entry_from_book(self):
        """test"""
        entry = self.telephone_book.remove_entry("Otto")
        self.assertEqual(entry.name, "Otto",
                         "Das ist nicht das richtige Entry Objekt")
        self.assertEqual(len(self.telephone_book.get_entries()),
                         2, "Objekt wurde nicht gelöscht")

    def test_get_entry_with_valid_username(self):
        """test2"""
        entry = self.telephone_book.get_entry("Otto")
        self.assertEqual(entry.name, "Otto", "Passt nicht")
        self.assertTrue(isinstance(entry, Entry))

    def test_get_entry_with_invalid_username(self):
        """test"""
        with self.assertRaises(Exception):
            self.telephone_book.get_entry("Uwe")

    def test_exceed_max_number_of_entries(self):
        """test"""
        entry_4 = Entry("Uwe")
        entry_4.phone_number = "123456"
        with self.assertRaises(Exception):
            self.telephone_book.add(entry_4)

    def test_len(self):
        """test"""
        self.assertEqual(len(self.telephone_book),
                         3, "Es fehlen Testobjekte")

    def test_iter_implementation(self):
        """test"""
        it = iter(self.telephone_book)
        with self.assertRaises(StopIteration):
            next(it)
            next(it)
            next(it)
            next(it)


class TestEntry(unittest.TestCase):

    def setUp(self) -> None:
        """wird VOR jeder Test-Methode aufgerufen"""
        self.entry = Entry(name="Klaus")
        self.entry.phone_number = "0049 37 234 234"

    def test_create_entry_object_with_invalid_username(self):
        with self.assertRaises(Exception):
            Entry(name="k")

    def test_valid_telephone_number(self):
        """testen, ob eingetragene Telefonnummer stimmt"""
        self.assertEqual(self.entry.phone_number, "0049 37 234 234",
                         "Die Telefonnummer wurde falsch eingetragen")

    def test_raise_exception_if_invalid_telephone_number(self):
        """testen, ob bei einer invaliden Nummer eine Exception ausgelöst wird"""
        with self.assertRaises(Exception):
            self.entry.phone_number = "343"

    def test_raise_exception_if_long_telephone_number(self):
        """testen, ob bei einer invaliden Nummer eine Exception ausgelöst wird"""
        with self.assertRaises(Exception):
            self.entry.phone_number = "3431213132132132132131323234"
