import pytest

from core import Node, EventDispatcher

from unittest.mock import Mock


def test_node_initialization(event_dispatcher):
    """Тест: Инициализация узла."""
    node = Node(event_dispatcher)
    
    assert not node.is_active  # Узел должен быть неактивен
    assert node.parent is None  # Родителя быть не должно
    assert node.children == []  # Дочерние узлы отсутствуют
    assert node.dispatcher is None  # Диспетчера нет по умолчанию


def test_add_child(event_dispatcher):
    """Тест: Добавление дочерних узлов."""
    parent = Node(event_dispatcher)
    child = Node(event_dispatcher)
    
    parent.add_child(child)
    
    assert len(parent.children) == 1  # У родителя появился один ребёнок
    assert parent.children[0] == child  # Это тот же узел, что мы добавили
    assert child.parent == parent  # Ребёнок знает о своём родителе


def test_parent_activation(event_dispatcher):
    """Тест: Активация узла активирует всех родителей."""
    root = Node(event_dispatcher)
    child = Node(event_dispatcher)
    grandchild = Node(event_dispatcher)
    
    # Формируем дерево: root -> child -> grandchild
    root.add_child(child)
    child.add_child(grandchild)
    
    # Активируем самый глубокий уровень
    grandchild.activate()
    
    # Проверяем, что все узлы активировались в процессе
    assert grandchild.is_active  # Сам узел активен
    assert child.is_active  # Родитель активен
    assert root.is_active  # Корень активен


def test_children_deactivation(event_dispatcher):
    """Тест: Деактивация узла деактивирует всех детей."""
    root = Node(event_dispatcher)
    child = Node(event_dispatcher)
    grandchild = Node(event_dispatcher)
    
    # Формируем дерево: root -> child -> grandchild
    root.add_child(child)
    child.add_child(grandchild)
    
    # Активируем весь путь
    grandchild.activate()
    
    # Проверяем активацию
    assert root.is_active
    assert child.is_active
    assert grandchild.is_active
    
    # Деактивируем корень
    root.deactivate()
    
    # Проверяем, что все узлы деактивировались
    assert not root.is_active
    assert not child.is_active
    assert not grandchild.is_active


def test_dispatcher_events(event_dispatcher):
    """Тест: События через диспетчер."""
    mock_dispatcher = Mock(event_dispatcher)
    node = Node(dispatcher=mock_dispatcher)
    
    # Активируем узел
    node.activate()
    
    # Проверяем, что событие активации было отправлено
    mock_dispatcher.emit.assert_called_with("NODE_ACTIVATED", {"node_name": node.name})
    
    # Сбрасываем mock и деактивируем узел
    mock_dispatcher.reset_mock()
    node.deactivate()
    
    # Проверяем, что событие деактивации было отправлено
    mock_dispatcher.emit.assert_called_with("NODE_DEACTIVATED", {"node_name": node.name})


def test_readable_tree(event_dispatcher):
    """Тест: Текстовое представление дерева."""
    root = Node(event_dispatcher)
    child1 = Node(event_dispatcher)
    child2 = Node(event_dispatcher)
    grandchild = Node(event_dispatcher)
    
    # Формируем дерево
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)
    
    # Активируем часть дерева
    grandchild.activate()
    
    # Ожидаемое текстовое представление
    expected_tree = (
        "[ACTIVE] Node\n"
        "    [ACTIVE] Node\n"
        "        [ACTIVE] Node\n"
        "    [INACTIVE] Node\n"
    )
    
    assert root.to_readable_tree() == expected_tree
