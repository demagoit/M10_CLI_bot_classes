'''
Наш асистент вже вміє взаємодіяти з користувачем за допомогою командного рядка, 
отримуючи команди та аргументи та виконуючи потрібні дії. 
У цьому завданні треба буде попрацювати над внутрішньою логікою асистента, 
над тим, як зберігаються дані, які саме дані і що з ними можна зробити.
'''
from collections import UserDict

# {name:{phone:[], email:[], favorite: False}}


class Field:
    '''
    Базовий клас для полів запису. Буде батьківським для всіх полів, 
    у ньому реалізується логіка загальна для всіх полів
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''

    def __init__(self, value):
        if not value.isidentifier():
            raise ValueError
        if (len(value) == 0) | (value is None):
            raise ValueError
        super().__init__(value)


class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр). 
    Необов'язкове поле з телефоном та таких один запис Record може містити декілька.
    '''

    def __init__(self, value):

        if not value.isdigit():
            raise ValueError
        if len(value) != 10:
            raise ValueError

        super().__init__(value)


class Record():
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. 
    Відповідає за логіку додавання/видалення/редагування необов'язкових полів та 
    зберігання обов'язкового поля Name
    '''

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        '''додавання об'єктів'''
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        '''видалення об'єктів'''
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return
        raise ValueError

    def edit_phone(self, old_phone, new_phone):
        '''редагування об'єктів'''
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for item in self.phones:
            if item.value == old_phone.value:
                self.phones.insert(self.phones.index(item), new_phone)
                self.phones.remove(item)
                return
        raise ValueError

    def find_phone(self, phone):
        '''пошук об'єктів'''
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def __str__(self):
        return f'Contact name: {self.name}, phones: {", ".join([x.value for x in self.phones])}'


class AddressBook(UserDict):
    '''
    Клас для зберігання та управління записами. 
    Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
    '''

    def add_record(self, contact):
        '''додає запис до self.data.'''
        self.data[str(contact.name)] = contact

    def find(self, name):
        '''знаходить запис за ім'ям.'''
        if name in self.data.keys():
            return self.data.get(name)
        return None

    def delete(self, name):
        '''який видаляє запис за ім'ям.'''
        if name in self.data.keys():
            self.data.pop(name)


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
