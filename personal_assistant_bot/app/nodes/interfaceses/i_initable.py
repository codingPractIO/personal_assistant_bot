from abc import ABC, abstractmethod

class IInitable(ABC):
    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def deinit(self) -> None:
        ...
