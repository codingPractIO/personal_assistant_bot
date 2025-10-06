import logging

from app.nodes.interfaceses import IMessageTextHandler
from core import register_node_class
from core.nodes import IHandler

from .user_node import UserNode


logger = logging.getLogger(__name__)


@register_node_class
class Registration(UserNode, IMessageTextHandler):
    def handle(self, *args, **kwargs) -> bool:
        if super().handle(*args, **kwargs):
            return True
        logger.debug("HANDLED")
        return True
