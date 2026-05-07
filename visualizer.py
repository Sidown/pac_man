import pygame
from pygame import Rect, Surface

# idee creatives:
# - Mode Zombie -18 => fond: shlop rg.otf
# - Mode Sex -18
# - drogue
# - alcolique
# - sucre
# - mode 42.


class Boxed_text:
    def __init__(
        self,
        screen: Surface,
        text: str,
        coordinate: tuple[int, int],
        font_path: str,
        font_size: int,
        font_color: tuple[int, int, int],
    ) -> None:
        self.screen: Surface = screen
        self.text: str = text
        self.x, self.y = coordinate
        self.font_path: str = font_path
        self.font_size: int = font_size
        self.font_color: tuple[int, int, int] = font_color
        self.rect: Rect

    def create_boxed_text(self, center_x: bool) -> None:
        """"""
        font = pygame.font.Font(self.font_path, self.font_size)
        text = font.render(self.text, False, self.font_color)

        # calculate the coordinate of the rect
        x1 = self.x
        y1 = self.y
        x2 = text.get_width()
        y2 = text.get_height()

        if center_x:
            width = self.screen.get_width()
            text_width = text.get_width()
            x1 = (width // 2) - (text_width // 2)
            x2 = text_width

        self.rect = pygame.Rect(x1, y1, x2, y2)

        # print the rect and the text on the surface.
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        self.screen.blit(text, (x1, y1))


class Button(Boxed_text):
    def __init__(
        self,
        screen: Surface,
        text: str,
        coordinate: tuple[int, int],
        font_path: str,
        font_size: int,
        font_color: tuple[int, int, int],
        center_x: bool,
    ) -> None:
        super().__init__(screen, text, coordinate, font_path, font_size, font_color)

    def is_clicked(self) -> bool:
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if button.collidepoint(x, y):
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    return True

        return False


class Visualizer:
    """"""

    def __init__(self) -> None:
        self.WIDTH = 540
        self.HEIGHT = 960
        self.screen: Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.init()

    def _show_main_menu(self) -> None:
        """Show the home page of the Pac-Man game."""

        header = Boxed_text(
            self.screen,
            "Pac-Man, Will you survive...",
            ((self.WIDTH // 2), 30),
            "assets/fonts/shlop rg.otf",
            56,
            (126, 29, 29),
        )

        btn_game = Boxed_text(
            self.screen,
            "New Game",
            ((self.WIDTH // 2), 250),
            "assets/fonts/shlop rg.otf",
            42,
            (126, 29, 29),
        )

        btn_high_score = Boxed_text(
            self.screen,
            "View High Score",
            ((self.WIDTH // 2), 350),
            "assets/fonts/shlop rg.otf",
            42,
            (126, 29, 29),
        )

        btn_theme = Boxed_text(
            self.screen,
            "Change Theme",
            ((self.WIDTH // 2), 450),
            "assets/fonts/shlop rg.otf",
            42,
            (126, 29, 29),
        )

        header.create_boxed_text(True)
        btn_game.create_boxed_text(True)
        btn_high_score.create_boxed_text(True)
        btn_theme.create_boxed_text(True)

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if btn_game.rect.collidepoint(x, y):
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("New Game !")
            if btn_high_score.rect.collidepoint(x, y):
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("let's view the highest score!")
            if btn_theme.rect.collidepoint(x, y):
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("Ok we will set up a new theme !")

    def run(self) -> None:
        """The full game visualisation"""
        pygame.display.set_caption("Pac-Man")
        running = True
        bg = pygame.image.load("assets/background/zombie.jpg")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.blit(bg, (0, 0))
            self._show_main_menu()
            pygame.display.flip()
        pygame.quit()

    def _show_game(self) -> None:
        pass

    def _show_game_over(self) -> None:
        pass
