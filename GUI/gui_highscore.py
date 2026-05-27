import pygame
from pygame import Surface
from pygame.event import Event

from parser import Config

from .scene import Scene
from .score import HighScore
from .ui_elements.button import Button
from .ui_elements.theme import Theme


class HighScoreScene(Scene):
    """
    Scene that display the top 10 high scores
    """

    def __init__(
        self,
        screen: Surface,
        theme: Theme,
        width_height: tuple[int, int],
        config: Config,
        highscore: HighScore,
    ) -> None:
        """
        Initialise the highscore scene
        arguments:
        screen -> the pygame surface
        theme -> the visual theme
        width_height -> width and height of the window in pixels
        config -> game configuration
        highscore -> the highscore manager
        """
        self.current_scene = "high_score"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.config: Config = config
        self.highscore: HighScore = highscore

        self.btn_back_to_menu = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "Back to Main Menu",
            self._back_to_menu_callback,
            (50, 50),
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

    def _back_to_menu_callback(self) -> None:
        """
        return to the main menu
        """
        self.current_scene = "main_menu"

    def handle_events(self, events: list[Event]) -> str:
        """
        process a list of events and return the next scene to display
        arguments:
        events -> the list of events to process
        """
        self.current_scene = "high_score"
        for event in events:
            self.btn_back_to_menu.handle_event(event)
        return self.current_scene

    def update(self) -> None:
        """
        frame per frame logic, not needed in this scene
        """
        pass

    def _display_title(self) -> None:
        """
        Render the title of the screen
        """
        font = pygame.font.Font("assets/fonts/Retro Gaming.ttf", 42)
        displayed_title = font.render(
            "PacMac Highscore",
            False,
            self.theme.title_color,
        )
        self.screen.blit(
            displayed_title,
            ((self.WIDTH // 2) - (displayed_title.get_width() // 2), 135),
        )

    def _display_score(self) -> None:
        """
        Display the scores
        """
        font = font = pygame.font.Font("assets/fonts/Retro Gaming.ttf", 24)
        index = 1
        gap = 45
        for name, score in self.highscore.scores:
            displayed_score = font.render(
                f"{index}. {name} - {score}pts",
                False,
                self.theme.text_color,
            )
            self.screen.blit(
                displayed_score,
                (
                    (self.WIDTH // 2) - (displayed_score.get_width() // 2),
                    (175 + (index * gap)),
                ),
            )
            index += 1

    def draw(self) -> None:
        """
        Render the highscore scene
        """
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
        self._display_title()
        self._display_score()
