class Theme:
    """
    Class for all the visual styling parameters used for the scenes.
    """

    def __init__(
        self,
        background_color: tuple[int, int, int] = (25, 25, 166),
        game_background_color: tuple[int, int, int] = (0, 0, 0),
        title_color: tuple[int, int, int] = (255, 255, 0),
        text_color: tuple[int, int, int] = (255, 255, 255),
        wall_color: tuple[int, int, int] = (25, 25, 166),
        wall_size: int = 3,
        btn_background_color: tuple[int, int, int] = (0, 0, 0),
        btn_text_color: tuple[int, int, int] = (255, 255, 255),
        btn_on_mouse_over_text_color: tuple[int, int, int] = (255, 255, 0),
        btn_on_mouse_over_background_color: tuple[int, int, int] = (0, 0, 0),
        font_path: str = "assets/fonts/Retro Gaming.ttf",
        header_size: int = 42,
        text_size: int = 28,
    ) -> None:
        """
        Initialise the Theme class with colour and font settings
        Arguments:
        background_color -> colour used for background
        game_background_color -> color used for the background in game
        title_color -> colour used for title
        text_color -> colour used for basic text
        wall_color -> colour used for maze walls
        wall_size -> thickness used for maze walls in pixels
        btn_background_color -> background button colour
        btn_text_color -> text button colour
        btn_on_mouse_over_text_color -> button colour on hover
        btn_on_mouse_over_background_color -> background button
            colour on hover
        font_path -> path to the font file
        header_size -> font size for header
        text_size -> font size for text
        """
        self.background_color: tuple[int, int, int] = background_color
        self.game_background_color: tuple[int, int, int] = (
            game_background_color)
        self.title_color: tuple[int, int, int] = title_color
        self.text_color: tuple[int, int, int] = text_color
        self.wall_color: tuple[int, int, int] = wall_color
        self.wall_size: int = wall_size
        self.btn_background_color: tuple[int, int, int] = btn_background_color
        self.btn_text_color: tuple[int, int, int] = btn_text_color
        self.btn_on_mouse_over_text_color: tuple[int, int, int] = (
            btn_on_mouse_over_text_color
        )
        self.btn_on_mouse_over_background_color: tuple[int, int, int] = (
            btn_on_mouse_over_background_color
        )
        self.font_path: str = font_path
        self.header_size: int = header_size
        self.text_size: int = text_size
