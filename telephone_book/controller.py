from models import TelephoneBook, Entry
from exceptions import (EntriesExceededException,
                        ValidationError)

MSG = {
    "welcome_screen": (
        "Bitte wählen:\n"
        "add: neuen User anlegen\n",
    ),
    "add_name": "Username eingeben: ",
    "add_number": "Telefonnummer eingeben: ",
}


class Controller:
    def __init__(self, telephone_book: TelephoneBook):
        """Controller Method

        Args:
            telephone_book (TelephoneBook)
        """
        self.telephone_book = telephone_book
        self.operations = {
            "add": self.add,
            "delete": self.delete
        }

    def delete(self):

        if not self.telephone_book.get_entries():
            raise ValueError("Das Telefonbuch ist leer")

        """stelle dem user Interface für die Eingabe eines Namens zur Verfügung.
        Lösche den entsprechenden Eintrag aus dem Telefonbuch"""
        name = input(MSG.get("add_name"))
        self.telephone_book.remove_entry(name)
        print(f"User {name} wurde erfolgreich gelöscht")

    def add(self):

        # Username wird eingegeben. Falls Fehler (Name-Error, doppelter Name)
        # wird Loop nicht beeendet
        while True:
            name = input(MSG.get("add_name"))
            try:
                entry = Entry(name)
                self.telephone_book.add(entry)
                break
            except ValidationError as e:
                print(e)
            except EntriesExceededException as e:
                print(e)
                return

        while True:
            number = input(MSG.get("add_number"))
            try:
                entry.phone_number = number
                print("User wurde erfolgreich angelegt!")
                break
            except ValidationError as e:
                print(e)

    def controller(self, user_input: list) -> None:
        """user input auf Operation mappen
        userinput: command, *args, zb. add
        """
        try:
            command, *args = user_input
            try:
                operation = self.operations[command.lower()]
            except KeyError:
                raise NotImplementedError(
                    "diese Funktion ist nicht implementiert"
                )
            operation()
        except (ValueError, ValidationError) as e:
            print(f"Fehler: {e}")
        except NotImplementedError as e:
            # in LOG datei Schreiben!
            print(e)

    def handle_user_input(self):
        """Usereingabe:
        add 
        """
        user_input = input(MSG.get("welcome_screen")).split()
        self.controller(user_input)
