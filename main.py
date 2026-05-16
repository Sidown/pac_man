import pygame
from mazegenerator.mazegenerator import MazeGenerator

import parser
from ghost import Blinky, Clyde, Inky, Pinky, Player
from gui_main_loop import Visualizer
from not_corner import not_corner
from pacgum import Pacgum, SuperPacgum
from theme import Theme


def main():

    # Parsing
    config = parser.parser("./config.json")

    # Maze genereation
    mazegenerator = MazeGenerator(
        size=(15, 15),
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=42,
    )
    mazegenerator.generate()
    pacgums = {}
    for y, row in enumerate(mazegenerator.maze):
        for x, _ in enumerate(row):
            if mazegenerator.maze[y][x] != 15 and not_corner(mazegenerator, x, y):
                pacgums.update(
                    {(x, y): Pacgum(20, (x, y), "./assets/skin/other/dot.png")}
                )
    super_pacgums_coord = [
        (0, 0),
        (0, len(mazegenerator.maze) - 1),
        (len(mazegenerator.maze[0]) - 1, 0),
        (len(mazegenerator.maze[0]) - 1, len(mazegenerator.maze) - 1),
    ]
    super_pacgums = {}
    for coord in super_pacgums_coord:
        super_pacgums.update(
            {coord: SuperPacgum(100, coord, "./assets/skin/other/sdot.png")}
        )
    player = Player(
        "assets/skin/pacman.png", 3, 14, 14, mazegenerator, pacgums, super_pacgums
    )

    blinky = Blinky("./assets/skin/ghosts/blinky.png", 0, 0, mazegenerator, player)
    pinky = Pinky(
        "./assets/skin/ghosts/pinky.png",
        0,
        len(mazegenerator.maze) - 1,
        mazegenerator,
        player,
    )
    inky = Inky(
        "./assets/skin/ghosts/inky.png",
        len(mazegenerator.maze[0]) - 1,
        0,
        mazegenerator,
        player,
        blinky,
        pinky,
    )
    clyde = Clyde(
        "./assets/skin/ghosts/clyde.png",
        len(mazegenerator.maze[0]) - 1,
        len(mazegenerator.maze) - 1,
        mazegenerator,
        player,
    )

    theme = Theme(
        background_color=(25, 25, 166),
        game_background_color=(0, 0, 0),
        title_color=(255, 255, 0),
        text_color=(255, 255, 255),
        wall_color=(25, 25, 166),
        wall_size=3,
        btn_background_color=(0, 0, 0),
        btn_text_color=(255, 255, 255),
        btn_on_mouse_over_text_color=(255, 255, 0),
        btn_on_mouse_over_background_color=(0, 0, 0),
        font_path="assets/fonts/Retro Gaming.ttf",
        header_size=42,
        text_size=28,
    )

    # Visualisation
    gui = Visualizer(
        mazegenerator, theme, blinky, pinky, inky, clyde, player, pacgums, super_pacgums
    )
    gui.run()


if __name__ == "__main__":
    main()
