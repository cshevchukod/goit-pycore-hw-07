from collections import UserDict
from datetime import datetime, timedelta

from record import Record


class AddressBook(UserDict):

    BIRTHDAY_REMINDER = 7

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Повертає список словників:
        {"name": <ім'я>, "congratulation_date": "DD.MM.YYYY"}
        для днів народження, які потрібно привітати протягом наступного тижня.
        """
        today = datetime.today().date()
        limit_date = today + timedelta(days=self.BIRTHDAY_REMINDER)
        result: list[dict] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            # вихідна дата народження
            bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            bday_this_year = bday.replace(year=today.year)

            # якщо в цьому році вже пройшов — переносимо на наступний
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            if today <= bday_this_year <= limit_date:
                congrat_date = bday_this_year

                # якщо вихідний — переносимо на понеділок
                if congrat_date.weekday() == 5:      # субота
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:    # неділя
                    congrat_date += timedelta(days=1)

                result.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congrat_date.strftime("%d.%m.%Y"),
                    }
                )

        return result
    