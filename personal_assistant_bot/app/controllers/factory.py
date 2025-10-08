from core.controllers.factory import IFactory

from data.repositories import UserRepository

from .registration_controller import (
    RegistrationController,
)

class Factory(IFactory):
    def __init__(self, users: dict):
        super().__init__()
        self._user_repository = UserRepository(users)

    def get_registration_controller(self) -> RegistrationController:
        return RegistrationController(self._user_repository)
