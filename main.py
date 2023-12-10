'''
Наш асистент вже вміє взаємодіяти з користувачем за допомогою командного рядка, 
отримуючи команди та аргументи та виконуючи потрібні дії. 
У цьому завданні треба буде попрацювати над внутрішньою логікою асистента, 
над тим, як зберігаються дані, які саме дані і що з ними можна зробити.
'''
from collections import UserDict
import datetime

# {name:{phone:[], email:[], favorite: False}}


class Field:
    '''
    Базовий клас для полів запису. Буде батьківським для всіх полів, 
    у ньому реалізується логіка загальна для всіх полів
    '''

    def __init__(self, value = None):
        self.__value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

class Birthday(Field):
    '''
    Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
    '''
    def __init__(self, value):
        self.value = value
        super().__init__()

    @property
    def value(self):
        '''value getter'''
        return self.__value

    @value.setter
    def value(self, value):
        if value is not None:
            try:
                self.__value = datetime.date.fromisoformat(value)
            except ValueError:
                raise(
                    f'Birthday expected in format: YYYY-MM-DD, instead "{value}" given.'
                    )
        else:
            self.__value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)

class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''

    def __init__(self, value):
        self.value = value
        super().__init__()

    @property
    def value(self):
        '''value getter'''
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isidentifier():
            raise ValueError(
                f'Name should start with letter and contain only letters and digits - \
                    "{value}" given.'
                )
        if (len(value) == 0) | (value is None):
            raise ValueError('Name could not be ommited - "{value}" given.')
        self.__value = value

    def __str__(self):
        return str(self.__value)


class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр). 
    Необов'язкове поле з телефоном та таких один запис Record може містити декілька.
    '''

    def __init__(self, value):
        self.value = value
        super().__init__()

    @property
    def value(self):
        '''value getter'''
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError(f'Phone should have only digits - "{value}" given.')
        if len(value) != 10:
            raise ValueError(
                f'Phone should be at least 10 digits long - "{value}" given.')
        self.__value = value

    def __str__(self):
        return str(self.__value)

class Record():
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. 
    Відповідає за логіку додавання/видалення/редагування необов'язкових полів та 
    зберігання обов'язкового поля Name
    '''

    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        '''додавання об'єктів'''
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        '''видалення об'єктів'''
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return
        raise ValueError (
            f'Phone "{phone}" not found for contact "{self.name}".')

    def edit_phone(self, old_phone, new_phone):
        '''редагування об'єктів'''
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for item in self.phones:
            if item.value == old_phone.value:
                self.phones.insert(self.phones.index(item), new_phone)
                self.phones.remove(item)
                return
        raise ValueError(
            f'Phone "{old_phone}" not found for contact "{self.name}".')

    def find_phone(self, phone):
        '''пошук об'єктів'''
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def days_to_birthday(self):
        '''
        метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту, 
        якщо день народження заданий.
        '''

        if not self.birthday.value:
            days_to_bd = None
        else:
            td = datetime.date.today()
            bd = datetime.date(td.year, self.birthday.value.month, self.birthday.value.day)

            if td <= bd:
                days_to_bd = (bd - td).days
            else:
                days_to_bd = (datetime.date(bd.year + 1, bd.month, bd.day) - td).days

        return days_to_bd

    def __str__(self):
        return f'Contact name: {self.name}, birthday {self.birthday}, phones: {", ".join([x.value for x in self.phones])}'
        # return f'Contact name: {self.name}, phones: {", ".join([x.value for x in self.phones])}'

    def __repr__(self):
        return f'Contact name: {self.name}, birthday {self.birthday}, phones: {", ".join([x.value for x in self.phones])}'
        # return f'Contact name: {self.name}, phones: {", ".join([x.value for x in self.phones])}'


class AddressBook(UserDict):
    '''
    Клас для зберігання та управління записами. 
    Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
    '''

    def __init__(self):
        super().__init__()
        self.__n = 1 #records per printed sheet
        self.__current_index = 0
        self.__records = []

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

    def __next__(self):
        
        out_dict = ''
        for _ in range(self.__n):
            if self.__current_index < len(self.__records):
                record = self.find(self.__records[self.__current_index])
                out_dict += str(record) + '\n'
                self.__current_index +=1
            else:
                break
        
        if out_dict:
            return out_dict
        else:
            raise StopIteration

    def __iter__(self):
        self.__records = list(self.data.keys())
        return self


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

# # juli_record = Record("Juli", "1/1/80")
# juli_record = Record("Juli", "1980-12-11")
# juli_record.add_phone("9876543210")
# book.add_record(juli_record)

# for name, record in book.data.items():
#     print(record)

# print(juli_record.days_to_birthday())
# print(john.days_to_birthday())

# import random
# letters = 'abcdifghijklmnopqrstuvwxyz'
# numbers = '0123456789'
# for i in range(20):
#     name = ''.join(random.choices(letters, k=4))
#     phone = ''.join(random.choices(numbers, k=10))
#     rec = Record(name)
#     rec.add_phone(phone)
#     book.add_record(rec)

# book._AddressBook__n = 5

# for i in book:
#     print(i)
#     print('-----------')
