from exceptions import ValidationError
import functools


def validate(*validate_fns):
    def outer_wrapper(func):
        def inner_wrapper(*args, **kwargs):  # args = self, number
            for fn in validate_fns:
                fn(args[1])  # setter-Element (dh. der Wert, der gesetzt wird)
            return func(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper


def telephone_number(number):
    if len(number) < 5:
        raise ValidationError("Diese Nummer hat zu wenig Zahlen")

    if len(number) > 20:
        raise ValidationError("Diese Nummer ist zu lang")
