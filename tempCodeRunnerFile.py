import pandas as pd  # для роботи з даними
import matplotlib.pyplot as plt  # для побудови графіків
from datetime import datetime  # для роботи з датами
import os  # для роботи з файлами

def get_age(date_of_birth):
    """Повертає вік на основі дати народження."""
    try:
        birth_date = datetime.fromisoformat(date_of_birth)
    except ValueError:
        return None  # повертаємо None при помилці
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def read_csv(file_name):
    """Зчитує CSV файл і повертає DataFrame."""
    if not os.path.isfile(file_name):
        print("Не вдалося відкрити файл CSV.")
        return None

    try:
        data = pd.read_csv(file_name, sep=',', encoding='utf-8-sig')
        print("Файл успішно зчитано!")
        return data
    except Exception as e:
        print(f"Помилка під час зчитування файлу: {e}")
        return None

def plot_gender_count(data):
    """Підраховує і візуалізує кількість чоловіків і жінок."""
    gender_count = data['Стать'].value_counts()
    print("Кількість співробітників за статтю:\n", gender_count)

    gender_count.plot(kind='bar', color=['blue', 'orange'])
    plt.title('Розподіл співробітників за статтю')
    plt.xlabel('Стать')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.show()

def plot_age_group_count(data):
    """Підраховує і візуалізує кількість співробітників у вікових категоріях."""
    data['Вік'] = data['Дата народження'].apply(get_age)

    # Видалення рядків з None у стовпці 'Вік'
    data = data[data['Вік'].notna()]

    # Створення вікових категорій
    bins = [0, 17, 45, 70, 100]
    labels = ['0-17', '18-45', '46-70', '71+']
    data['Вікова група'] = pd.cut(data['Вік'], bins=bins, labels=labels)

    age_count = data['Вікова група'].value_counts()
    print("Кількість співробітників за віковими групами:\n", age_count)

    age_count.plot(kind='bar', color='green')
    plt.title('Вікові групи співробітників')
    plt.xlabel('Вікова група')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.show()

def plot_gender_age_distribution(data):
    """Підраховує і візуалізує кількість чоловіків і жінок у кожній віковій групі."""
    data['Вік'] = data['Дата народження'].apply(get_age)

    # Видалення рядків з None у стовпці 'Вік'
    data = data[data['Вік'].notna()]

    # Створення вікових категорій
    bins = [0, 17, 45, 70, 100]
    labels = ['0-17', '18-45', '46-70', '71+']
    data['Вікова група'] = pd.cut(data['Вік'], bins=bins, labels=labels)

    gender_age_count = data.groupby(['Вікова група', 'Стать']).size().unstack()
    print("Кількість співробітників за статтю у вікових групах:\n", gender_age_count)

    gender_age_count.plot(kind='bar', stacked=True)
    plt.title('Статевий розподіл за віковими групами')
    plt.xlabel('Вікова група')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.legend(title='Стать')
    plt.show()

def main():
    file_name = 'Serhii-table.csv'  # назва файлу
    data = read_csv(file_name)

    if data is not None:  # якщо дані успішно зчитано
        plot_gender_count(data)  # графік статевого розподілу
        plot_age_group_count(data)  # графік вікових груп
        plot_gender_age_distribution(data)  # графік статі за віковими групами

if __name__ == "__main__":
    main()  # запуск програми
