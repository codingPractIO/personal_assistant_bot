from app.nodes.interfaceses import IMessageTextHandler
from core import Node, register_node_class


@register_node_class
class Root(Node, IMessageTextHandler):

    def __route_user(self, user):
        # Проверяем состояние пользователя
        if user.is_registered and user.is_authenticated:
            # Зарегистрирован и авторизован
            raise NotImplementedError
        elif user.is_registered:
            # Зарегистрирован, но не авторизован
            raise NotImplementedError
        else:
            # Не зарегистрирован
            raise NotImplementedError
