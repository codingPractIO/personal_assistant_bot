from app.events import Events
from app.nodes.interfaceses import IMessageTextHandler
from core import register_node_class

from .user_node import UserNode
from ..context import Context
from ..controllers import UserController


@register_node_class
class Root(UserNode, IMessageTextHandler):
    
    def init(self, context: Context) -> None:
        super().init(context)

    def activate(self) -> None:
        super().activate()
        user = self._user_controller.get_by_telegram_id(self._user_telegram_id)
        if user:
            raise NotImplementedError("Registered")
            # self.dispatcher.emit(Events.activate_registration)
        else:
            # Не зарегистрирован
            self.dispatcher.emit(Events.activate_node, "Registration")
            # raise NotImplementedError("Not registered yet")
