from mazegenerator.mazegenerator import MazeGenerator

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

    # Visualisation
    gui = Visualizer(mazegenerator)
    gui.run()


if __name__ == "__main__":
    main()
