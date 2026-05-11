from mazegenerator.mazegenerator import MazeGenerator
from ghost import Blinky, Pinky, Inky, Clyde, Player

import parser
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
    player = Player(3, 2, 2) # a remplacer par le player definitif
    blinky = Blinky("./assets/skin/skin_zombie.png", 14, 14, mazegenerator, player)
    pinky = Pinky("./assets/skin/skin_zombie.png", 14, 14, mazegenerator, player)
    inky = Inky("./assets/skin/skin_zombie.png", 14, 14, mazegenerator, player, blinky, pinky)
    clyde = Clyde("./assets/skin/skin_zombie.png", 14, 14, mazegenerator, player)


    # Visualisation
    gui = Visualizer(mazegenerator, clyde)
    gui.run()


if __name__ == "__main__":
    main()
