from address_book import AddressBook
from record import Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            # або стандартний текст, або текст з exception
            return str(e)
        except IndexError:
            return "Not enough arguments."
    return inner


def parse_input(user_input: str):
    parts = user_input.split()
    command = parts[0].lower() if parts else ""
    return command, *parts[1:]


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Phone changed."


@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    phones = [p.value for p in record.phones]
    return ", ".join(phones) if phones else "No phones."


@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    lines = []
    for record in book.data.values():
        phones = ", ".join(p.value for p in record.phones) if record.phones else "no phones"
        bday = record.birthday.value if record.birthday else "no birthday"
        lines.append(f"{record.name.value}: {phones}; birthday: {bday}")
    return "\n".join(lines)


# НОВІ ХЕНДЛЕРИ

@input_error
def add_birthday(args, book: AddressBook):
    """
    add-birthday [ім'я] [дата народження в форматі DD.MM.YYYY]
    """
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        # зазвичай в ДЗ вимагають працювати тільки з існуючими контактами;
        # якщо хочеш, можна створювати новий Record, але за замовчуванням: помилка
        record = Record(name)
        book.add_record(record)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """
    show-birthday [ім'я]
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday is not set."
    return record.birthday.value


@input_error
def birthdays(args, book: AddressBook):
    """
    birthdays
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    lines = []
    for item in upcoming:
        lines.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(lines)