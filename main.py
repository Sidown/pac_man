import parser
from visualizer import Visualizer
from mazegenerator.mazegenerator import MazeGenerator



def main():
    print("Hello from pac-man!")
    
    # Parsing
    config = parser.parser("./config.json")
    print(config)

    # Visualisation
    gui = Visualizer()
    gui.run()
    mazegenerator = MazeGenerator(
        size = (15, 15),
        entry_cell = (0, 0),
        exit_cell = (-1, -1),
        seed = 42,
    )
    mazegenerator.generate()


if __name__ == "__main__":
    main()
