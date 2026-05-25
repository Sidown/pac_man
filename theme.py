import pygame
from pygame import Surface

from player import Player
from score import HighScore


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

    def draw(self, screen: Surface) -> None:
        """Create a Text instance."""
        displayed_text = self.font.render(self.text, False, self.font_color)

        if self.center_x:
            center_x = self.x - (displayed_text.get_width() / 2)
            screen.blit(displayed_text, (center_x, self.y))
        else:
            screen.blit(displayed_text, (self.x, self.y))


class Clickable:
    def __init__(
        self,
        on_mouse_over_background_color: tuple[int, int, int],
        on_mouse_over_text_color: tuple[int, int, int],
        hovered: bool,
        callback,
    ) -> None:
        self.on_mouse_over_bg_color = on_mouse_over_background_color
        self.on_mouse_over_text_color = on_mouse_over_text_color
        self.hovered = hovered
        self.callback = callback


class Button(Text, Clickable):
    def __init__(
        self,
        surface: Surface,
        font_size: int,
        font_path: str,
        font_color: tuple[int, int, int],
        background_color: tuple[int, int, int],
        text: str,
        callback,
        coordinate: tuple[int, int],
        center_x: bool,
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
        """Display an animation during if the mouse is over the element"""
        # print the rect and the text on the surface.
        pygame.draw.rect(self.surface, self.on_mouse_over_bg_color, self.rect)
        if self.center_x:
            self.surface.blit(
                self.displayed_text,
                (self.x - (self.displayed_text.get_width() / 2), self.y),
            )
        else:
            self.surface.blit(self.displayed_text, (self.x, self.y))

    def draw(self, screen) -> None:
        color = self.on_mouse_over_bg_color if self.hovered else self.background_color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()


class TextInput:
    """Rect de couleur
    si l'utilisateur passe ca souris dessus et click, la couleur change.
    si il tape des lettres, elles apparaissent a l'ecran et sont dans une variable.
    lorsque le user click sur ENTER, on sauvegarde la valeur grave a une methode."""

    def __init__(
        self,
        screen: Surface,
        coordinate: tuple[int, int],
        width: int,
        height: int,
        player: Player,
        highscore: HighScore,
    ) -> None:
        self.screen: Surface = screen
        self.x: int = coordinate[0]
        self.y: int = coordinate[1]
        self.width: int = width
        self.height: int = height
        self.player: Player = player
        self.highscore: HighScore = highscore
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text: str = ""
        self.font = pygame.font.Font("assets/fonts/Retro Gaming.ttf", 28)

    def draw(self) -> None:
        displayed_text = self.font.render("Enter your Name:", False, (0, 0, 0))
        self.screen.blit(displayed_text, (self.x, self.y - 35))
        pygame.draw.rect(self.screen, (145, 145, 145), self.rect)
        if self.text == "":
            return
        displayed_text = self.font.render(self.text, False, (0, 0, 0))
        self.screen.blit(displayed_text, (self.x, self.y + 10))

    def handle_event(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # check que self.text est au bon format
                # sauvegarder ca dans le json.
                self.highscore.save_high_score(self.text, self.player.score)
                return
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 10:
                    self.text += event.unicode
            print(self.text)
