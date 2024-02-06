import sqlite3


def connect_and_add_photo(name, photo_path):
    # Подключение к базе данных (если ее нет, она будет создана)
    conn = sqlite3.connect('employee.db')

    # Создание курсора для работы с базой
    cursor = conn.cursor()

    # Создание таблицы для лиц
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    photo BLOB)''')

    with open(photo_path, 'rb') as file:
        image_data = file.read()
    # Выполнение запроса на добавление новой записи в таблицу,
    # где photo_path - это путь к файлу с фотографией
    cursor.execute("INSERT INTO employee (name, photo) VALUES (?, ?)", (name, image_data))
    print(f'Сотрудник {name} был добавлен')

    # Выполнение команд и сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()


connect_and_add_photo('Uskova', 'KnownFaces/Uskova Lubov.jpg')



