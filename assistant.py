# Консольний бот-помічник (книга контактів)
# Запуск:  python assistant.py
# Або імпорт:  from assistant import assistant_main

from address_book import AddressBook, Record


# Парсер команд користувача
def parse_input(user_input):
    # Розбиває введений користувачем рядок на команду та аргументи.
    # Наприклад: "add Petro 12345"
    # -> команда 'add', аргументи ['Petro', '12345']

    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, *args


# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError:
            # Контакт не знайдено
            return "Contact not found."

        except ValueError as e:
            # Валідація телефону / дати або неправильний формат команди
            msg = str(e)
            return msg or "Give me name and phone please."

        except IndexError:
            # Коли користувач передав недостатньо аргументів
            return "Enter the argument for the command"

    return inner


# Обробники команд

@input_error
def add_contact(args, book):
    # Команда:  add <name> <phone>
    # Додає новий контакт або додає телефон до існуючого.

    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    # Команда:  change <name> <new_phone>
    # Змінює телефон у контакті (або додає, якщо не було).

    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, new_phone = args

    record = book.find(name)
    if record is None:
        raise KeyError

    # Якщо в контакта немає телефонів — додаємо новий
    if not record.phones:
        record.add_phone(new_phone)
    else:
        old_phone = record.phones[0].value
        record.edit_phone(old_phone, new_phone)

    return "Contact updated."


@input_error
def show_phone(args, book):
    # Команда:  phone <name>
    # Повертає телефони контакту.

    if not args:
        raise IndexError

    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError

    if not record.phones:
        return "No phones."

    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    # Команда:  all
    # Показує всі контакти, відсортовані за імʼям.
    # args тут не використовуються, але лишаємо для єдиного інтерфейсу.

    if not book.data:
        return "No contacts."

    names = sorted(book.data.keys())
    lines = []
    for name in names:
        record = book.find(name)
        lines.append(str(record))

    return "\n".join(lines)


@input_error
def add_birthday(args, book):
    # Команда:  add-birthday <name> <DD.MM.YYYY>
    # Додає або оновлює день народження контакту.

    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")

    name, birthday = args

    record = book.find(name)
    if record is None:
        # У ДЗ допускається створення контакту, якщо його ще нема
        record = Record(name)
        book.add_record(record)

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    # Команда:  show-birthday <name>
    # Повертає дату народження контакту.

    if not args:
        raise IndexError

    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError

    if record.birthday is None:
        return "Birthday is not set."

    return record.birthday.value


@input_error
def birthdays(args, book):
    # Команда:  birthdays
    # Повертає список контактів, яких потрібно привітати впродовж тижня.
    # args не використовуються.

    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."

    lines = []
    for item in upcoming:
        lines.append(f"{item['name']}: {item['congratulation_date']}")

    return "\n".join(lines)


# Основна логіка роботи бота (для запуску без main.py з ДЗ)
def main():
    # Створюємо порожню адресну книгу
    book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # Команди виходу
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


# Точка входу для імпорту
def assistant_main():
    main()


if __name__ == "__main__":
    main()
