from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass  # Base class does not provide validation


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        super().validate(value)


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        super().validate(value)

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
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            return e

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                phone.validate(new_phone)
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
        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.month, self.birthday.day)
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.month, self.birthday.day)
        days_left = (next_birthday - today).days
        return days_left

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'Not specified'}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]

