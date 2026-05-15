import pygame
from pygame import Surface


class Theme:
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
        self.background_color: tuple[int, int, int] = background_color
        self.game_background_color: tuple[int, int, int] = game_background_color
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


class Text:
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
        center_y: bool,
    ) -> None:
        self.surface: Surface = surface
        self.font_size: int = font_size
        self.font_path: str = font_path
        self.font_color: tuple[int, int, int] = font_color
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.background_color: tuple[int, int, int] = background_color
        self.text: str = text
        self.x, self.y = coordinate
        self.center_x: bool = center_x
        self.center_y: bool = center_y

    def create(self) -> None:
        """Create a Text instance."""
        displayed_text = self.font.render(self.text, False, self.font_color)

        if self.center_x:
            self.x = self.x - (displayed_text.get_width() / 2)
        if self.center_y:
            self.y = self.y - (displayed_text.get_height() / 2)

        self.surface.blit(displayed_text, (self.x, self.y))


class Clickable:
    def __init__(
        self,
        on_mouse_over_background_color: tuple[int, int, int],
        on_mouse_over_text_color: tuple[int, int, int],
    ) -> None:
        self.on_mouse_over_bg_color = on_mouse_over_background_color
        self.on_mouse_over_text_color = on_mouse_over_text_color


class Button(Text, Clickable):
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
        center_y: bool,
        on_mouse_over_background_color: tuple[int, int, int],
        on_mouse_over_text_color: tuple[int, int, int],
    ):
        Text.__init__(
            self,
            surface,
            font_size,
            font_path,
            font_color,
            background_color,
            text,
            coordinate,
            center_x,
            center_y,
        )
        Clickable.__init__(
            self, on_mouse_over_background_color, on_mouse_over_text_color
        )
        # calculate the coordinate of the rect
        self.displayed_text = self.font.render(
            self.text, False, self.on_mouse_over_text_color
        )
        x1 = self.x
        y1 = self.y

        if self.center_x:
            x1 = x1 - (self.displayed_text.get_width() / 2)
        if self.center_y:
            y1 = y1 - (self.displayed_text.get_height() / 2)

        x2 = self.displayed_text.get_width()
        y2 = self.displayed_text.get_height()

        self.rect = pygame.Rect(x1, y1, x2, y2)

    def on_mouse_over(self) -> None:
        """Display an animation during if the mouse is over the element"""

        # print the rect and the text on the surface.
        pygame.draw.rect(self.surface, self.on_mouse_over_bg_color, self.rect)
        self.surface.blit(self.displayed_text, (self.x, self.y))
