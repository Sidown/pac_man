import pygame
from pygame import Surface
from pygame.event import Event

from game_class.player import Player

from .scene import Scene
from .score import HighScore
from .ui_elements.button import Button
from .ui_elements.highscore_input import HighScoreInput
from .ui_elements.theme import Theme


class GameOverScene(Scene):
    """
    Scene displayed when the player loose.
    """

    def __init__(
        self,
        screen: Surface,
        theme: Theme,
        width_height: tuple[int, int],
        player: Player,
        highscore: HighScore,
    ) -> None:
        """
        Initialise the game over scene
        arguments:
        screen -> the pygame surface
        theme -> the visual theme
        width_height -> width and height of the window in pixels
        player -> the player
        highscore -> the highscore manager
        """
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.player: Player = player
        self.highscore: HighScore = highscore
        self.PADDING = 80
        self.current_scene = "game_over"
        self.game_over_text = pygame.font.Font(self.theme.font_path,
                                               56).render(
            "Game Over ... looser !!!!!", True, (255, 0, 100)
        )
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
        self.text_input_name = HighScoreInput(
            self.screen,
            (self.WIDTH // 2, self.HEIGHT // 2 + 150),
            250,
            60,
            self.player,
            self.highscore,
        )

    def _back_to_menu_callback(self) -> None:
        """
        reset the player and return to the main menu
        """
        self.player.new_game()
        self.highscore.current_score = 0
        self.current_scene = "main_menu"

    def handle_events(self, events: list[Event]) -> str:
        """
        Process a list of events and return the name of the next scene
        arguments:
        events -> list of events to process
        return value:
        the next scene to display
        """
        self.current_scene = "game_over"
        is_completed_name = False
        for event in events:
            self.btn_back_to_menu.handle_event(event)
            is_completed_name = self.text_input_name.handle_event(event)
        if is_completed_name:
            self.player.new_game()
            self.highscore.current_score = 0
            return "main_menu"
        return self.current_scene

    def update(self) -> None:
        """
        Update frame by frame, not needed in this scene
        """
        pass

    def draw(self) -> None:
        """
        Render the game over screen
        """
        self.screen.fill(self.theme.background_color)
        self.btn_back_to_menu.draw(self.screen)
        self.text_input_name.draw()
        self.screen.blit(
            self.game_over_text,
            self.game_over_text.get_rect(
                center=(
                    (self.WIDTH // 2),
                    (self.HEIGHT // 2),
                )
            ),
        )
        player_score_text = pygame.font.Font(self.theme.font_path, 28).render(
            f"your score: {self.highscore.current_score}pts",
            False,
            self.theme.text_color,
        )
        self.screen.blit(
            player_score_text,
            (
                (self.WIDTH // 2) - (player_score_text.get_width() // 2),
                self.HEIGHT // 2 + 70,
            ),
        )
