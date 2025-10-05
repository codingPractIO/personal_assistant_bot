import logging

from app.events import Events
from .i_initable import IInitable
from core.nodes import IActivatable

from typing import TYPE_CHECKING


logger = logging.getLogger(__name__)


class IMessageTextHandler(IActivatable):
    if TYPE_CHECKING:
        from core import EventDispatcher
        dispatcher: EventDispatcher

    def activate(self) -> None:
        super().activate()
        self.dispatcher.subscribe(Events.message_text, self._handle_message)

    def deactivate(self) -> None:
        self.dispatcher.unsubscribe(Events.message_text, self._handle_message)
        super().deactivate()

    def _handle_message(self, message) -> None:
        logger.debug(f">>> {self.__class__.__name__}.handle_message({message})")
