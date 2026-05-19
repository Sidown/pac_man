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
            border_size = 5

            cell_width = (
                window_size[0] - (2 * padding) - ((maze_width + 1) *
                                                  border_size)
            ) / maze_width

            cell_height = self.cell_height = (
                window_size[1]
                - (2 * padding)
                - ((maze_height + 1) * border_size)
            ) / maze_height

            self.levels.append(Level((maze_width, maze_height),
                                     self.config.points_per_pacgum,
                                     cell_width, cell_height,
                                     self.config.lives))
        

class Level:
    def __init__(self, size: tuple[int], pacgum_points, cell_width,
                 cell_height, player_lives):
        self.maze: MazeGenerator = MazeGenerator(size)
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
            (len(self.maze.maze[0] - 1, 0)),
            (len(self.maze.maze[0]) - 1, len(self.maze.maze) - 1)
        ]
        self.super_pacgums: dict[tuple[int], SuperPacgum] = {}
        for coord in super_pacgums_coord:
            self.super_pacgums.update(
                {coord: SuperPacgum(100, coord, "./assets/skin/other/sdot.png",
                                    cell_width, cell_height)}
            )
        
        self.player: Player = Player(player_lives, len(self.maze.maze),
                                     len(self.maze.maze[0]),
                                     self.maze, self.pacgums,
                                     self.super_pacgums,
                                     cell_height, cell_width)
        
        self.ghosts: dict[str, Ghost] = {
            "blinky": Blinky(
                "./assets/skin/ghosts/blinky.png",
                0, 0,
                self.maze,
                self.player,
                cell_width,
                cell_height),
            "pinky": Pinky(
                "./assets/skin/ghosts/pinky.png",
                0,
                len(self.maze.maze) - 1,
                self.maze,
                self.player,
                cell_width,
                cell_height),
            "inky": Inky(
                "./assets/skin/ghosts/inky.png",
                len(self.maze.maze[0]) - 1,
                0,
                self.maze,
                self.player,
                cell_width,
                cell_height,
                self.ghosts["blinky"],
                self.ghosts["pinky"]),
            "clyde": Clyde(
                "./assets/skin/ghosts/clyde.png",
                len(self.maze.maze[0]) - 1,
                len(self.maze.maze) - 1,
                self.maze,
                self.player,
                cell_width,
                cell_height)
        }

