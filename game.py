from ghost import Ghost, Blinky, Pinky, Inky, Clyde
from player import Player
from pacgum import Pacgum, SuperPacgum
from mazegenerator.mazegenerator import MazeGenerator
from parser import Config, parser
from not_corner import not_corner

class Game:
    def __init__(self, window_size, padding):
        self.config: Config = parser("./config.json")
        self.levels: list[Level] = []
        for level in self.config.levels:
            maze_width = level["width"]
            maze_height = level["height"]
            self.border_size = 5
            self.window_size = window_size
            self.padding = padding
            self.level_configs = self.config.levels
            self._loaded_levels: dict[int, Level] = {}

    def get_level(self, index: int):
        if index not in self._loaded_levels:
            config = self.level_configs[index]
            maze_width = config["width"]
            maze_height = config["height"]
            cell_width = (
                self.window_size[0] - (2 * self.padding) -
                ((maze_width + 1) * self.border_size)
                ) / maze_width
            cell_height = (
                self.window_size[1] - (2 * self.padding) -
                ((maze_height + 1) * self.border_size)
            ) / maze_height
            self._loaded_levels[index] = Level(
                (maze_width, maze_height),
                self.config.points_per_pacgum,
                self.config.points_per_super_pacgum,
                cell_width, cell_height,
                self.config.lives,
                self.config.seed
            )
        return self._loaded_levels[index]
   

class Level:
    def __init__(self, size: tuple[int], pacgum_points, super_pacgum_points, cell_width,
                 cell_height, player_lives, seed):
        self.maze: MazeGenerator = MazeGenerator(size, seed=seed)
        self.pacgums: dict[tuple[int], Pacgum] = {}
        for y, row in enumerate(self.maze.maze):
            for x, _ in enumerate(row):
                if self.maze.maze[y][x] != 15 and not_corner(self.maze, x, y):
                    self.pacgums.update(
                        {(x, y): Pacgum(pacgum_points, (x, y),
                                        "./assets/skin/other/dot.png",
                                        cell_width, cell_height)})
        
        super_pacgums_coord = [
            (0, 0),
            (0, len(self.maze.maze) - 1),
            (len(self.maze.maze[0]) - 1, 0),
            (len(self.maze.maze[0]) - 1, len(self.maze.maze) - 1)
        ]
        self.super_pacgums: dict[tuple[int], SuperPacgum] = {}
        for coord in super_pacgums_coord:
            self.super_pacgums.update(
                {coord: SuperPacgum(super_pacgum_points, coord,
                                    "./assets/skin/other/sdot.png",
                                    cell_width, cell_height)}
            )
        
        self.player: Player = Player(player_lives, len(self.maze.maze),
                                     len(self.maze.maze[0]),
                                     self.maze, self.pacgums,
                                     self.super_pacgums,
                                     cell_height, cell_width)
        
        blinky = Blinky(
                "./assets/skin/ghosts/blinky.png",
                0, 0,
                self.maze,
                self.player,
                cell_width,
                cell_height)
        pinky = Pinky(
                "./assets/skin/ghosts/pinky.png",
                0,
                len(self.maze.maze) - 1,
                self.maze,
                self.player,
                cell_width,
                cell_height)
        inky = Inky(
                "./assets/skin/ghosts/inky.png",
                len(self.maze.maze[0]) - 1,
                0,
                self.maze,
                self.player,
                cell_width,
                cell_height,
                blinky,
                pinky)
        clyde = Clyde(
                "./assets/skin/ghosts/clyde.png",
                len(self.maze.maze[0]) - 1,
                len(self.maze.maze) - 1,
                self.maze,
                self.player,
                cell_width,
                cell_height)
        
        self.ghosts: dict[str, Ghost] = {
            "blinky": blinky,
            "pinky": pinky,
            "inky": inky,
            "clyde": clyde
            }
        self.cell_width = cell_width
        self.cell_height = cell_height

