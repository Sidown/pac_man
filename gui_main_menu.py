import pygame
from pygame import Surface

from theme import Button, Text, Theme


class MainMenuScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height

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
            ((self.WIDTH // 2), 550),
            True,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

    def handle_events(self, events) -> str:
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if self.btn_game.rect.collidepoint(x, y):
                self.btn_game.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    return "game"
            if self.btn_high_score.rect.collidepoint(x, y):
                self.btn_high_score.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    return "high-score"
            if self.btn_instruction.rect.collidepoint(x, y):
                self.btn_instruction.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    return "instruction"
            if self.btn_exit.rect.collidepoint(x, y):
                self.btn_exit.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    return "quit"
        return "main_menu"

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.theme.background_color)
        self.header.draw(self.screen)
        self.btn_game.draw(self.screen)
        self.btn_high_score.draw(self.screen)
        self.btn_instruction.draw(self.screen)
        self.btn_exit.draw(self.screen)
