import logging
from xml.dom.domreg import registered

from app.controllers.factory import Factory
from core import EventDispatcher
from core.nodes import node_tree_builder, build_tree_from_config
from core.nodes.node_manager import NodeManager

from data.models import User

from app import tree_config
from app.context import Context
from app.nodes.user_node import UserNode


logging.basicConfig(level=logging.DEBUG)


def main():
    event_dispatcher = EventDispatcher()

    users = {
        1: User(telegram_id=1, registered=True),
    }

    factory = Factory(users)

    context = Context(telegram_id=2, factory=factory)

    tree_root: UserNode = build_tree_from_config(tree_config.tree_config, event_dispatcher)
    tree_root.init(context)

    node_manager = NodeManager(tree_root, event_dispatcher)
    node_manager.init()

    tree_root.activate()

    # event_dispatcher.emit(Events.message_text, "Hello, world!")
    node_manager.handle({"type": "text", "text": "Hello, world!"})
    node_manager.handle({"type": "text", "text": "foo"})
    node_manager.handle({"type": "text", "text": "bar"})


if __name__ == '__main__':
    main()
