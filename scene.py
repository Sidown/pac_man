from abc import ABC, abstractmethod
from pygame.event import Event


class Scene(ABC):
    @abstractmethod
    def handle_events(self, events: list[Event]) -> str:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
