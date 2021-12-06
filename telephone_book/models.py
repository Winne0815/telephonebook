from datetime import datetime
from config import Config
from exceptions import (EntriesExceededException, ValidationError)
import validators as val
import arrow


class Entry:
    """ein einzelner Eintrag in einem Telefonbuch"""

    def __init__(self, name) -> None:

        if len(name) < 2:
            raise ValidationError(
                "Der Username darf nicht kleiner als 2 Zeichen sein")
        self.__name = name
        self.__phone_number = None
        self.__created_at = datetime.now()

    @property
    def name(self):
        return self.__name

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    @val.validate(val.telephone_number)
    def phone_number(self, number):
        self.__phone_number = number

    def __repr__(self) -> str:
        return f"Entry({self.__name})"

    def __str__(self) -> str:
        return f"{self.__name}: {self.__phone_number}"


class TelephoneBook:
    def __init__(self, name, config) -> None:
        self.__name = name
        self.__entries = {}
        self.__config = config

    def get_entry(self, name):
        """einen User-Entry aus der Liste holen"""
        try:
            return self.__entries[name]
        except KeyError:
            raise ValueError(
                f"Der Name {name} befindet sich nicht im Telefonbuch")

    def remove_entry(self, name: str) -> Entry:
        try:
            return self.__entries.pop(name)
        except KeyError:
            raise ValidationError(
                f"Der Name {name} befindet sich nicht im Telefonbuch")

    def add(self, entry: Entry) -> None:

        if entry.name in self.__entries:
            # ValueError wird später zu InvalidUserName
            raise ValidationError(
                "Dieser Name befindet sich bereits im Telefonbuch!")

        if len(self.__entries) >= self.__config["max_entries"]:
            raise EntriesExceededException(
                "maximale Anzahl an Einträgen erreicht!"
            )

        self.__entries.update(
            {
                entry.name: entry
            }
        )

    def get_entries(self, **kwargs) -> dict:
        """Liste Telefonbuch-Einträge"""
        return self.__entries

    def __add__(self, entry: Entry):
        """Telephonebook + Eintrag fügt einen neuen Eintrag ins Telefonbuch"""
        if not isinstance(entry, Entry):
            raise NotImplementedError("das muss ein Entry-Objekt sein")
        self.add(entry)
        return self

    def __sub__(self, entry: Entry):
        """Telephonebook + Eintrag fügt einen neuen Eintrag ins Telefonbuch"""
        if not isinstance(entry, Entry):
            raise NotImplementedError("das muss ein Entry-Objekt sein")
        self.remove_entry(entry.name)
        return self

    def __len__(self):
        return len(self.__entries)

    def __iter__(self):
        return iter(self.__entries)


if __name__ == '__main__':
    donald = Entry("Donald")
    klaus = Entry("Klaus")
    dieter = Entry("Dieter")
    donald.phone_number = "0049 43 2342 243 23"

    my_book = TelephoneBook("mein privates Telefonbuch", Config.config())
    my_book.add(dieter)
    my_book = my_book + donald
    my_book.add(klaus)

    print("Länge von book", len(my_book))
    for entry in my_book:
        print("Entry =>,", entry)

    # my_book.add(dieter)  # geht nicht, weil in config.json nur 2
    # Einträge erlaubt sind
    entries = my_book.get_entries()
    print("Aktuelle Einträge im Telefonbuch:", entries)
    for name, obj in entries.items():
        print(name, obj.phone_number)

    my_book = my_book - klaus

    entries = my_book.get_entries()
    print("Aktuelle Einträge im Telefonbuch:", entries)
    for name, obj in entries.items():
        print(name, obj.phone_number)

    # my_book.get_entry("Otto")
    print("Donald wurde gelöscht: ", my_book.remove_entry("Donald"))
