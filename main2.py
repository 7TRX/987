import sqlite3  # Импортировать модуль для работы с базой данных SQLite
import numpy as np  # Импортировать модуль для работы с многомерными массивами и матрицами
import face_recognition  # Импортировать модуль для распознавания лиц
import cv2  # Импортировать модуль для компьютерного зрения
from TerminalController import *  # Импортировать класс для работы с турникетом
import os  # Импортировать модуль для работы с операционной системой
from datetime import datetime  # Импортировать модуль для работы со временем

turnstile = TurnstileController()  # Создать экземпляр класса для управления турникетом

def connect_and_add_photo(name, photo_path):
    conn = sqlite3.connect('employee.db')  # Подключиться к базе данных employee.db
    cursor = conn.cursor()  # Создать объект-курсор для выполнения SQL-запросов
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    photo BLOB)''')  # Создать таблицу employee, если она не существует
    with open(photo_path, 'rb') as file:  # Открыть файл с фотографией в бинарном режиме
        image_data = file.read()  # Прочитать данные изображения
    cursor.execute("INSERT INTO employee (name, photo) VALUES (?, ?)", (name, image_data))  # Вставить запись в таблицу employee
    print(f'Сотрудник {name} был добавлен')  # Вывести сообщение о добавлении сотрудника
    conn.commit()  # Закоммитить изменения в базе данных
    conn.close()  # Закрыть соединение с базой данных

#connect_and_add_photo('Uskova Lubov', 'KnownFaces/Uskova Lubov.jpg')  # Вызвать функцию для добавления фотографии сотрудника

conn = sqlite3.connect('employee.db')  # Подключиться к базе данных employee.db
c = conn.cursor()  # Создать объект-курсор для выполнения SQL-запросов
c.execute('''SELECT * FROM employee''')  # Выполнить запрос на выбор всех записей из таблицы employee
rows = c.fetchall()  # Получить все строки результата запроса

encodeListFromDB = []  # Создать пустой список для хранения кодировок лиц из базы данных
classNames = []  # Создать пустой список для хранения имен сотрудников
for row in rows:  # Для каждой строки результата запроса
    id, name, image_data = row  # Распаковать значения столбцов id, name и image_data
    classNames.append(name)  # Добавить имя сотрудника в список имен
    image_array = np.frombuffer(image_data, dtype=np.uint8)  # Преобразовать данные изображения в массив NumPy
    img = cv2.imdecode(image_array, 1)  # Декодировать изображение с помощью OpenCV
    encode = face_recognition.face_encodings(img)[0]  # Получить кодировку лица из изображения
    encodeListFromDB.append(encode)  # Добавить кодировку лица в список кодировок из базы данных

encodeListKnown = encodeListFromDB  # Присвоить список кодировок из базы данных переменной
print("Декодирование закончено")  # Вывести сообщение о завершении декодирования
cap = cv2.VideoCapture(0)  # Получить доступ к видеопотоку с камеры

while True:  # Бесконечный цикл
    success, img = cap.read()  # Получить следующий кадр из видеопотока
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Уменьшить размер изображения
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)  # Найти положения лиц на текущем кадре
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # Получить кодировки лиц с текущего кадра

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):  # Для каждой кодировки и положения лица
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # Сравнить кодировку лица с известными кодировками
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # Вычислить расстояние до известных лиц
        matchIndex = np.argmin(faceDis)  # Найти индекс наименьшего расстояния

        if matches[matchIndex]:  # Если найдено совпадение
            name = classNames[matchIndex]  # Получить имя сотрудника по индексу совпадения
            print(name)  # Вывести имя сотрудника
            y1, x2, y2, x1 = faceLoc  # Распаковать значения положения лица
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Увеличить размер области лица
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Нарисовать прямоугольник вокруг лица
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # Нарисовать прямоугольник для имени
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # Вывести имя сотрудника
            turnstile.open_turnstile()  # Открыть турникет
            time.sleep(0.1)  # Подождать 0.1 секунды
            turnstile.close_turnstile()  # Закрыть турникет

    cv2.imshow("WebCam", img)  # Показать изображение с наложенными прямоугольниками и именем
    cv2.waitKey(1)  # Ждать 1 миллисекунду