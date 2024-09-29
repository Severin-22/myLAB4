import csv
import random 
from faker import Faker


number_records = 2000 # це змінна для кількості записів

male_count = int(number_records * 0.6) # це змінна для кількості чол імен

female_count = number_records - male_count # це змінна для кількості жін імен

fake = Faker('uk_UA') # тут відбувається ініціалізація бібліотеки за укр мовою

fields = ['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада', 
          'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'] # це змінна для полів що в методичці

def generate_record(gender): # це функція, в середині якої відбуватиметься записи у таблицю
    first_name = fake.first_name_male() if gender == 'Чоловік' else fake.first_name_female()
    last_name = fake.last_name_male() if gender == 'Чоловік' else fake.last_name_female()
    patronymic = fake.middle_name_male() if gender == 'Чоловік' else fake.middle_name_female()
    
    record = {
        'Прізвище': last_name,
        'Ім’я': first_name,
        'По батькові': patronymic,
        'Стать': gender,
        'Дата народження': fake.date_of_birth(minimum_age=16, maximum_age=85).strftime('%d.%m.%Y'),
        'Посада': fake.job(),
        'Місто проживання': fake.city(),
        'Адреса проживання': fake.address(),
        'Телефон': fake.phone_number(),
        'Email': fake.email()
    }
    return record

#  37 і 38 рядки генерують записи за статтю
records = [generate_record('Чоловік') for _ in range(male_count)]
records += [generate_record('Жінка') for _ in range(female_count)]

with open('Serhii-table.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)

    writer.writeheader()

    writer.writerows(records)

print("Твої дані збереглися у csv файл")
