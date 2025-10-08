from data.models import User
from data.repositories import UserRepository


class RegistrationController:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self._user_repository.get_by_telegram_id(telegram_id)

    def register_user(self, telegram_id: int) -> User:
        assert isinstance(telegram_id, int), f"Invalid telegram_id: {telegram_id}"
        assert self.get_by_telegram_id(telegram_id) is None, f"User already registered: {telegram_id}"

        user = User(telegram_id=telegram_id)
        self._user_repository.register(user)
        return user
