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

    def handle_events(self):
        return "game_over"

    def update(self):
        pass

    def draw(self, screen):
        self.screen.fill(self.theme.background_color)
        game_over_text = pygame.font.Font(self.theme.font_path, 56).render(
            "Game Over ... Fucki.. looser !!!!!", True, (255, 0, 100)
        )
        self.screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(
                    (self.WIDTH // 2),
                    (self.HEIGHT // 2),
                )
            ),
        )
