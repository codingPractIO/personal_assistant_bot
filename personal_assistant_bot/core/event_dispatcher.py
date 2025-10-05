from typing import Callable, Dict, List


class EventDispatcher:
    def __init__(self):
        """
        Система управления событиями.
        """
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """
        Подписывает обработчик на событие.
        
        :param event_name: Название события.
        :param handler: Функция-обработчик события.
        """
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        if handler not in self.listeners[event_name]:
            self.listeners[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """
        Отписывает обработчик от события.

        :param event_name: Название события.
        :param handler: Функция-обработчик события.
        """
        if event_name in self.listeners:
            if handler in self.listeners[event_name]:
                self.listeners[event_name].remove(handler)
                if not self.listeners[event_name]:
                    del self.listeners[event_name]

    def emit(self, event_name: str, *args) -> None:
        """
        Публикует событие для всех подписчиков.
        
        :param event_name: Название события.
        :param args: Данные, связанные с событием.
        """
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(*args)
