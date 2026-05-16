import sys

import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface, time

from ghost import Blinky, Clyde, Inky, Pinky, Player
from gui_game import GameScene
from gui_game_over import GameOverScene
from gui_main_menu import MainMenuScene
from pacgum import Pacgum, SuperPacgum
from theme import Theme


class Visualizer:
    """"""

    def __init__(
        self,
        maze: MazeGenerator,
        theme: Theme,
        blinky: Blinky,
        pinky: Pinky,
        inky: Inky,
        clyde: Clyde,
        player: Player,
        pacgums: dict[tuple[int], Pacgum],
        super_pacgums: dict[tuple[int], SuperPacgum],
    ) -> None:
        self.WIDTH = 960
        self.HEIGHT = 720
        self.PADDING = 80
        self.maze: MazeGenerator = maze
        self.theme: Theme = theme
        self.screen: Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.maze_height = len(self.maze.maze)
        self.maze_width = len(self.maze.maze[0])
        self.border_size = 5
        self.cell_width = (
            self.WIDTH - (2 * self.PADDING) - ((self.maze_width + 1) * self.border_size)
        ) / self.maze_width
        self.cell_height = (
            self.HEIGHT
            - (2 * self.PADDING)
            - ((self.maze_height + 1) * self.border_size)
        ) / self.maze_height
        self.player: Player = player
        self.player.skin = pygame.transform.scale(
            pygame.image.load(self.player.skin_path),
            (self.cell_width, self.cell_height),
        )
        self.vulnerable_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/ghosts/blue_ghost.png"),
            (self.cell_width, self.cell_height),
        )
        self.eyes_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/ghosts/eyes.png"),
            (self.cell_width, self.cell_height),
        )
        self.blinky: Blinky = blinky
        self.blinky_skin = pygame.transform.scale(
            pygame.image.load(self.blinky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.pinky: Pinky = pinky
        self.pinky_skin = pygame.transform.scale(
            pygame.image.load(self.pinky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.inky: Inky = inky
        self.inky_skin = pygame.transform.scale(
            pygame.image.load(self.inky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.clyde: Clyde = clyde
        self.clyde_skin = pygame.transform.scale(
            pygame.image.load(self.clyde.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.pacgums: dict[tuple[int], Pacgum] = pacgums
        self.pacgums_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/other/dot.png"),
            (self.cell_width, self.cell_height),
        )
        self.super_pacgums: dict[tuple[int], SuperPacgum] = super_pacgums
        self.super_pacgums_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/other/sdot.png"),
            (self.cell_width, self.cell_height),
        )

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
