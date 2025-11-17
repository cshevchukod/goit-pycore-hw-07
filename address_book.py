from collections import UserDict
from datetime import datetime, timedelta

from record import Record
from fields import Field, Name, Phone, Birthday


class AddressBook(UserDict):
    BIRTHDAY_REMINDER = 7  # кількість днів уперед для перевірки

    def add_record(self, record):
        #Додати Record до книги. Ключ — імʼя (рядок).
        self.data[record.name.value] = record

    def find(self, name):
        #Знайти Record за імʼям. Повертає Record або None.
        return self.data.get(name)

    def delete(self, name):
        #Видалити Record за імʼям.
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        #Повертає список словників
        today = datetime.today().date()
        end_date = today + timedelta(days=self.BIRTHDAY_REMINDER)
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            bday_this_year = bday_date.replace(year=today.year)

            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            if today <= bday_this_year <= end_date:
                congrat_date = bday_this_year

                if congrat_date.weekday() == 5:      # субота
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:    # неділя
                    congrat_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congrat_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming


# Щоб зовнішній код міг і далі робити:
# from address_book import AddressBook, Record, Name, Phone, Birthday
__all__ = ["AddressBook", "Record", "Field", "Name", "Phone", "Birthday"]
