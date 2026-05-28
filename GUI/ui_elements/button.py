from typing import Callable

import pygame
from pygame import Surface
from pygame.event import Event

from .text import Text


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
            center_x_pos = x1 - (self.displayed_text.get_width() / 2)
            self.rect = pygame.Rect(center_x_pos, y1, x2, y2)
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
