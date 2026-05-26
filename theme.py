from typing import Callable
import pygame
from pygame import Surface
from pygame.event import Event

from player import Player
from score import HighScore


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


class Clickable:
    """
    Class for clickable
    """
    def __init__(
        self,
        on_mouse_over_background_color: tuple[int, int, int],
        on_mouse_over_text_color: tuple[int, int, int],
        hovered: bool,
        callback: Callable[[], None],
    ) -> None:
        """
        Initialise the clickable class
        arguments:
        on_mouse_over_background_color -> background colour when hovered
        on_mouse_over_text_color -> text colour when hovered
        hovered -> hover state
        callback -> callable invoked on click
        """
        self.on_mouse_over_bg_color = on_mouse_over_background_color
        self.on_mouse_over_text_color = on_mouse_over_text_color
        self.hovered = hovered
        self.callback = callback


class Button(Text, Clickable):
    """
    A button combining text and click handling
    """
    def __init__(
        self,
        surface: Surface,
        font_size: int,
        font_path: str,
        font_color: tuple[int, int, int],
        background_color: tuple[int, int, int],
        text: str,
        callback: Callable[[], None],
        coordinate: tuple[int, int],
        center_x: bool,
        on_mouse_over_background_color: tuple[int, int, int],
        on_mouse_over_text_color: tuple[int, int, int],
    ):
        """
        Initialise the button
        arguments:
        surface -> pygame surface to draw on
        font_size -> size of the font
        font_path -> path to the font file
        font_color -> text colour
        background_color -> background colour
        text -> text of the button
        callback -> callable invoked when the button is clicked
        coordinate -> x,y position of the button
        center_x -> if true, the button is centred on x
        on_mouse_over_background_color -> background colour on hover
        on_mouse_over_text_color -> text colour on hover
        """
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
        )
        Clickable.__init__(
            self,
            on_mouse_over_background_color,
            on_mouse_over_text_color,
            False,
            callback,
        )
        # calculate the coordinate of the rect
        self.displayed_text = self.font.render(
            self.text, False, self.on_mouse_over_text_color
        )
        x1 = self.x
        y1 = self.y

        x2 = self.displayed_text.get_width()
        y2 = self.displayed_text.get_height()

        if self.center_x:
            center_x = x1 - (self.displayed_text.get_width() / 2)
            self.rect = pygame.Rect(center_x, y1, x2, y2)
        else:
            self.rect = pygame.Rect(x1, y1, x2, y2)

    def on_mouse_over(self) -> None:
        """Display an animation if the mouse is over the element"""
        # print the rect and the text on the surface.
        pygame.draw.rect(self.surface, self.on_mouse_over_bg_color, self.rect)
        if self.center_x:
            self.surface.blit(
                self.displayed_text,
                (self.x - (self.displayed_text.get_width() / 2), self.y),
            )
        else:
            self.surface.blit(self.displayed_text, (self.x, self.y))

    def draw(self, screen: Surface) -> None:
        """
        Draw the button on the screen
        Arguments:
        screen -> the surface to render the button on
        """
        color = (self.on_mouse_over_bg_color if self.hovered
                 else self.background_color)
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: Event) -> None:
        """
        Update the hover state and use the callback on mouse click
        arguments:
        event -> the pygame event
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()


class TextInput:
    """
    Text input.
    Click in the box to start typing.
    Only alphabetical characters and space are authorised.
    Max 10 characters.
    """

    def __init__(
        self,
        screen: Surface,
        coordinate: tuple[int, int],
        width: int,
        height: int,
        player: Player,
        highscore: HighScore,
    ) -> None:
        """
        Initialise the TextInput class
        arguments:
        screen -> the pygame surface to draw on
        coordinate -> x,y coordinate of the input box
        width -> width of the input box in pixels
        height -> height of the input box in pixels
        player -> the player
        highscore -> the highscore manager used to get the entry
        """
        self.screen: Surface = screen
        self.x: int = coordinate[0]
        self.y: int = coordinate[1]
        self.width: int = width
        self.height: int = height
        self.player: Player = player
        self.highscore: HighScore = highscore
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text: str = ""
        self.font = pygame.font.Font("assets/fonts/pressstart2p-regular.ttf",
                                     28)
        self.is_valid_name: bool = True

    def draw(self) -> None:
        """
        Draw the input label, box, text and error message
        """
        displayed_text = self.font.render("Enter your Name:", False, (0, 0, 0))
        self.screen.blit(displayed_text, (self.x, self.y - 35))
        pygame.draw.rect(self.screen, (145, 145, 145), self.rect)
        if self.text == "":
            return
        displayed_text = self.font.render(self.text, False, (0, 0, 0))
        self.screen.blit(displayed_text, (self.x, self.y + 10))
        if not self.is_valid_name:
            font = pygame.font.Font("assets/fonts/pressstart2p-regular.ttf",
                                    22)
            displayed_error = font.render(
                "Please enter a valid name (<10 char alpha and space only)",
                False,
                (255, 0, 0),
            )
            self.screen.blit(displayed_error, (self.x - 250, self.y + 65))

    def handle_event(self, event: Event) -> bool:
        """
        Process keyboard event
        arguments:
        event -> the pygame event to process
        return value:
        true if the player pressed enter and the name was saved
        false otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.highscore.save_high_score(self.text, self.player.score)
                self.text = ""
                return True
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 10:
                    self.is_valid_name = True
                    if event.unicode.isalpha() or event.unicode.isspace():
                        self.text += event.unicode
                        self.is_valid_name = True
                    else:
                        self.is_valid_name = False
                else:
                    self.is_valid_name = False
        return False
