import sys

import pygame
from pygame import Surface, time

from gui_game import GameScene
from gui_game_over import GameOverScene
from gui_main_menu import MainMenuScene
from theme import Theme


class Visualizer:
    """"""

    def __init__(
        self,
        theme: Theme,
    ) -> None:
        self.WIDTH = 960
        self.HEIGHT = 720
        self.theme: Theme = theme
        self.screen: Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.init()

    def run(self) -> None:
        """The full game visualisation"""
        pygame.display.set_caption("Pac-Man")
        running = True
        scenes = {
            "main_menu": MainMenuScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT)
            ),
            "game": GameScene(self.screen, self.theme, (self.WIDTH, self.HEIGHT)),
            "game_over": GameOverScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT)
            ),
        }
        current_scene = "main_menu"
        clock = time.Clock()
        while running:
            events = pygame.event.get()
            if any(event.type == pygame.QUIT for event in events):
                pygame.quit()
                sys.exit()
            next_scene = scenes[current_scene].handle_events(events)
            current_scene = next_scene

            scenes[current_scene].update()
            scenes[current_scene].draw()

            pygame.display.flip()
            clock.tick(50)
        pygame.quit()
