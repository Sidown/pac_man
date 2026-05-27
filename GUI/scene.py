from abc import ABC, abstractmethod
from pygame.event import Event


class Scene(ABC):
    """
    Abstract base class for all the scenes
    """
    @abstractmethod
    def handle_events(self, events: list[Event]) -> str:
        """
        process a list of events and return the name of the next scene
        arguments:
        events -> list of events to process
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Render the scene in the display surface
        """
        pass

    @abstractmethod
    def update(self) -> None:
        """
        Advance the scene logic frame per frame
        """
        pass
