""" 
Hauptdatei des Programms
"""
from controller import Controller
from models import TelephoneBook
from config import Config


def main():
    display_manager = Controller(
        TelephoneBook("mein privates Telefonbuch", Config.config()),

    )

    while True:
        display_manager.handle_user_input()


if __name__ == '__main__':
    main()
