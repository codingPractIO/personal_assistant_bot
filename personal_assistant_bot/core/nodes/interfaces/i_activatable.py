from abc import ABC, abstractmethod


class IActivatable(ABC):
    @abstractmethod
    def activate(self) -> None:
        ...

    @abstractmethod
    def deactivate(self) -> None:
        ...
