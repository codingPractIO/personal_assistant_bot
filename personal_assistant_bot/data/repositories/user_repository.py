from data.models import User


class UserRepository:
    def __init__(self, users):
        self.__users: dict[int, User] = users

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.__users.get(telegram_id)

    def register(self, user: User) -> None:
        user.registered = True
        self.__users[user.telegram_id] = user
