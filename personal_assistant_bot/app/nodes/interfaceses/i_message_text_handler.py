import logging

from app.events import Events
from .i_initable import IInitable
from core.nodes import IActivatable, IHandler

from typing import TYPE_CHECKING


logger = logging.getLogger(__name__)


class IMessageTextHandler(IHandler):
    def handle(self, message, *args, **kwargs) -> bool:
        if message['type'] != 'text':
            return True
        return False

    def _handle_message(self, message) -> None:
        logger.debug(f">>> {self.__class__.__name__}.handle_message({message})")
