from queue import Queue

from app.events import Events
from core import Node, EventDispatcher
from .interfaces import IHandler


class NodeManager(IHandler):
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
    
    def handle(self, *args, **kwargs) -> bool:
        """
        todo:
            cache active branches on activate call of every node,
            because walking around tree on every message is too expensive.
        """
        result = False
        
        active_deepest_nodes = []
        
        # Use BFS to find the deepest active nodes
        queue = Queue()
        queue.put((self.root, 0))  # node and depth
        max_depth = -1
        
        while not queue.empty():
            current_node, depth = queue.get()
            
            if current_node.is_active:
                if depth > max_depth:
                    max_depth = depth
                    active_deepest_nodes = [current_node]
                elif depth == max_depth:
                    active_deepest_nodes.append(current_node)
            
            for child in current_node.children:
                queue.put((child, depth + 1))
        
        # Call handle method from child to parent for each node
        for node in active_deepest_nodes:
            current = node
            while current:
                if isinstance(current, IHandler):
                    if current.handle(*args, **kwargs):
                        break
                current = current.parent

        return result

    def _activate_node(self, name: str) -> None:
        node = self._find_node(name)
        assert node
        node.activate()

        while node.parent:
            node = node.parent
            if not node.is_active:
                node.activate()
            else:
                break

    def _deactivate_node(self, name: str) -> None:
        # todo: деактивировать в обратном порядке

        node = self._find_node(name)
        assert node

        s = [node]

        while s:
            node = s.pop()
            if node.is_active:
                node.deactivate()

            if node.children and any(c.is_active for c in node.children):
                s.extend(node.children)

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
