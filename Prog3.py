import pandas as pd 
import matplotlib.pyplot as plt  
from datetime import datetime  
import os  

def read_csv(file_name):
    """Зчитує CSV файл і повертає DataFrame."""
    try:
        data_frame = pd.read_csv(file_name)
        print("Файл успішно відкрито.")
        return data_frame
    except FileNotFoundError:
        print("Неможливо відкрити CSV файл.")
        exit()
    except Exception as e:
        print(f"Помилка при читанні файлу CSV: {e}")
        exit()

def calculate_age(data_frame):
    """Додає стовпець з віком до DataFrame."""
    current_date = datetime.now()
    data_frame['Дата народження'] = pd.to_datetime(data_frame['Дата народження'], errors='coerce', format='%d.%m.%Y')
    
    data_frame['Вік'] = data_frame['Дата народження'].apply(
        lambda dob: current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day)) if pd.notnull(dob) else None
    )
    return data_frame

def plot_gender_count(data_frame):
    """Підраховує і візуалізує кількість чоловіків і жінок."""
    gender_counts = data_frame['Стать'].value_counts()
    print("Кількість співробітників за статтю:\n", gender_counts)

    gender_counts.plot(kind='bar', color=['purple', 'orange'])
    plt.title('Розподіл співробітників за статтю')
    plt.xlabel('Стать')
    plt.ylabel('Кількість')
    plt.xticks(rotation=0)
    plt.show()

def plot_age_group_count(data_frame):
    """Підраховує і візуалізує кількість співробітників у вікових категоріях."""
    age_categories = {
        '0-17': data_frame[data_frame['Вік'] < 18],
        '18-45': data_frame[(data_frame['Вік'] >= 18) & (data_frame['Вік'] <= 45)],
        '46-70': data_frame[(data_frame['Вік'] > 45) & (data_frame['Вік'] <= 70)],
        '71+': data_frame[data_frame['Вік'] > 70]
    }

    age_category_counts = {category: len(data) for category, data in age_categories.items()}
    print("\nКількість співробітників у кожній віковій категорії:")
    for category, count in age_category_counts.items():
        print(f"{category}: {count}")

    plt.bar(age_category_counts.keys(), age_category_counts.values(), color=['red', 'lightgreen', 'gray', 'yellow'])
    plt.title('Кількість співробітників за віковими категоріями')
    plt.xlabel('Вікова категорія')
    plt.ylabel('Кількість')
    plt.xticks(rotation=45)
    plt.show()

def plot_gender_age_distribution(data_frame):
    """Візуалізує кількість чоловіків і жінок у кожній віковій категорії."""
    age_categories = {
        'вік 0-17': data_frame[data_frame['Вік'] < 18],
        'вік 18-45': data_frame[(data_frame['Вік'] >= 18) & (data_frame['Вік'] <= 45)],
        'вік46-70': data_frame[(data_frame['Вік'] > 45) & (data_frame['Вік'] <= 70)],
        'вік71+': data_frame[data_frame['Вік'] > 70]
    }

    print("\nКількість співробітників жіночої та чоловічої статі у кожній віковій категорії:")
    for category, data in age_categories.items():
        gender_counts_in_category = data['Стать'].value_counts()
        print(f"{category}:")
        print(gender_counts_in_category)

        if not gender_counts_in_category.empty:
            gender_counts_in_category.plot(
                kind='pie',
                autopct='%1.1f%%',
                colors=['magenta', 'cyan'],
                labels=gender_counts_in_category.index.tolist(),
                startangle=90
            )
            plt.title(f'Стать співробітників у віковій категорії: {category}')
            plt.ylabel('')
            plt.axis('equal')
            plt.show()
        else:
            print(f"У категорії {category} немає даних.")

def main():
    file_name = 'Serhii-table.csv'  # назва файлу
    data_frame = read_csv(file_name)

    # Розрахунок віку
    data_frame = calculate_age(data_frame)

    if data_frame is not None: 
        plot_gender_count(data_frame)  # графік статевого розподілу
        plot_age_group_count(data_frame)  # графік вікових груп
        plot_gender_age_distribution(data_frame)  # графік статі за віковими групами

if __name__ == "__main__":
    main()  
