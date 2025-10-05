from app.events import Events
from core import Node, EventDispatcher

from queue import Queue


class NodeManager:
    def __init__(self, root: Node, dispatcher: EventDispatcher) -> None:
        """
        Класс для поиска узлов в дереве.

        :param root: Корневой узел дерева (Node)
        """
        self.root = root
        self.dispatcher = dispatcher

    def init(self) -> None:
        self.dispatcher.subscribe(Events.activate_node, self._activate_node)
        self.dispatcher.subscribe(Events.deactivate_node, self._deactivate_node)

    def deinit(self) -> None:
        self.dispatcher.unsubscribe(Events.activate_node, self._activate_node)
        self.dispatcher.unsubscribe(Events.deactivate_node, self._deactivate_node)

    def _activate_node(self, name: str) -> None:
        node = self._find_node(name)
        assert node
        node.activate()

    def _deactivate_node(self, name: str) -> None:
        node = self._find_node(name)
        assert node
        node.deactivate()

    def _find_node(self, name: str) -> Node | None:
        """
        Находит узел с заданным именем, используя BFS (обход в ширину).

        :param name: Имя узла, который нужно найти.
        :return: Найденный узел или None, если узел не найден.
        """
        queue = Queue()
        queue.put(self.root)
        
        while not queue.empty():
            current_node = queue.get()
            
            if current_node.name == name:
                return current_node
            
            for child in current_node.children:
                queue.put(child)
        
        return None  # Узел не найден
