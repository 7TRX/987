import sqlite3
import numpy as np
import face_recognition
import cv2
from TerminalController import *
import os
from datetime import datetime
turnstile = TurnstileController()


def connect_and_add_photo(name, photo_path):
    conn = sqlite3.connect('employee.db')
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


#connect_and_add_photo('Uskova Lubov', 'KnownFaces/Uskova Lubov.jpg')

conn = sqlite3.connect('employee.db')
c = conn.cursor()
c.execute('''SELECT * FROM employee''')
rows = c.fetchall()


encodeListFromDB = []
classNames = []
for row in rows:
    id, name, image_data = row
    classNames.append(name)
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    img = cv2.imdecode(image_array, 1)  # Декодируйте изображение
    encode = face_recognition.face_encodings(img)[0]
    encodeListFromDB.append(encode)

encodeListKnown = encodeListFromDB
print("Декодирование закончено")
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex]
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            turnstile.open_turnstile()
            time.sleep(0.1)
            turnstile.close_turnstile()


    cv2.imshow("WebCam", img)
    cv2.waitKey(1)