from dataclasses import dataclass

from app.controllers import UserController


@dataclass
class Context:
    telegram_id: int
    user_controller: UserController
