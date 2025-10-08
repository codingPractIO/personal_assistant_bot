from dataclasses import dataclass

from core.controllers import IFactory


@dataclass
class Context:
    telegram_id: int
    factory: IFactory
