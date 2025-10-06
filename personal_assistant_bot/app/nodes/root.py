from app.events import Events
from core import register_node_class
from core.nodes import IHandler

from .user_node import UserNode
from ..context import Context


@register_node_class
class Root(UserNode, IHandler):
    def init(self, context: Context) -> None:
        super().init(context)

    def activate(self) -> None:
        super().activate()
        user = self._user_controller.get_by_telegram_id(self._user_telegram_id)
        if user:
            raise NotImplementedError("Registered")
        else:
            # Не зарегистрирован
            self.dispatcher.emit(Events.activate_node, "Registration")
