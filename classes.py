from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid_date(value) and not self.has_birthday():
            self.__value = value
        elif not self.is_valid_date(value):
            raise ValueError("Incorrect date format. Use DD.MM.YYYY")
        elif self.has_birthday():
            raise ValueError("The birthday has alrady added")

    def is_valid_date(self, date):
        # Використовуємо регулярний вираз для перевірки формату
        date_pattern = r"^\d{2}\.\d{2}.\d{4}$"
        return re.match(date_pattern, date) is not None

    def has_birthday(self):
        return any(isinstance(field, Birthday) for field in self.value)


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.validate_phone(value):
            self.__value = value
        else:
            raise ValueError("Invalid phone number")

    def validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, serched_phone):
        for phone in self.phones:
            if phone.value == serched_phone:
                return phone
        return "Phone not found"

    def add_birthday(self, birthday):
        if self.birthday == None:
            self.birthday = birthday
            return "You add the birthday"
        else:
            return "The birthday has alrady added"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def show_birthday(self, name):
        if name in self.data:
            return self.data[name].birthday
        else:
            return None

    def get_birthdays_per_week(self):
        pass


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    john.add_birthday("29.10.1999")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    print(book.show_birthday("John"))
    # Видалення запису Jane
    book.delete("Jane")
