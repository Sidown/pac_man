import pygame
from pygame import Surface

from scene import Scene
from theme import Button, TextInput, Theme


class GameOverScene(Scene):
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.PADDING = 80
        self.current_scene = "game_over"
        self.game_over_text = pygame.font.Font(self.theme.font_path, 56).render(
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
        self.text_input_name = TextInput(self.screen, (350, self.WIDTH // 2), 250, 60)

    def _back_to_menu_callback(self) -> None:
        self.current_scene = "main_menu"

    def handle_events(self, events) -> str:
        self.current_scene = "game_over"
        for event in events:
            self.btn_back_to_menu.handle_event(event)
            self.text_input_name.handle_event(event)
        return self.current_scene

    def update(self):
        pass

    def draw(self):
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
