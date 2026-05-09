import pygame
from mazegenerator.mazegenerator import MazeGenerator
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
        """Create a box containing a text."""
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


class Visualizer:
    """"""

    def __init__(self, maze: MazeGenerator) -> None:
        self.WIDTH = 540
        self.HEIGHT = 960
        self.PADDING = 50
        self.screen: Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.bg = pygame.image.load("assets/background/zombie.jpg")
        self.maze: MazeGenerator = maze

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

        # Managed mouse click
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if btn_game.rect.collidepoint(x, y):
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    self._show_game()
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

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.blit(self.bg, (0, 0))
            self._show_main_menu()
            pygame.display.flip()
        pygame.quit()

    def _print_maze(self) -> None:
        """Print the maze."""

        maze_width = len(self.maze.maze)
        maze_height = len(self.maze.maze[0])
        border_size = 5

        cell_width = (
            self.WIDTH - (2 * self.PADDING) - ((maze_width + 1) * border_size)
        ) / maze_width
        cell_height = (
            self.HEIGHT - (2 * self.PADDING) - ((maze_height + 1) * border_size)
        ) / maze_height

        print(f"self.WIDTH: {self.WIDTH} | cell_width: {cell_width}")
        self.screen.fill((149, 204, 144))

        curr_x = self.PADDING
        curr_y = self.PADDING

        for row_nb in range(maze_height):
            print_down = False
            if row_nb == (maze_height - 1):
                print_down = True
            for col_nb in range(maze_width):
                opp_code = self.maze.maze[row_nb][col_nb]
                print_right = False
                if col_nb == (maze_width - 1):
                    print_right = True

                self._print_cell(
                    curr_x,
                    curr_y,
                    cell_width,
                    cell_height,
                    opp_code,
                    border_size,
                    (126, 29, 29),
                    print_right,
                    print_down,
                )
                curr_x += cell_width + (border_size)
            curr_x = self.PADDING
            curr_y += cell_height + (border_size)

    def _print_cell(
        self,
        x: int | float,
        y: int | float,
        cell_width: int | float,
        cell_height: int | float,
        opp_code: int,
        border_size: int,
        wall_color: tuple[int, int, int],
        print_east: bool,
        print_down: bool,
    ) -> None:
        # upper border
        if opp_code & 0b0001:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x - border_size, y - border_size),
                (x + cell_width + border_size, y - border_size),
                border_size,
            )
        # east border
        if (opp_code & 0b0010) and print_east:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x + cell_width + border_size, y - border_size),
                (x + cell_width + border_size, y + cell_height + border_size),
                border_size,
            )
        # south border
        if (opp_code & 0b0100) and print_down:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x - border_size, y + cell_height + border_size),
                (x + cell_width + border_size, y + cell_height + border_size),
                border_size,
            )
        # west border
        if opp_code & 0b1000:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x - border_size, y - border_size),
                (x - border_size, y + cell_height + border_size),
                border_size,
            )

    def _show_game(self) -> None:
        """The Game screen"""
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
            self.screen.blit(self.bg, (0, 0))
            self._print_maze()
            pygame.display.flip()
        pygame.quit()

    def _show_game_over(self) -> None:
        """The Gane Over screen"""
        pass
