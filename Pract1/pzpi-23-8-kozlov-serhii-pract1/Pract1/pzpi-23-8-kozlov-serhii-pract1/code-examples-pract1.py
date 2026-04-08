from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

class Publisher:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        print("\n[Publisher] Сповіщаю всіх підписників про нову подію...")
        for observer in self._observers:
            observer.update(message)

    def do_business_logic(self) -> None:
        print("\n[Publisher] Виконую важливу бізнес-логіку: Створено нового користувача.")
        self.notify("Користувача 'JohnDoe' успішно зареєстровано.")

class EmailSubscriber(Observer):
    def update(self, message: str) -> None:
        print(f"EmailSubscriber: Відправлено email з текстом: {message}")

class PushSubscriber(Observer):
    def update(self, message: str) -> None:
        print(f"PushSubscriber: Відображено push-сповіщення: {message}")

if __name__ == "__main__":
    publisher = Publisher()

    email_sub = EmailSubscriber()
    push_sub = PushSubscriber()

    publisher.attach(email_sub)
    publisher.attach(push_sub)

    publisher.do_business_logic()
