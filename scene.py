from abc import ABC, abstractmethod


class Scene(ABC):
    @abstractmethod
    def handle_events(self, events) -> str:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
