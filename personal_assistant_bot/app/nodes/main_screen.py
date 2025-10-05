from core import register_node_class

from .user_node import UserNode


@register_node_class
class MainScreen(UserNode):
    pass
