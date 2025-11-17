from fields import Name, Phone, Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # Поле дня народження (необов'язкове)

    def add_phone(self, phone):
        #Додати новий телефон до контакту.
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        #Видалити телефон зі списку. Повертає True/False.
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        #Змінити існуючий телефон на новий.
        for p in self.phones:
            if p.value == old_phone:
                p._validate(new_phone)
                p.value = new_phone
                return True
        raise ValueError("Phone to edit not found")

    def find_phone(self, phone):
        #Повертає обʼєкт Phone або None.
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        #Додати/оновити день народження контакту.
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        bday_str = self.birthday.value if self.birthday else "no birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"
