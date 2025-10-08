import logging
from core import EventDispatcher
from core.nodes.interfaces import IActivatable


logger = logging.getLogger(__name__)


class Node(IActivatable):
    """
    Представляет узел дерева состояний.

    Правила:
    - Активация узла автоматически активирует всех его родителей.
    - Деактивация узла автоматически деактивирует всех его детей.
    """
    
    def __init__(self, dispatcher: EventDispatcher | None):
        self.__is_active = False
        self.parent = None
        self.children = []
        self.dispatcher = dispatcher
    
    @property
    def is_active(self):
        return self.__is_active
    
    @property
    def name(self):
        return self.__class__.__name__
    
    def add_child(self, child_node):
        """Добавляет потомка и устанавливает родительскую связь."""
        child_node.parent = self
        self.children.append(child_node)

    def activate(self) -> None:
        """Активирует узел и рекурсивно активирует всех родителей."""
        super().activate()
        logger.debug(f"{self.__class__.__name__} ACTIVATED")

        self.__is_active = True
        
        # Уведомляем через диспетчер
        if self.dispatcher:
            self.dispatcher.emit("NODE_ACTIVATED", {"node_name": self.name})

    def deactivate(self) -> None:
        """Деактивирует узел и рекурсивно деактивирует детей."""
        if not self.__is_active:
            return
        super().deactivate()
        logger.debug(f"{self.__class__.__name__} DEACTIVATED")

        self.__is_active = False
        
        # Уведомляем через диспетчер
        if self.dispatcher:
            self.dispatcher.emit("NODE_DEACTIVATED", {"node_name": self.name})

    def to_readable_tree(self, level=0):
        """
        Возвращает текстовое представление дерева узлов, начиная с текущего узла.

        Parameters:
        - level: уровень вложенности (для отступов).

        Returns:
        - Текстовая строка, отображающая дерево состояния узлов.
        """
        # Генерируем строку для текущего узла
        state = "[ACTIVE]" if self.is_active else "[INACTIVE]"
        result = f"{' ' * (level * 4)}{state} {self.name}\n"
        
        # Добавляем потомков (рекурсивно)
        for child in self.children:
            result += child.to_readable_tree(level + 1)
        
        return result
