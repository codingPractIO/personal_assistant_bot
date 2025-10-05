from core import Node, EventDispatcher
from app.controllers import UserController

from ..context import Context


class UserNode(Node):
    def __init__(self, dispatcher: EventDispatcher) -> None:
        super().__init__(dispatcher)
        self._user_telegram_id: int | None = None
        self._user_controller: UserController | None = None

    def init(self, context: Context) -> None:
        self._user_telegram_id = context.telegram_id
        self._user_controller = context.user_controller
        
        for child in self.children:
            child.init(context)
