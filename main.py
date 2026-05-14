import pygame
from mazegenerator.mazegenerator import MazeGenerator

import parser
from ghost import Blinky, Clyde, Inky, Pinky, Player
from visualizer import Visualizer
from pacgum import Pacgum, SuperPacgum
from not_corner import not_corner


def main():
    # print("Hello from pac-man!")

    # Parsing
    config = parser.parser("./config.json")
    # print(config)

    # Maze genereation
    mazegenerator = MazeGenerator(
        size=(15, 15),
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=42,
    )
    mazegenerator.generate()
    pacgums = {}
    for (y, row) in enumerate(mazegenerator.maze):
        for (x, _) in enumerate(row):
            print(x, y)
            if mazegenerator.maze[y][x] != 15 and not_corner(mazegenerator, x, y):
                pacgums.update({(x, y): Pacgum(20, (x, y), "./assets/skin/other/dot.png")})
    super_pacgums_coord = [(0, 0), (0, len(mazegenerator.maze) - 1),
                           (len(mazegenerator.maze[0]) - 1, 0),
                           (len(mazegenerator.maze[0]) - 1,
                            len(mazegenerator.maze) - 1)]
    super_pacgums = {}
    for coord in super_pacgums_coord:
        super_pacgums.update({coord: SuperPacgum(100, coord, "./assets/skin/other/dot.png")})
    player = Player(
        3,
        14,
        14,
        mazegenerator,
        pacgums,
        super_pacgums
    )

    blinky = Blinky("./assets/skin/ghosts/blinky.png", 0, 0, mazegenerator, player)
    pinky = Pinky("./assets/skin/ghosts/pinky.png", 0, 14, mazegenerator, player)
    inky = Inky(
        "./assets/skin/ghosts/inky.png", 14, 0, mazegenerator, player, blinky, pinky
    )
    clyde = Clyde("./assets/skin/ghosts/clyde.png", 14, 14, mazegenerator, player)

    # Visualisation
    gui = Visualizer(mazegenerator, blinky, pinky, inky, clyde, player, pacgums, super_pacgums)
    gui.run()


if __name__ == "__main__":
    main()
