import parser
from visualizer import Visualizer

def main():
    print("Hello from pac-man!")
    
    # Parsing
    config = parser.parser("./config.json")
    print(config)

    # Visualisation
    gui = Visualizer()
    gui.run()


if __name__ == "__main__":
    main()
