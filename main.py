from collections import UserDict

# {name:{phone:[], email:[], favorite: False}}

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # self.__str__()
    pass    


class Phone(Field):
    def __init__(self, value):
        
        # if value.startswith('+'):
        #     value = value[1:]
        if not value.isdigit():
            raise ValueError
        # if len(value) == 12:
        #     value = '+' + value
        # elif len(value) == 10:
        #     value = '+38' + value
        # elif len(value) == 9:
        #     value = '+380' + value
        # else:
        #     raise ValueError

        if len(value) != 10:
            raise ValueError
        
        super().__init__(value)
        


class Record():
    
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    

    def remove_phone(self, phone):
        # phone = Phone(phone).value
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return
        raise ValueError
        
    def edit_phone(self, old_phone, new_phone):
        # print(old_phone)
        # print([x.value for x in self.phones])
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        
        for item in self.phones:
            if item.value == old_phone.value:
                self.phones.insert(self.phones.index(item), new_phone)
                self.phones.remove(item)
                return
        raise ValueError
        
    def find_phone(self, phone):
        # print(phone, type(phone))
        # print(self.phones)
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def __str__(self):
        return f'Contact name: {self.name}, phones: {", ".join([x.value for x in self.phones])}'

    # def add_phone(self, phone):
    #     self.phones.append(Phone(phone).__str__())

    # def remove_phone(self, phone):
    #     phone = Phone(phone).__str__()
    #     if phone in self.phones:
    #         self.phones.remove(phone)
    #     else:
    #         pass
    #         # raise

    # def edit_phone(self, old_phone, new_phone):
    #     old_phone = Phone(old_phone).__str__()
    #     new_phone = Phone(new_phone).__str__()

    #     if old_phone in self.phones:
    #         self.phones.insert(self.phones.index(old_phone), new_phone)
    #         self.remove_phone(old_phone)
    #     else:
    #         # raise
    #         pass

    # def find_phone(self, phone):
    #     print(phone, type(phone))
    #     print(self.phones)
    #     for item in self.phones:
    #         if phone in item:
    #             return item
    #     return None

    # def __str__(self):
    #     return f'Contact name: {self.name}, phones: {", ".join(self.phones)}'


class AddressBook(UserDict):
    # def __init__(self):
    #     pass

    def add_record(self, contact):
        # додає запис до self.data.
        self.data[contact.name.__str__()] = contact

    def find(self, name):
        # знаходить запис за ім'ям.
        if name in self.data.keys():
            return self.data.get(name) 
        # else:
        #     raise KeyError

    def delete(self, name):
        # який видаляє запис за ім'ям.
        if name in self.data.keys():
            self.data.pop(name)
        # else:
        #     raise KeyError


# book = AddressBook()

# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# book.add_record(john_record)

# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# for name, record in book.data.items():
#     print(record)

# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)

# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")

# book.delete("Jane")
