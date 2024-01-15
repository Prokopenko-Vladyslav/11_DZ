from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Phone number must contain 10 digits.")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неправильний формат дня народження. Використовуйте формат: Рік-Місяць-День.")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

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
                phone.validate_phone()
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
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        else:
            return None

    def print_days_to_birthday(self):
        days = self.days_to_birthday()
        if days is not None:
            print(f"Днів до наступного дня народження для {self.name.value}: {days} днів")
        else:
            print(f"Інформація про народження відсутня для {self.name.value}")

    def __repr__(self):
        return f"Ім'я контакту: {self.name.value}, телефони: {'; '.join(str(p) for p in self.phones)}, день народження: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]



# Створюємо користувача з ім'ям, телефоном і, за бажанням, днем народження
user_name = "Іван Іванов"
user_phone = "1234567890"
user_birthday = "1990-05-15"

try:
    # Спробуємо створити користувача і додати його до адресної книги
    user_record = Record(name=user_name, birthday=Birthday(user_birthday))
    user_record.add_phone(user_phone)

    # Виведемо інформацію про користувача та кількість днів до наступного дня народження
    print(user_record)
    user_record.days_to_birthday()

except ValueError as e:
    print(f"Помилка: {e}")
