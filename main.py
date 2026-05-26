from gui_main_loop import Visualizer
from theme import Theme


def main():

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
    gui = Visualizer(theme)
    gui.run()


if __name__ == "__main__":
    main()
