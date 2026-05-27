import pygame
from pygame import Surface
from pygame.event import Event

from game_class.player import Player
from GUI.score import HighScore


class HighScoreInput:
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
        Initialise the HighScoreInput class
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
        self.font = pygame.font.Font("assets/fonts/Retro Gaming.ttf", 28)
        self.is_valid_name: bool = True
        self.is_clicked: bool = False
        self.hovered: bool = False

    def draw(self) -> None:
        """
        Draw the input label, box, text and error message
        """
        displayed_text = self.font.render("Enter your Name:", False, (255, 255, 255))
        self.screen.blit(
            displayed_text, (self.x - displayed_text.get_width() - 10, self.y + 10)
        )
        color = (255, 255, 255) if self.is_clicked or self.hovered else (200, 200, 200)
        pygame.draw.rect(self.screen, color, self.rect)
        if not self.is_valid_name:
            font = pygame.font.Font("assets/fonts/Retro Gaming.ttf", 22)
            displayed_error = font.render(
                "Please enter a valid name (<10 char alpha and space only)",
                False,
                (255, 0, 0),
            )
            self.screen.blit(
                displayed_error,
                (self.x - (displayed_error.get_width() // 2), (self.y + 100)),
            )
        if self.text == "":
            return
        name_text = self.font.render(self.text, False, (0, 0, 0))
        self.screen.blit(name_text, (self.x, self.y + 10))

    def _reset_text(self) -> None:
        self.text = ""
        self.hovered = False
        self.is_clicked = False
        self.is_valid_name = True

    def handle_event(self, event: Event) -> bool:
        """
        Process keyboard event
        arguments:
        event -> the pygame event to process
        return value:
        true if the player pressed enter and the name was saved
        false otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            # si l'utilisateur a clique sur la zone de texte.
            self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.hovered:
            # si le user click en dehors de la zone de texte.
            self.is_clicked = False
        if self.is_clicked and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.highscore.save_high_score(self.text)
                self._reset_text()
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
