import logging
from typing import Callable


logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self):
        """
        Система управления событиями.
        """
        self.listeners: dict[str, list[Callable]] = {}
    
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

    def emit(self, event_name: str, *args, **kwargs) -> None:
        """
        Публикует событие для всех подписчиков.
        
        :param event_name: Название события.
        :param args: Данные, связанные с событием.
        """
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    logger.error(f"{self.__class__.__name__}.emit({event_name}, {args=}, {kwargs=}) -> {e.__class__.__name__}: {e}")
                    raise
