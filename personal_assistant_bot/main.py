import logging
from xml.dom.domreg import registered

from core import EventDispatcher
from core.nodes import node_tree_builder, build_tree_from_config
from core.nodes.node_manager import NodeManager

from data.models import User
from data.repositories import UserRepository

from app import tree_config
from app.events import Events
from app.context import Context
from app.nodes.user_node import UserNode
from app.controllers import UserController


logging.basicConfig(level=logging.DEBUG)


def main():
    event_dispatcher = EventDispatcher()

    users = {
        1: User(telegram_id=1, registered=True),
    }

    user_repository = UserRepository(users)
    user_controller = UserController(user_repository)  # or InitController?
    context = Context(telegram_id=1, user_controller=user_controller)

    tree_root: UserNode = build_tree_from_config(tree_config.tree_config, node_tree_builder.NODE_CLASSES, event_dispatcher)
    tree_root.init(context)

    node_manager = NodeManager(tree_root, event_dispatcher)
    node_manager.init()

    tree_root.activate()

    # event_dispatcher.emit(Events.message_text, "Hello, world!")
    node_manager.handle({"type": "text", "text": "Hello, world!"})


if __name__ == '__main__':
    main()
