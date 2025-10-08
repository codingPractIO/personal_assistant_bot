from core import EventDispatcher
from .node import Node
from .nodes_constants import CONSTRUCTOR, CHILDREN

NODE_CLASSES = {}


def register_node_class(cls):
    """
    Регистрирует класс узла для использования при построении дерева.
    """
    NODE_CLASSES[cls.__name__] = cls
    return cls


def build_tree_from_config(config, event_dispatcher: EventDispatcher | None = None) -> Node:
    """
    Рекурсивно строит дерево узлов из конфигурационного словаря.

    Parameters:
    - config: словарь с описанием дерева узлов (из YAML или JSON).

    Returns:
    - Корневой узел дерева.
    """

    assert CONSTRUCTOR in config, f"Node does not have '{CONSTRUCTOR}' field: {config}"
    node_constructor = config[CONSTRUCTOR]
    node_name = node_constructor.__name__

    # Double class creation protection BEGIN
    if not hasattr(build_tree_from_config, "class_counter"):
        setattr(build_tree_from_config, "class_counter", set())

    assert node_name not in build_tree_from_config.class_counter, f"Duplicate node class name '{node_name}' -> {config}"
    build_tree_from_config.class_counter.add(node_name)
    # Double class creation protection END

    # Создаём узел на основе его зарегистрированного класса
    root = node_constructor(event_dispatcher)
    for child_config in config.get("children", []):
        child_node = build_tree_from_config(child_config, event_dispatcher)
        root.add_child(child_node)

    return root
