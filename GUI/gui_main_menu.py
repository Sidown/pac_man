import sys

import pygame
from pygame import Surface
from pygame.event import Event

from scene import Scene
from theme import Button, Text, Theme


class MainMenuScene(Scene):
    """
    The main menu scene
    """
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        """
        initialise the main menu scene
        arguments:
        screen -> the pygame surface
        theme -> the visual theme
        width_height -> the width and height of the screen in pixels
        """
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.current_scene = "main_menu"
        self.header = Text(
            self.screen,
            self.theme.header_size,
            self.theme.font_path,
            self.theme.title_color,
            self.theme.background_color,
            "PACMAN",
            ((self.WIDTH // 2), 50),
            True,
        )

        self.btn_game = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "New Game",
            self._game_callback,
            ((self.WIDTH // 2), 250),
            True,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        self.btn_high_score = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "View High Score",
            self._highscore_callback,
            ((self.WIDTH // 2), 350),
            True,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        self.btn_instruction = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "View Instructions",
            self._instruction_callback,
            ((self.WIDTH // 2), 450),
            True,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        self.btn_exit = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "Exit",
            self._exit_callback,
            ((self.WIDTH // 2), 550),
            True,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

    def _exit_callback(self) -> None:
        """
        Exit pygame
        """
        pygame.quit()
        sys.exit()

    def _game_callback(self) -> None:
        """
        Switch to the game scene
        """
        self.current_scene = "game"

    def _instruction_callback(self) -> None:
        """
        Switch to the instruction scene
        """
        self.current_scene = "instruction"

    def _highscore_callback(self) -> None:
        """
        Switch to the highscore scene
        """
        self.current_scene = "high_score"

    def handle_events(self, events: list[Event]) -> str:
        """
        Process a list of events and return the next scene to display
        arguments:
        events -> list of events to process
        """
        self.current_scene = "main_menu"
        for event in events:
            self.btn_game.handle_event(event)
            self.btn_high_score.handle_event(event)
            self.btn_instruction.handle_event(event)
            self.btn_exit.handle_event(event)
        return self.current_scene

    def update(self) -> None:
        """
        frame per frame logic, not needed in this scene
        """
        pass

    def draw(self) -> None:
        """
        Render the main menu scene
        """
        self.screen.fill(self.theme.background_color)
        self.header.draw(self.screen)
        self.btn_game.draw(self.screen)
        self.btn_high_score.draw(self.screen)
        self.btn_instruction.draw(self.screen)
        self.btn_exit.draw(self.screen)
