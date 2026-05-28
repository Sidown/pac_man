import sys
from GUI.gui_main_loop import Visualizer
from GUI.ui_elements.theme import Theme


def main() -> None:
    """
    Build the theme and launch the game
    """
    try:
        if len(sys.argv) > 2:
            raise ValueError("Too much args, this program only"
                             "need the config file path")
        if len(sys.argv) < 2:
            raise ValueError("Too little args: missing config file path")
    except ValueError as e:
        print(e)
        sys.exit()

    config_path = sys.argv[1]
    theme = Theme(
        background_color=(25, 25, 166),
        game_background_color=(0, 0, 0),
        title_color=(255, 255, 0),
        text_color=(255, 255, 255),
        wall_color=(25, 25, 166),
        wall_size=5,
        btn_background_color=(0, 0, 0),
        btn_text_color=(255, 255, 255),
        btn_on_mouse_over_text_color=(255, 255, 0),
        btn_on_mouse_over_background_color=(0, 0, 0),
        font_path="assets/fonts/Retro Gaming.ttf",
        header_size=42,
        text_size=28,
    )

    # Visualisation
    gui = Visualizer(theme, config_path)
    gui.run()


if __name__ == "__main__":
    main()
