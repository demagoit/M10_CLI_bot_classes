'''
Наш асистент вже вміє взаємодіяти з користувачем за допомогою командного рядка,
отримуючи команди та аргументи та виконуючи потрібні дії.
У цьому завданні треба буде попрацювати над внутрішньою логікою асистента,
над тим, як зберігаються дані, які саме дані і що з ними можна зробити.
'''
from collections import UserDict
import datetime
import json

# {name:{phone:[], email:[], favorite: False}}


class Field:
    '''
    Базовий клас для полів запису. Буде батьківським для всіх полів,
    у ньому реалізується логіка загальна для всіх полів
    '''

    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)


class Birthday(Field):
    '''
    Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
    '''

    def __init__(self, value):
        super().__init__()
        self.value = value

    @property
    def value(self):
        '''value getter'''
        return self._value

    @value.setter
    def value(self, value):
        if value is not None:
            try:
                datetime.date.fromisoformat(value)
                self._value = value
            except ValueError:
                raise (
                    f'Birthday expected in format: YYYY-MM-DD, instead "{value}" given.'
                )
        else:
            self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)


class Name(Field):
    '''
    Клас для зберігання імені контакту. Обов'язкове поле.
    '''

    def __init__(self, value):
        super().__init__()
        self.value = value

    @property
    def value(self):
        '''value getter'''
        return self._value

    @value.setter
    def value(self, value):
        if not value.isidentifier():
            raise ValueError(
                f'Name should start with letter and contain only letters and digits - \
                    "{value}" given.'
            )
        if (len(value) == 0) | (value is None):
            raise ValueError('Name could not be ommited - "{value}" given.')
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)

class Phone(Field):
    '''
    Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном та таких один запис Record може містити декілька.
    '''

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    @property
    def value(self):
        '''value getter'''
        return self._value

    @value.setter
    def value(self, value: str):
        if not value.isdigit():
            raise ValueError(
                f'Phone should have only digits - "{value}" given.')
        if len(value) != 10:
            raise ValueError(
                f'Phone should be at least 10 digits long - "{value}" given.')
        self._value = value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)


class Record():
    '''
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    Відповідає за логіку додавання/видалення/редагування необов'язкових полів та
    зберігання обов'язкового поля Name
    '''

    def __init__(self, name: str, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        '''додавання об'єктів'''
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        '''видалення об'єктів'''
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return
        raise ValueError(
            f'Phone "{phone}" not found for contact "{self.name}".')

    def edit_phone(self, old_phone: str, new_phone: str):
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

    def __find_phone_pattern(func):
        def inner(self, phone):
            result = func(self, phone)
            if result:
                return result
            else:
                match_list = []
                for item in self.phones:
                    if phone in item.value:
                        match_list.append(item.value)
                return '\n'.join(match_list) if match_list else None
        return inner

    @__find_phone_pattern
    def find_phone(self, phone: str):
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
            obd = datetime.date.fromisoformat(str(self.birthday))
            bd = datetime.date(td.year, obd.month, obd.day)

            if td <= bd:
                days_to_bd = (bd - td).days
            else:
                days_to_bd = (datetime.date(
                    bd.year + 1, bd.month, bd.day) - td).days

        return days_to_bd

    def __str__(self):
        return f'Contact name: {self.name}, birthday {self.birthday}, phones: {", ".join([x.value for x in self.phones])}'

    def __repr__(self):
        return f'Contact name: {self.name}, birthday {self.birthday}, phones: {", ".join([x.value for x in self.phones])}'


class AddressBook(UserDict):
    '''
    Клас для зберігання та управління записами.
    Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
    '''

    def __init__(self):
        super().__init__()
        self.__n = 1  # records per printed sheet

    @property
    def rec_per_page(self):
        '''records per printed sheet'''
        return self.__n

    @rec_per_page.setter
    def rec_per_page(self, value: str):
        try:
            self.__n = int(value)
        except:
            raise ValueError(
                f'Number records per page should be integer - "{value}" given.')

    def add_record(self, contact: Record):
        '''додає запис до self.data.'''
        self.data[str(contact.name)] = contact

    def __find_name_pattern(func):
        def inner(self, pattern: str):
            result = func(self, pattern)
            if result:
                return result
            else:
                match_list = []
                if pattern.isdigit():
                    '''знаходить запис за фрагментом номера.'''
                    for name in self.data.keys():
                        found = self.data.get(name).find_phone(pattern)
                        if found:
                            match_list.append(str(self.data.get(name)))
                    return '\n'.join(match_list) if match_list else None
                else:
                    '''знаходить запис за фрагментом імені.'''
                    for name in self.data.keys():
                        pattern_match = name.lower().find(pattern.lower())
                        if pattern_match != -1:
                            match_list.append(str(self.find(name)))
                    return '\n'.join(match_list) if match_list else None

        return inner

    @__find_name_pattern
    def find(self, name: str):
        '''знаходить запис за ім'ям.'''
        if name in self.data.keys():
            return self.data.get(name)
        return None

    def delete(self, name: str):
        '''який видаляє запис за ім'ям.'''
        if name in self.data.keys():
            self.data.pop(name)

    def save_JSON(self, filename='phonebook.json'):
        with open(filename, 'w') as fh:
            json.dump(self, fh, indent=4, cls=BookEncoder)

    def load_JSON(self, filename='phonebook.json'):
        with open(filename, 'r') as fh:
            input = json.load(fh)

        for item in input.keys():
            phones = input.get(item).get('phones')
            rec = Record(input.get(item).get('name'),
                               input.get(item).get('birthday'))
            for phone in phones:
                rec.add_phone(phone)
            self.add_record(rec)

    def __iter__(self):
        return AddressBookItterator(self)


class AddressBookItterator(UserDict):
    def __init__(self, adr_book: AddressBook):
        self.data = adr_book.data
        self.__n = adr_book.rec_per_page  # records per printed sheet
        self.__current_index = 0
        self.__records = list(self.data.keys())
        self.__records.sort()

    def __next__(self):

        output = ''
        for _ in range(self.__n):
            if self.__current_index < len(self.__records):
                record = self.data.get(self.__records[self.__current_index])
                output += str(record) + '\n'
                self.__current_index += 1
            else:
                break

        if output:
            return output

        raise StopIteration


# subclass JSONEncoder
# https://pynative.com/make-python-class-json-serializable/
class BookEncoder(json.JSONEncoder):
    def default(self, obj):
        if 'data' in obj.__dict__:
            out = obj.__dict__.get("data")
        elif '_value' in obj.__dict__:
            out = obj.__dict__.get('_value')
        else:
            out = obj.__dict__
        return out


# class BookDencoder(json.JSONDecoder):
#     def default(self, obj):
#         out = obj.__dict__
#         for item in out.keys():
#             phones = item.get('phones')
#             out[item] = Record(item.get('name'), item.get('birthday'))
#             for phone in phones:
#                 out[item].add_phone(phone)
#         return out