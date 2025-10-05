from app.nodes.interfaceses import IMessageTextHandler
from core import register_node_class

from .user_node import UserNode


@register_node_class
class Registration(UserNode, IMessageTextHandler):
    pass
