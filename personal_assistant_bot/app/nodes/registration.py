from app.nodes.interfaceses import IMessageTextHandler
from core import Node, register_node_class


@register_node_class
class Registration(Node, IMessageTextHandler):
    pass
