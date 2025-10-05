import logging

from app.events import Events
from core import EventDispatcher
from core.nodes import node_tree_builder, build_tree_from_config
from app import tree_config


logging.basicConfig(level=logging.DEBUG)


def main():
    event_dispatcher = EventDispatcher()
    tree_root = build_tree_from_config(tree_config.tree_config, node_tree_builder.NODE_CLASSES, event_dispatcher)
    tree_root.activate()

    event_dispatcher.emit(Events.message_text, "Hello, world!")
    print()


if __name__ == '__main__':
    main()
