"""Консольний бот для управління додатком"""
import os
# import bot_helper.address_book as book
# import bot_helper.note_book as notebook
# import bot_helper.pretty as pretty
# from bot_helper.clean import sorting_files
# from bot_helper.commands import *

# from . import address_book as book
# from . import note_book as notebook
# from . import pretty
# from .clean import sorting_files
# from .commands import *

import address_book as book
import pretty
from commands import *

def input_error(func):
    """Функія-декоратор, що ловить помилки вводу"""
    def inner(my_book, val):
        try:
            return_data = func(my_book, val)
        except IndexError:
            return_data = ("Give me name please", )   #and phone please", )
        except TypeError:
            return_data = ("Wrong command, try again", )
        except KeyError:
            return_data = ("Wrong user, repeat please", )
        except ValueError:
            return_data = ("Wrong number, repeat please", )
        
        except book.UserExists:
            return_data = ('User already exists.')
        except book.WrongName:
            return_data = ("User not exists, repeat please", )
        except book.WrongPhone:
            return_data = (
                'Phone should have only digits and be at least 10 digits long.', )
        except book.ExistsPhone:
            return_data = ("Phone is exist", )
        except book.NotExistsPhone:
            return_data = ("Phone not exist", )
        except book.WrongBirthday:
            return_data = ("Wrong birthday, repeat please", )
        except book.ExistsBirthday:
            return_data = ("User already has a birthday", )
        except book.WrongMemo:
            return_data = (
                "Not printable characters in Memo or record size excides.", )
        except book.ExistsMemo:
            return_data = ("User already has a memo", )
        except book.WrongAddress:
            return_data = (
                "Not printable characters in Address or record size excides.", )
        except book.ExistsAddress:
            return_data = ("User already has an address", )
        except book.WrongEmail:
            return_data = ("Wrong e-mail, repeat please", )
        except book.ExistsEmail:
            return_data = ("User already has an e-mail", )
        return return_data
    return inner


def handler_hello(my_book=None, _=None):
    return "How can I help you?"

def handler_help(my_book=None, _=None):
    """Метод обробляє команду 'help'
    """
    help_list = [
        ['help', 'command description'],
        ['hello', 'greets the user'],
        ['add <name> \[phone] \[birthday] \[Email] \[postal address] \[memos]',
         'for add user, if user is exist will be added\n'
         'variation format for telefon number:\n'
         '+38(055)111-22-33\n'
         '38(055)111-22-34\n'
         '8(055)111-22-35\n'
         '(055)111-22-36\n'
         '055111-22-37\n'
         'and all variant without "-"'],
        ['change <name> <from phone> <to phone>', 'for chandge phone'],
        ['show-all', 'for show all records'],
        ['find <some letters> | find <some numbers>',
            'for find record by name or phone'],
        ['delete-telephone <user> <phone>', 'for delete phone from user'],
        ['delete-user <user>', 'for delete user from address book'],
        ['email-add <name> <email text>', 'to add e-mail to user'],
        ['email-delete <name>', 'to delete Email from user'],
        ['email-replace <name> <new Email>',
            'to replace existing Email with new text'],
        ['next-birthday <name>',
            'shows the number of days until the subscriber`s next birthday'],
        ['finde-birthday \[number of days]',
            'displaying a list of subscribers for the nearest specified number of days'],
        ['memo-add <name> <note text>',
            'to add note to user (max.240 printable characters)'],
        ['memo-delete <name>', 'to delete note from user'],
        ['memo-replace <name> <note text>',
            'to replace existing note at user with new text'],
        ['address-add <name> <address text>',
            'to add address to user (max.100 printable characters)'],
        ['address-delete <name>', 'to delete address from user'],
        ['address-replace <name> <new address>',
            'to replace existing address at user with new text'],
        # ['add-note <title> <text> \[tag]',' to add note'],
        # ['change-note <title> <new_text>', 'to change text in note by title'],
        # ['show-all-notes', 'to show all notes'],
        # ['find-note <some text>', 'to find notes by <some_text> in title of note'],
        # ['find-note-by-tag <some text>', 'to find notes by <some_text> in tags of note'],
        # ['delete-note-tag <title> <tag>', 'to delete tag <tag> in note <title>'],
        # ['add-note-tag <title> <tag>', 'to add tag <tag> in note <title>'],
        # ['delete-note <title>', 'to delete note by <title>'],
        # ['sort-folder <path>', 'sorts files in a folder path'],
        ['close | exit', 'for exit']
    ]

    pretty.table(
        title='List of commands with format',
        header=['Command', 'Description'],
        rows=help_list,
    )

def handler_show_all(my_book, _=None):
    if my_book:
        return my_book
    return ('No users',)

def handler_exit(my_book, _=None):
    return "Good bye!"

def handler_add_user(my_book, list_):

    if list_[0] == "":
        raise IndexError
    
    phone = my_book.find_pattern(list_[1], 'phones')
    if phone:
        raise book.ExistsPhone
    
    list_[0] = list_[0].capitalize()

    record = my_book.find(list_[0])
    if record:
        raise book.UserExists
    else:
        param_names = book.PARAM_NAMES
        rec_data = {param_names[i]: list_[i] for i in range(len(param_names))}
        record = book.Record(**rec_data)

    my_book.add_record(record)
    
    return "Command successfully complete"

def handler_delete_user(my_book, list_):

    my_book.delete(list_[0].capitalize())
    return f"User {list_[0].capitalize()} successfully deleted"

def handler_find_user(my_book, list_):

    list_rec = my_book.find(list_[0].capitalize())
    if list_rec:
        ret_book = book.AddressBook()
        ret_book.rec_per_page = my_book.rec_per_page
        ret_book.add_record(list_rec)
        return ret_book
    return "Contact not found"

def handler_find_pattern(my_book, list_):
    """Search for given pattern in given field(s) of record
    """
    list_rec = my_book.find_pattern(*list_)
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        ret_book.rec_per_page = my_book.rec_per_page
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return f"Pattern {list_[0]} not found."

def handler_add_phone(my_book, list_):
    found = my_book.find_pattern(list_[1], 'phones')
    if found:
        raise book.ExistsPhone
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.add_phone(list_[1])
    return f"For user {list_[0].capitalize()} successfully added phone {list_[1]}"

def handler_change_phone(my_book, list_):

    found = my_book.find_pattern(list_[2], 'phones')
    if found:
        raise book.ExistsPhone
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName

    if record.phones is not None:
        record.edit_phone(list_[1], list_[2])
        return f"Phone {list_[1]} from user {list_[0].capitalize()} successfully changet to phone {list_[2]}"
    else:
        list_.pop(1)
        return handler_add_phone(my_book, list_)    

def handler_delete_phone(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.delete_phone(list_[1])
    return f"From user {list_[0].capitalize()} successfully deleted phone {list_[1]}."

def handler_add_birthday(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.add_birthday(list_[1])
    return f"To user {list_[0].capitalize()} successfully added birthday date:\n\t {list_[1]}"

def handler_replace_birthday(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    if record.birthday is not None:
        record.edit_birthday(list_[1])
        return f"Birthday of user {list_[0].capitalize()} successfully changet to {list_[1]}"
    else:
        return handler_add_birthday(my_book, list_)    

def handler_delete_birthday(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.delete_birthday()
    return f"From user {list_[0].capitalize()} successfully deleted birthday date."

def handler_find_birthday(my_book, list_):

    qua_days = list_[0]
    if qua_days == "":
        qua_days = 10
    else:
        qua_days = int(qua_days)
    list_rec = my_book.find_records_for_birthday(qua_days)
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        ret_book.qua_for_iter = my_book.rec_per_page
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return ret_book
    return f"Contact with birthdays in {qua_days} days not found."

def handler_next_birthday(my_book, list_):

    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    days = record.days_to_birthday()
    if days:
        return f"Next birthday for user {list_[0].capitalize()} after {days} days"
    else:
        return f"Unknown birthday for user {list_[0].capitalize()}"

def handler_add_email(my_book, list_):
    found = my_book.find_pattern(list_[1], 'emails')
    if found:
        raise book.ExistsEmail
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.add_email(list_[1])
    return f"To user {list_[0].capitalize()} successfully added e-mail:\n\t {list_[1]}"

def handler_delete_email(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.delete_email(list_[1])
    return f"From user {list_[0].capitalize()} successfully deleted e-mail {list_[1]}."

def handler_replace_email(my_book, list_):
    found = my_book.find_pattern(list_[2], 'emails')
    if found:
        raise book.ExistsEmail
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    if record.emails is not None:
        record.edit_email(list_[1], list_[2])
        return f"For user {list_[0].capitalize()} e-mail\n\t{list_[1]} \nsuccessfully changed to:\n\t{list_[2]}"
    else:
        list_.pop(1)
        return handler_add_email(my_book, list_)    

def handler_add_memo(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    new_memo = ' '.join(list_[1:])
    record.add_memo(new_memo)
    return f"To user {list_[0].capitalize()} successfully added memo:\n\t {new_memo}"

def handler_delete_memo(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.delete_memo(list_[1])
    return f"From user {list_[0].capitalize()} successfully deleted memo {list_[1]}."

def handler_replace_memo(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    if record.memos is not None:
        record.edit_memo(list_[1], list_[2])
        return f"For user {list_[0].capitalize()} memo\n\t{list_[1]} \nsuccessfully changed to:\n\t{list_[2]}"
    else:
        list_.pop(1)
        return handler_add_memo(my_book, list_)

def handler_add_addr(my_book, list_):
    found = my_book.find_pattern(list_[1], 'address')
    if found:
        raise book.ExistsAddress
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    new_addr = ' '.join(list_[1:])
    record.add_address(new_addr)
    return f"To user {list_[0].capitalize()} successfully added address:\n\t {new_addr}"

def handler_delete_addr(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    record.delete_address(list_[1])
    return f"From user {list_[0].capitalize()} successfully deleted address {list_[1]}."

def handler_replace_addr(my_book, list_):
    found = my_book.find_pattern(list_[2], 'address')
    if found:
        raise book.ExistsAddress
    record = my_book.find(list_[0].capitalize())
    if not record:
        raise book.WrongName
    if record.address is not None:
        record.edit_address(list_[1], list_[2])
        return f"For user {list_[0].capitalize()} address\n\t{list_[1]} \nsuccessfully changed to:\n\t{list_[2]}"
    else:
        list_.pop(1)
        return handler_add_addr(my_book, list_)

NAME_COMMANDS = {

    "help": handler_help,
    "hello": handler_hello,
    "show-all": handler_show_all, 
    "close": handler_exit,
    "exit": handler_exit,

    "user-add": handler_add_user,
    "user-find": handler_find_user,
    "user-delete": handler_delete_user,
    "pattern-find": handler_find_pattern,

    "phone-add": handler_add_phone,
    "phone-delete": handler_delete_phone,
    "phone-replace": handler_change_phone,

    "birthday-add": handler_add_birthday,
    "birthday-delete": handler_delete_birthday,
    "birthday-replace": handler_replace_birthday,
    "birthday-next": handler_next_birthday,
    "birthday-find": handler_find_birthday,
    
    "email-add": handler_add_email,
    "email-delete": handler_delete_email,
    "email-replace": handler_replace_email,

    "memo-add": handler_add_memo,
    "memo-delete": handler_delete_memo,
    "memo-replace": handler_replace_memo,

    "address-add": handler_add_addr,
    "address-delete": handler_delete_addr,
    "address-replace": handler_replace_addr
    }


# def defs_commands(comm):
#     """Метод додає до команди функцію"""
#     return NAME_COMMANDS[comm]


@input_error
def parser_command(my_book, command):
    list_command = command
    if list_command[0] in NAME_COMMANDS:
        any_command = NAME_COMMANDS.get(list_command[0])
        ret_rezault = any_command(my_book, list_command[1:])
        return ret_rezault
    else:
        raise TypeError


current_path = os.path.abspath(os.getcwd())
# file_name_phones_p = os.path.join(current_path, 'bot_helper', 'book_pickle.bin')
# file_name_notes_p = os.path.join(current_path, 'bot_helper', 'notes_book_pickle.bin')

# file_name_phones_p = os.path.join(current_path, 'book_pickle.bin')
file_name_phones = os.path.join(current_path, 'phonebook.json')

def main():
    """Метод відновлює книги контактів та нотатки, обирає режим роботи"""
    handler_hello()

    if os.path.exists(file_name_phones):
        my_book_phones = book.AddressBook()
        my_book_phones.load_JSON(file_name_phones)
    else:
        my_book_phones = book.AddressBook()
    
    # if os.path.exists(file_name_notes_p):
    #     my_book_notes_p = notebook.NoteBook()
    #     my_book_notes = my_book_notes_p.load_from_file_pickle(file_name_notes_p)
    # else:
    #     my_book_notes = notebook.NoteBook()

    while True:
        command = get_command_suggestions()
        ret_rezault = parser_command(my_book_phones, command)

        if ret_rezault:
            pretty.parser(ret_rezault, '1')
            # pretty.parser(ret_rezault, mode)
            if ret_rezault == "Good bye!":
                # my_book_phones.save_to_file_pickle(file_name_phones_p)
                # my_book_notes.save_to_file_pickle(file_name_notes_p)
                my_book_phones.save_JSON(file_name_phones)
                exit()

if __name__ == "__main__":
    main()
