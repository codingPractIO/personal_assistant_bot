from core import EventDispatcher
from .node import Node


NODE_CLASSES = {}


def register_node_class(cls):
    """
    Регистрирует класс узла для использования при построении дерева.
    """
    NODE_CLASSES[cls.__name__] = cls
    return cls


def build_tree_from_config(config, node_classes: dict, event_dispatcher: EventDispatcher | None = None) -> Node:
    """
    Рекурсивно строит дерево узлов из конфигурационного словаря.

    Parameters:
    - config: словарь с описанием дерева узлов (из YAML или JSON).

    Returns:
    - Корневой узел дерева.
    """
    node_name = config["name"]
    node_class = node_classes.get(node_name)
    if not node_class:
        raise ValueError(f"Unknown node class: {node_name}")
    
    # Создаём узел на основе его зарегистрированного класса
    root = node_class(event_dispatcher)
    for child_config in config.get("children", []):
        child_node = build_tree_from_config(child_config, node_classes)
        root.add_child(child_node)

    return root
