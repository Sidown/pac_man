import sys

import pygame
from pygame import Surface, time

from cheat import Cheat
from game import Game
from gui_game import GameScene
from gui_game_over import GameOverScene
from gui_highscore import HighScoreScene
from gui_instruction import InstructionScene
from gui_main_menu import MainMenuScene
from gui_victory import VictoryScene
from parser import Config, parser
from player import Player
from score import HighScore
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

        highscore: HighScore = HighScore()

        # charge la config
        config: Config = parser("json_file/config.json")
        nb_lives = config.lives
        spawn_x = config.levels[0]["width"] // 2
        spawn_y = config.levels[0]["height"] // 2

        # creer le player
        player: Player = Player(nb_lives, spawn_x, spawn_y)
        cheat: Cheat = Cheat()
        scenes = {
            "main_menu": MainMenuScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT)
            ),
            "game": GameScene(
                self.screen,
                self.theme,
                (self.WIDTH, self.HEIGHT),
                config,
                player,
                highscore,
                cheat,
            ),
            "game_over": GameOverScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT), player, highscore
            ),
            "instruction": InstructionScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT)
            ),
            "high_score": HighScoreScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT), config, highscore
            ),
            "victory": VictoryScene(
                self.screen, self.theme, (self.WIDTH, self.HEIGHT), player, highscore
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
            if current_scene != "game" and next_scene == "game":
                scenes["game"] = GameScene(
                    self.screen,
                    self.theme,
                    (self.WIDTH, self.HEIGHT),
                    config,
                    player,
                    highscore,
                    cheat,
                )
                scenes["game"].load_level()
            current_scene = next_scene

            scenes[current_scene].update()
            scenes[current_scene].draw()

            pygame.display.flip()
            clock.tick(50)
        pygame.quit()
