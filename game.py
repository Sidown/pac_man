import random

from mazegenerator.mazegenerator import MazeGenerator

from ghost import Blinky, Clyde, Ghost, Inky, Pinky
from not_corner import not_corner
from pacgum import Pacgum, SuperPacgum
from parser import Config
from player import Player


class Level:
    def __init__(
        self,
        size: tuple[int],
        pacgum_points: int,
        super_pacgum_points: int,
        cell_width: int,
        cell_height: int,
        seed: float,
        player: Player,
    ) -> None:
        self.maze: MazeGenerator = MazeGenerator(size, seed=seed)
        self.pacgums: dict[tuple[int], Pacgum] = {}
        self.player = player
        for y, row in enumerate(self.maze.maze):
            for x, _ in enumerate(row):
                if (
                    self.maze.maze[y][x] != 15
                    and not_corner(self.maze, x, y)
                    and (x, y)
                    != (len(self.maze.maze[0]) // 2, len(self.maze.maze) // 2)
                ):
                    self.pacgums.update(
                        {
                            (x, y): Pacgum(
                                pacgum_points,
                                (x, y),
                                "./assets/skin/other/dot.png",
                                cell_width,
                                cell_height,
                            )
                        }
                    )

        super_pacgums_coord = [
            (0, 0),
            (0, len(self.maze.maze) - 1),
            (len(self.maze.maze[0]) - 1, 0),
            (len(self.maze.maze[0]) - 1, len(self.maze.maze) - 1),
        ]
        self.super_pacgums: dict[tuple[int], SuperPacgum] = {}
        for coord in super_pacgums_coord:
            self.super_pacgums.update(
                {
                    coord: SuperPacgum(
                        super_pacgum_points,
                        coord,
                        "./assets/skin/other/sdot.png",
                        cell_width,
                        cell_height,
                    )
                }
            )

        blinky = Blinky("./assets/skin/ghosts/blinky.png", cell_width,
                        cell_height)
        blinky.set_parameters(self.maze, self.player)

        pinky = Pinky(
            "./assets/skin/ghosts/pinky.png",
            cell_width,
            cell_height,
        )
        pinky.set_parameters(self.player)

        inky = Inky(
            "./assets/skin/ghosts/inky.png",
            cell_width,
            cell_height,
        )
        inky.set_parameters(self.maze, self.player, blinky, pinky)

        clyde = Clyde(
            "./assets/skin/ghosts/clyde.png",
            cell_width,
            cell_height,
        )
        clyde.set_parameters(self.maze, self.player)

        self.ghosts: dict[str, Ghost] = {
            "blinky": blinky,
            "pinky": pinky,
            "inky": inky,
            "clyde": clyde,
        }

        self.cell_width = cell_width
        self.cell_height = cell_height


class Game:
    def __init__(self, window_size: int, padding: int, config:
                 Config, player: Player) -> None:
        self.config: Config = config
        self.levels: list[Level] = []
        for _ in self.config.levels:
            self.border_size = 5
            self.window_size = window_size
            self.padding = padding
            self.level_configs = self.config.levels
            self._loaded_levels: dict[int, Level] = {}
            self.player = player

    def get_level(self, index: int) -> Level:
        if index not in self._loaded_levels:
            config = self.level_configs[index]
            maze_width = config["width"]
            maze_height = config["height"]
            cell_width = (
                self.window_size[0]
                - (2 * self.padding)
                - ((maze_width + 1) * self.border_size)
            ) / maze_width
            cell_height = (
                self.window_size[1]
                - (2 * self.padding)
                - ((maze_height + 1) * self.border_size)
            ) / maze_height
            if index == 0:
                self._loaded_levels[index] = Level(
                    (maze_width, maze_height),
                    self.config.points_per_pacgum,
                    self.config.points_per_super_pacgum,
                    cell_width,
                    cell_height,
                    self.config.lives,
                    self.config.seed,
                    self.player,
                )
            else:
                self._loaded_levels[index] = Level(
                    (maze_width, maze_height),
                    self.config.points_per_pacgum,
                    self.config.points_per_super_pacgum,
                    cell_width,
                    cell_height,
                    self.config.lives,
                    random.random(),
                    self.player,
                )
        return self._loaded_levels[index]
