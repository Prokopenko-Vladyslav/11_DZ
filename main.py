from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if self.value is not None:
            if len(self.value) != 10 or not self.value.isdigit():
                raise ValueError("Phone number must contain 10 digits.")

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.validate()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте YYYY-MM-DD.")

    @property
    def year(self):
        return int(self.value.split('-')[0])

    @property
    def month(self):
        return int(self.value.split('-')[1])

    @property
    def day(self):
        return int(self.value.split('-')[2])


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        phone_number = Phone(phone)
        phone_number.validate()
        self.phones.append(phone_number)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone  # validate буде автоматично викликаний всередині value.setter
                phone_found = True
                break
        if not phone_found:
            raise ValueError("Phone number not found for editing.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        birthday_day = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        user_birthday_in_this_year = date(today.year, birthday_day.month, birthday_day.day)
        different = user_birthday_in_this_year - today
        if different.days > 0:
            return f'left until birthday {different.days} days'
        else:
            user_birthday_in_next_year = date(today.year + 1, birthday_day.month, birthday_day.day)
            different_new = user_birthday_in_next_year - today
            return f'left until birthday {different_new.days} days'

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Record with name '{name}' not found.")

    def iterator(self, batch_size):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]
            
book = AddressBook()
john_record = Record("John", birthday="1996-06-07")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)
print(john_record.birthday)
print(john_record)