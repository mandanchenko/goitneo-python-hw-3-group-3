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
def add_contact(args, book):
    new_record = Record(args[0])
    new_record.add_phone(args[1])
    book.add_record(new_record)
    return "Contact added."


@input_error
def change_contact(args, book):
    if book.delete(args[0]):
        new_record = Record(args[0])
        new_record.add_phone(args[1])
        book.add_record(new_record)
        return "Contact updated."
    else:
        return "Name not found!"


@input_error
def show_phone(arg, book):
    searched_record = book.find(arg)
    for phone in searched_record.phones:
        print(phone)


@input_error
def show_all(book):
    for name, record in book.data.items():
        print(record)


@input_error
def add_birthday(args, book):
    searched_record = book.find(args[0])
    searched_record.add_birthday(args[1])
    return "birthday added"


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
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            show_phone(args[0], book)
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(book.show_birthday(args[0]))
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
