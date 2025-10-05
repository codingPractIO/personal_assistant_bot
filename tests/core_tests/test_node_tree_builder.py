import pytest
from core.nodes.node_tree_builder import register_node_class, build_tree_from_config, NODE_CLASSES
from core import Node
from app import tree_config  # Импортируем конфигурацию


# Создаём фиктивные классы для регистрации узлов
class RootNode(Node):
    pass


class ChildNode(Node):
    pass


class GrandchildNode1(Node):
    pass


class GrandchildNode2(Node):
    pass


class GrandchildNode3(Node):
    pass


# Pytest-фикстура для очистки реестра NODE_CLASSES перед каждым тестом
@pytest.fixture(autouse=True)
def node_classes():
    NODE_CLASSES.clear()
    return {
        c.__name__: c
        for c in (
            RootNode,
            ChildNode,
            GrandchildNode1,
            GrandchildNode2,
            GrandchildNode3,
        )
    }
    
TEST_CONFIG = {
    "name": "RootNode",  # Имя корневого узла (класс)
    "children": [
        {
            "name": "ChildNode",  # Дочерний узел 1
            "children": [
                {"name": "GrandchildNode1"},  # Внучатый узел 1-1
                {"name": "GrandchildNode2"}  # Внучатый узел 1-2
            ],
        },
        {
            "name": "ChildNode",  # Дочерний узел 2
            "children": [
                {"name": "GrandchildNode3"}  # Внучатый узел 2-1
            ],
        },
    ],
}

def test_build_tree_from_config(node_classes):
    """Тест: Построение дерева из конфигурации."""
    
    # Строим дерево из конфигурации
    tree = build_tree_from_config(TEST_CONFIG, node_classes)
    
    # Проверяем, что корневой узел — тип RootNode
    assert isinstance(tree, RootNode)
    
    # Проверяем, что у корневого узла 2 дочерних элемента
    assert len(tree.children) == 2
    
    # Проверяем, что первый дочерний узел правильно построен
    child1 = tree.children[0]
    assert isinstance(child1, ChildNode)
    assert len(child1.children) == 2  # У первого узла 2 потомка
    
    # Проверяем, что второй дочерний узел правильно построен
    child2 = tree.children[1]
    assert isinstance(child2, ChildNode)
    assert len(child2.children) == 1  # У второго узла 1 потомок


def check_tree_structure(node, config):
    """
    Проверяет, что структура узла соответствует конфигурации.

    :param node: Узел дерева, который нужно проверить.
    :param config: Подобъект конфигурации, которому узел должен соответствовать.
    """
    # Проверяем, что имя узла совпадает с указанным в конфиге
    assert node.__class__.__name__ == config["name"], \
        f"Имя узла {node.__class__.__name__} не соответствует ожидаемому {config['name']}"
    
    # Проверяем, что количество детей соответствует конфигурации
    expected_children = config.get("children", [])
    assert len(node.children) == len(expected_children), \
        f"У {node.__class__.__name__} должно быть {len(expected_children)} дочерних элементов, найдено {len(node.children)}"
    
    # Рекурсивно проверяем все дочерние узлы
    for child_node, child_config in zip(node.children, expected_children):
        check_tree_structure(child_node, child_config)


def test_tree_structure(node_classes):
    """Тест: структура построенного дерева соответствует конфигурации."""
    tree = build_tree_from_config(TEST_CONFIG, node_classes)  # Создаём дерево на основе конфигурации
    
    # Проверяем, что структура дерева соответствует конфигурации
    check_tree_structure(tree, TEST_CONFIG)


def test_invalid_node_class(node_classes):
    """Тест: Обработка ошибок с некорректным именем узла."""
    invalid_config = {
        "name": "UnknownNode",  # Некорректное имя узла
        "children": []
    }
    
    # Проверяем, что при попытке построить дерево выбрасывается исключение
    with pytest.raises(ValueError, match="Unknown node class: UnknownNode"):
        build_tree_from_config(invalid_config, node_classes)


def test_invalid_structure(node_classes):
    """Тест: Неверное имя узла выбрасывает ValueError."""
    invalid_config = {
        "name": "UnknownNode",  # Неизвестное имя узла
        "children": []
    }
    
    with pytest.raises(ValueError, match="Unknown node class: UnknownNode"):
        build_tree_from_config(invalid_config, node_classes)


def test_empty_tree(node_classes):
    """Тест: Пустая конфигурация создаёт дерево без детей."""
    empty_config = {"name": "RootNode", "children": []}
    tree = build_tree_from_config(empty_config, node_classes)
    
    # Проверяем, что корневой узел создан корректно, но без детей
    assert isinstance(tree, RootNode)
    assert len(tree.children) == 0
