import sqlite3
import numpy as np
import face_recognition
import cv2
import os
from datetime import datetime

def connect_and_add_photo(name, photo_path):
    conn = sqlite3.connect('../employee.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    photo BLOB)''')
    with open(photo_path, 'rb') as file:
        image_data = file.read()
    cursor.execute("INSERT INTO employee (name, photo) VALUES (?, ?)", (name, image_data))
    print(f'Сотрудник {name} был добавлен')
    conn.commit()
    conn.close()

connect_and_add_photo('Lyarva', '../KnownFaces/Lyarva.jpg')

conn = sqlite3.connect('../employee.db')
c = conn.cursor()
c.execute('''SELECT * FROM employee where name = "Yuriy"''')
rows = c.fetchall()


encodeListFromDB = []
for row in rows:
    id, name, image_data = row
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    img = cv2.imdecode(image_array, 1)  # Декодируйте изображение
    encode = face_recognition.face_encodings(img)[0]
    encodeListFromDB.append(encode)

classNames = name
encodeListKnown = encodeListFromDB
print("Декодирование закончено")
print(row)