import pygame
from mazegenerator.mazegenerator import MazeGenerator

import parser
from ghost import Blinky, Clyde, Inky, Pinky, Player
from visualizer import Visualizer


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
    player = Player(
        3,
        14,
        14,
    )
    blinky = Blinky("./assets/skin/skin_zombie.png", 0, 0, mazegenerator, player)
    pinky = Pinky("./assets/skin/skin_zombie.png", 0, 14, mazegenerator, player)
    inky = Inky(
        "./assets/skin/skin_zombie.png", 14, 0, mazegenerator, player, blinky, pinky
    )
    clyde = Clyde("./assets/skin/skin_zombie.png", 14, 14, mazegenerator, player)

    # Visualisation
    gui = Visualizer(mazegenerator, blinky, pinky, inky, clyde, player)
    gui.run()


if __name__ == "__main__":
    main()
