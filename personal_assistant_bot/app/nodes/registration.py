import logging

from app.nodes.interfaceses import IMessageTextHandler
from core import register_node_class
from core.nodes import IHandler

from .user_node import UserNode
from ..events import Events

logger = logging.getLogger(__name__)


@register_node_class
class Registration(UserNode, IMessageTextHandler):
    def __init__(self, dispatcher) -> None:
        super().__init__(dispatcher)
        self._registration_controller = None
    
    def init(self, context: IHandler) -> None:
        super().init(context)
        self._registration_controller = context.factory.get_registration_controller()

    def handle(self, *args, **kwargs) -> bool:
        if super().handle(*args, **kwargs):
            return True
        
        user = self._registration_controller.register_user(self._user_telegram_id)
        assert user is not None, f"User registration failed: {self._user_telegram_id}"
        logger.debug("HANDLED")
        
        self.dispatcher.emit(Events.activate_node, Registration2.__name__)

        return True


@register_node_class
class Registration2(Registration):
    def handle(self, *args, **kwargs) -> bool:
        logger.debug(f">>> {self.__class__.__name__}.handle(*{args}, **{kwargs})")
        self.dispatcher.emit(Events.activate_node, Registration3.__name__)
        return True


@register_node_class
class Registration3(Registration):
    def handle(self, *args, **kwargs) -> bool:
        logger.debug(f">>> {self.__class__.__name__}.handle(*{args}, **{kwargs})")
        self.dispatcher.emit(Events.deactivate_node, "Registration")
        return True
