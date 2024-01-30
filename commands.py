from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

NAME_COMMANDS = [
    "help",
    "hello",
    "show-all",
    "goodbye",
    "close",
    "exit",

    "user-add",
    "user-delete",
    "user-find",
    "pattern-find",

    "phone-add",
    "phone-replace",
    "phone-delete",

    "birthday-add",
    "birthday-replace",
    "birthday-delete",
    "birthday-next",
    "birthday-find",

    "address-add",
    "address-replace",
    "address-delete",

    "email-add",
    "email-replace",
    "email-delete",

    "memo-add",
    "memo-replace",
    "memo-delete"
]

PROMPTS = {"command_prompt": "Please enter your command: ",
           
           "search_prompt_pattern": "Enter a pattern to search: ",
           "search_prompt_scope": "Enter field to search (or enter to search everywhere): ",
           
           "user_name_prompt": "Enter contact name: ",
           "user_del_prompt": "Enter contact name to delete: ",

           "phone_prompt": "Enter phone number: ",
           "phone_del_prompt": "Enter phone to delete: ",
           "old_phone_prompt": "Enter old phone number: ",
           "new_phone_prompt": "Enter new phone number: ",

           "birthday_prompt": "Enter birthday(yyyy-mm-dd): ",
           "birthday_search_prompt": "Enter quantity of days: ",

           "email_prompt": "Enter email: ",
           "email_del_prompt": "Enter e-mail to delete: ",
           "old_email_prompt": "Enter old e-mail: ",
           "new_email_prompt": "Enter new e-mail: ",

           "address_prompt": "Enter address: ",
           "address_del_prompt": "Enter address to delete: ",
           "old_address_prompt": "Enter old address: ",
           "new_address_prompt": "Enter new address: ",

           "memo_prompt": "Enter memo: ",
           "memo_del_prompt": "Enter memo to delete: ",
           "old_memo_prompt": "Enter old memo: ",
           "new_memo_prompt": "Enter new memo: "
           }


def get_command_suggestions():
    try:           
        user_input = prompt(PROMPTS.get("command_prompt"), completer=WordCompleter(
            NAME_COMMANDS, ignore_case=True))
        
        if user_input == "show-all":
            command = user_input
            user_input_list = [command]
            return user_input_list
        
        elif user_input == "goodbye" or user_input == "close" or user_input == "exit":
            return [user_input]

        elif user_input == "help":
            command = user_input
            user_input_list = [command]
            return user_input_list

        elif user_input == "hello":
            command = user_input
            user_input_list = [command]
            return user_input_list

        elif user_input == "back":
            command = user_input
            user_input_list = [command]
            return user_input_list

        elif user_input == "user-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            phone = input(PROMPTS.get("phone_prompt"))
            birthday = input(PROMPTS.get("birthday_prompt"))
            email = input(PROMPTS.get("email_prompt"))
            address = input(PROMPTS.get("address_prompt"))
            memo = input(PROMPTS.get("memo_prompt"))
            user_input_list = [command, name, phone, birthday, email, address, memo]
            return user_input_list

        elif user_input == "user-delete":
            command = user_input
            name = input(PROMPTS.get("user_del_prompt"))
            user_input_list = [command, name]
            return user_input_list

        elif user_input == "user-find":
            command = user_input
            value = input(PROMPTS.get("user_name_prompt"))
            user_input_list = [command, value]
            return user_input_list

        elif user_input == "pattern-find":
            command = user_input
            value = input(PROMPTS.get("search_prompt_pattern"))
            scope = input(PROMPTS.get("search_prompt_scope"))
            user_input_list = [command, value, scope]
            return user_input_list

        elif user_input == "phone-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("phone_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "phone-replace":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            old_value = input(PROMPTS.get("old_phone_prompt"))
            new_value = input(PROMPTS.get("new_phone_prompt"))
            user_input_list = [command, name, old_value, new_value]
            return user_input_list
        
        elif user_input == "phone-delete":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("phone_del_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "birthday-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("birthday_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "birthday-delete":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            user_input_list = [command, name]
            return user_input_list

        elif user_input == "birthday-replace":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("birthday_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "birthday-next":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            user_input_list = [command, name]
            return user_input_list

        elif user_input == "birthday-find":
            command = user_input
            value = input(PROMPTS.get("birthday_search_prompt"))
            user_input_list = [command, value]
            return user_input_list

        elif user_input == "email-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("email_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "email-delete":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("email_del_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "email-replace":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            old_value = input(PROMPTS.get("old_email_prompt"))
            new_value = input(PROMPTS.get("new_email_prompt"))
            user_input_list = [command, name, old_value, new_value]
            return user_input_list

        elif user_input == "memo-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("memo_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "memo-delete":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("memo_del_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "memo-replace":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            old_value = input(PROMPTS.get("old_memo_prompt"))
            new_value = input(PROMPTS.get("new_memo_prompt"))
            user_input_list = [command, name, old_value, new_value]
            return user_input_list

        elif user_input == "address-add":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("address_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "address-delete":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            value = input(PROMPTS.get("address_del_prompt"))
            user_input_list = [command, name, value]
            return user_input_list

        elif user_input == "address-replace":
            command = user_input
            name = input(PROMPTS.get("user_name_prompt"))
            old_value = input(PROMPTS.get("old_address_prompt"))
            new_value = input(PROMPTS.get("new_address_prompt"))
            user_input_list = [command, name, old_value, new_value]
            return user_input_list

        return user_input.lower()
    
    except KeyboardInterrupt:
        user_input_list = ("\nCommand input interrupted. Exiting...",)
        exit()

