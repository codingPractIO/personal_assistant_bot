import logging

from core import register_node_class
from core.nodes import IHandler

from .user_node import UserNode


logger = logging.getLogger(__name__)


@register_node_class
class MainScreen(UserNode, IHandler):
    def handle(self, *args, **kwargs) -> bool:
        super().handle(*args, **kwargs)
        return True
