from datetime import datetime

from field import Field


class Birthday(Field):
    def __init__(self, value: str):
        # Перевірка формату дати та збереження як рядка
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
