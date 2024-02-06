import time


class TurnstileController:
    def __init__(self):
        self.is_open = False  # Изначально турникет закрыт

    def open_turnstile(self):
        if not self.is_open:  # Проверяем, не открыт ли уже турникет
            print("Открываем турникет")
            # Код для активации механизма открытия турникета (например, сигнал к исполнительному устройству)
            time.sleep(1)  # Небольшая задержка для имитации времени открытия
            print("Турникет открыт")
            self.is_open = True

    def close_turnstile(self):
        if self.is_open:  # Проверяем, не закрыт ли уже турникет
            print("Закрываем турникет")
            # Код для активации механизма закрытия турникета (например, сигнал к исполнительному устройству)
            time.sleep(1)  # Небольшая задержка для имитации времени закрытия
            print("Турникет закрыт")
            self.is_open = False


# Пример использования
if __name__ == "__main__":
    turnstile = TurnstileController()

    # Предположим, что здесь у вас есть вызовы функций распознавания лиц и получения результата
    recognized_person = True  # Предположим, что лицо успешно распознано

    if recognized_person:
        turnstile.open_turnstile()  # Если лицо распознано, открываем турникет
        time.sleep(5)
        turnstile.close_turnstile()
