from classes import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter correct user name"
        except IndexError:
            return "The entered value is outside the valid range"

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            new_record = Record(args[0])
            new_record.add_phone(args[1])
            book.add_record(new_record)
            print("Contact added.")
        elif command == "change":
            if book.delete(args[0]):
                new_record = Record(args[0])
                new_record.add_phone(args[1])
                book.add_record(new_record)
                print("Contact updated.")
            else:
                print("Name not found!")
        elif command == "phone":
            searched_record = book.find(args[0])
            print(searched_record.phones)
        elif command == "all":
            for name, record in book.data.items():
                print(record)
        # add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
        elif command == "add-birthday":
            searched_record = book.find(args[0])
            searched_record.add_birthday(args[1])

        # show-birthday [ім'я]: Показати дату народження для вказаного контакту.
        elif command == "show-birthday":
            print(book.show_birthday(args[0]))

        # birthdays: Показати дні народження, які відбудуться протягом наступного тижня.
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
