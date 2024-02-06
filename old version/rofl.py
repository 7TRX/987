import cv2
import dlib

# Загрузка модели распознавания лиц
detector = dlib.get_frontal_face_detector()

# Загрузка модели предсказания ключевых точек лица
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Открытие видеопотока из камеры
video_capture = cv2.VideoCapture(0)

while True:
    # Получение кадра из видеопотока
    ret, frame = video_capture.read()

    # Перевод кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц на кадре
    faces = detector(gray)

    # Цикл по обнаруженным лицам
    for face in faces:
        # Определение ключевых точек лица
        landmarks = predictor(gray, face)

        # Визуализация ключевых точек лица
        for i in range(68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Отображение кадра с распознанными лицами
    cv2.imshow('Video', frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
video_capture.release()
cv2.destroyAllWindows()
