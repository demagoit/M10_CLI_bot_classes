from main import *

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("5555555555", "1112223333")

print(f'\n 1. {john}')

mult = book.find("j")
print(f'\n2.------\n{mult}\n----')

found_phone = john.find_phone("1112223333")
print(f"{john.name}: {found_phone}")

mult = john.find_phone("23")
print(f'\n3.------\n{mult}\n----')

mult = book.find('9')
print(f'\n4.------\n{mult}\n----')

book.delete("Jane")

# juli_record = Record("Juli", "1/1/80")
juli_record = Record("Juli", "1980-12-11")
juli_record.add_phone("9876543210")
book.add_record(juli_record)

for name, record in book.data.items():
    print(record)

print(juli_record.days_to_birthday())
print(john.days_to_birthday())
print('********************\n')

import random
letters = 'abcdifghijklmnopqrstuvwxyz'
numbers = '0123456789'
for i in range(20):
    name = ''.join(random.choices(letters, k=4)).title()
    phone = ''.join(random.choices(numbers, k=10))
    rec = Record(name)
    rec.add_phone(phone)
    book.add_record(rec)

book.rec_per_page = 5

for i in book:
    print(i)
    print('-----------')

book.save_JSON()

book_1 = AddressBook()
book_1.load_JSON()
book_1.rec_per_page = 10

for i in book_1:
    print(i)
    print('++++++')
