import pygame
from pygame import Surface

from theme import Theme


class GameOverScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.PADDING = 80
        self.game_over_text = pygame.font.Font(self.theme.font_path, 56).render(
            "Game Over ... looser !!!!!", True, (255, 0, 100)
        )

    def handle_events(self, events):
        return "game_over"

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.theme.background_color)
        self.screen.blit(
            self.game_over_text,
            self.game_over_text.get_rect(
                center=(
                    (self.WIDTH // 2),
                    (self.HEIGHT // 2),
                )
            ),
        )
