from data.models import User
from data.repositories import UserRepository


class UserController:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def get_by_telegram_id(self, telegram_id: int) -> User:
        return self._user_repository.get_by_telegram_id(telegram_id)
