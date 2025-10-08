from app.events import Events
from core import register_node_class
from core.nodes import IHandler

from .user_node import UserNode
from ..context import Context


@register_node_class
class Root(UserNode, IHandler):
    def __init__(self, dispatcher) -> None:
        super().__init__(dispatcher)
        self._registration_controller = None

    def init(self, context: Context) -> None:
        super().init(context)
        self._registration_controller = context.factory.get_registration_controller()
    
    def activate(self) -> None:
        super().activate()
        user = self._registration_controller.get_by_telegram_id(self._user_telegram_id)

        # Если пользователь существует и он зарегистрирован — ведём на главный экран
        if user and getattr(user, "registered", False):
            self.dispatcher.emit(Events.activate_node, "MainScreen")
        else:
            # Нет пользователя или не зарегистрирован — ведём в регистрацию
            self.dispatcher.emit(Events.activate_node, "Registration")

    def handle(self, *args, **kwargs) -> bool:
        # Как корневой узел по умолчанию ничего не перехватываем,
        # чтобы не мешать обработке в ветках
        return False
