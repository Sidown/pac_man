import pygame
from pygame import Surface


class Text:
    """
    A text label rendered with pygame
    """

    def __init__(
        self,
        surface: Surface,
        font_size: int,
        font_path: str,
        font_color: tuple[int, int, int],
        background_color: tuple[int, int, int],
        text: str,
        coordinate: tuple[int, int],
        center_x: bool,
    ) -> None:
        """
        Initialise the text label
        arguments:
        surface -> the pygame surface to draw on
        font_size -> size of the font
        font_path -> path to the font file
        font_color -> color of the font
        background_color -> background colour
        text -> the string
        coordinate -> x,y position of the text
        center_x -> if true the label is centred on x
        """
        self.surface: Surface = surface
        self.font_size: int = font_size
        self.font_path: str = font_path
        self.font_color: tuple[int, int, int] = font_color
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.background_color: tuple[int, int, int] = background_color
        self.text: str = text
        self.x, self.y = coordinate
        self.center_x: bool = center_x

    def draw(self, screen: Surface) -> None:
        """
        Draw the text on the screen
        arguments:
        screen -> the surface to render the text on
        """
        displayed_text = self.font.render(self.text, False, self.font_color)

        if self.center_x:
            center_x = self.x - (displayed_text.get_width() / 2)
            screen.blit(displayed_text, (center_x, self.y))
        else:
            screen.blit(displayed_text, (self.x, self.y))
