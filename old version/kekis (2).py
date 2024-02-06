import pickle

import face_recognition
import cv2
import sqlite3
import os

def connect_and_add_photo(name, photo_path):
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS faces
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    photo BLOB)''')

    with open(photo_path, 'rb') as file:
        image_data = file.read()

    cursor.execute("INSERT INTO faces (name, photo) VALUES (?, ?)", (name, image_data))
    print(f'Сотрудник {name} был добавлен')

    conn.commit()
    conn.close()

connect_and_add_photo('Yuriy', '../KnownFaces/Yuriy.jpg')
# Функция для проверки лица
def check_face_in_database(face_encoding):
    conn = sqlite3.connect("faces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faces")
    rows = cursor.fetchall()
    for row in rows:
        known_face_encoding = pickle.loads(row[1])
        result = face_recognition.compare_faces([known_face_encoding], face_encoding)
        if result[0]:
            return True
    return False

# Открытие вебкамеры
video_capture = cv2.VideoCapture(0)

while True:
    # Захват видеопотока
    ret, frame = video_capture.read()

    # Преобразование изображения в RGB формат
    rgb_frame = frame[:, :, ::-1]

    # Поиск всех лиц на кадре
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = [face_recognition.face_encodings(rgb_frame, [face], model="large")[0] for face in face_locations]

    for face_encoding in face_encodings:
        if check_face_in_database(face_encoding):
            cv2.putText(frame, "Открыть", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Закрыто", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Отображение результата
    cv2.imshow('Video', frame)

    # Выход при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Освобождение ресурсов
video_capture.release()
cv2.destroyAllWindows()