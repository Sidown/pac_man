import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Rect, Surface, time
from pacgum import Pacgum, SuperPacgum

from ghost import Blinky, Clyde, Ghost, Inky, Pinky, Player

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
        self.center_x: bool = False

    def create_boxed_text(self, center_x: bool) -> None:
        """Create a box containing a text."""
        self.center_x = center_x
        font = pygame.font.Font(self.font_path, self.font_size)
        text = font.render(self.text, False, self.font_color)

        # calculate the coordinate of the rect
        x1 = self.x
        y1 = self.y
        x2 = text.get_width()
        y2 = text.get_height()

        if self.center_x:
            width = self.screen.get_width()
            text_width = text.get_width()
            x1 = (width // 2) - (text_width // 2)
            x2 = text_width

        self.rect = pygame.Rect(x1, y1, x2, y2)

        # print the rect and the text on the surface.
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        self.screen.blit(text, (x1, y1))

    def set_color(self, color: tuple[int, int, int]) -> None:
        """Change the button color."""
        font = pygame.font.Font(self.font_path, self.font_size)
        text = font.render(self.text, False, color)

        # calculate the coordinate of the rect
        x1 = self.x
        y1 = self.y
        x2 = text.get_width()
        y2 = text.get_height()

        if self.center_x:
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

    def __init__(
        self,
        maze: MazeGenerator,
        blinky: Blinky,
        pinky: Pinky,
        inky: Inky,
        clyde: Clyde,
        player: Player,
        pacgums: dict[tuple[int], Pacgum],
        super_pacgums: dict[tuple[int], SuperPacgum]
    ) -> None:
        self.WIDTH = 960
        self.HEIGHT = 720
        self.PADDING = 150
        self.maze: MazeGenerator = maze
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.maze_height = len(self.maze.maze)
        self.maze_width = len(self.maze.maze[0])
        self.border_size = 5
        self.cell_width = (
            self.WIDTH - (2 * self.PADDING) - ((self.maze_width + 1) * self.border_size)
        ) / self.maze_width
        self.cell_height = (
            self.HEIGHT
            - (2 * self.PADDING)
            - ((self.maze_height + 1) * self.border_size)
        ) / self.maze_height

        self.bg = pygame.image.load("assets/background/main_background.jpg")
        self.player: Player = player
        self.player.skin = pygame.transform.scale(
            pygame.image.load("assets/skin/skin_survivor.png"),
            (self.cell_width, self.cell_height),
        )
        self.vulnerable_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/ghosts/blue_ghost.png"),
            (self.cell_width, self.cell_height)
        )
        self.blinky: Blinky = blinky
        self.blinky_skin = pygame.transform.scale(
                    pygame.image.load(self.blinky.actual_skin),
                    (self.cell_width, self.cell_height))
        self.pinky: Pinky = pinky
        self.pinky_skin = pygame.transform.scale(
                    pygame.image.load(self.pinky.actual_skin),
                    (self.cell_width, self.cell_height))
        self.inky: Inky = inky
        self.inky_skin = pygame.transform.scale(
                    pygame.image.load(self.inky.actual_skin),
                    (self.cell_width, self.cell_height))
        self.clyde: Clyde = clyde
        self.clyde_skin = pygame.transform.scale(
                    pygame.image.load(self.clyde.actual_skin),
                    (self.cell_width, self.cell_height))
        self.pacgums: dict[tuple[int], Pacgum] = pacgums
        self.pacgums_skin = pygame.transform.scale(
                    pygame.image.load("./assets/skin/other/dot.png"),
                    (self.cell_width, self.cell_height))
        self.super_pacgums: dict[tuple[int], SuperPacgum] = super_pacgums
        self.super_pacgums_skin = pygame.transform.scale(
                    pygame.image.load("./assets/skin/other/sdot.png"),
                    (self.cell_width, self.cell_height))
        self._btn_game_rect = pygame.Rect(0, 0, 0, 0)
        self.hud_font = pygame.font.Font("assets/fonts/shlop rg.otf", 22)
        self._btn_back_rect = pygame.Rect(0, 0, 0, 0)

    def manage_mouse_click(self, btn_game, btn_high_score, btn_theme):
        """Managed mouse click"""
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if btn_game.rect.collidepoint(x, y):
                btn_game.set_color((200, 200, 200))
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    self._show_game()
            if btn_high_score.rect.collidepoint(x, y):
                btn_high_score.set_color((200, 200, 200))
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("let's view the highest score!")
            if btn_theme.rect.collidepoint(x, y):
                btn_theme.set_color((200, 200, 200))
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("Ok we will set up a new theme !")

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

        self._btn_game_rect = btn_game.rect
        self._btn_high_score_rect = btn_high_score.rect
        self._btn_theme_rect = btn_theme.rect

        self.manage_mouse_click(btn_game, btn_high_score, btn_theme)

    def run(self) -> None:
        """The full game visualisation"""
        pygame.display.set_caption("Pac-Man")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if hasattr(self, '_btn_game_rect') and self._btn_game_rect.collidepoint(x, y):
                        self._show_game()
                        return
            self.screen.blit(self.bg, (0, 0))
            self._show_main_menu()
            pygame.display.flip()
        pygame.quit()

    def _show_maze(self, curr_x, curr_y):
        """Show the maze"""
        for row_nb in range(self.maze_height):
            print_down = False
            if row_nb == (self.maze_height - 1):
                print_down = True
            for col_nb in range(self.maze_width):
                opp_code = self.maze.maze[row_nb][col_nb]
                print_right = False
                if col_nb == (self.maze_width - 1):
                    print_right = True

                self._print_cell(
                    curr_x,
                    curr_y,
                    self.cell_width,
                    self.cell_height,
                    opp_code,
                    self.border_size,
                    (126, 29, 29),
                    print_right,
                    print_down,
                )
                curr_x += self.cell_width + (self.border_size)
            curr_x = self.PADDING
            curr_y += self.cell_height + (self.border_size)

    def _print_maze(self) -> None:
        """Print the maze."""
        self.screen.fill((149, 204, 144))
        # bouton pour revenir au main menu.
        btn_back_to_main_menu = Boxed_text(
            self.screen,
            "Back to main menu",
            (10, 10),
            "assets/fonts/shlop rg.otf",
            24,
            (126, 29, 29),
        )
        btn_back_to_main_menu.create_boxed_text(False)
        self._btn_back_rect = btn_back_to_main_menu.rect

        curr_x = self.PADDING
        curr_y = self.PADDING

        # afficher le maze
        self._show_maze(curr_x, curr_y)

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
                (x, y),
                (x + cell_width + border_size, y),
                border_size,
            )
        # east border
        if (opp_code & 0b0010) and print_east:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x + border_size + cell_width, y),
                (x + cell_width + border_size, y + cell_height + border_size),
                border_size,
            )
        # south border
        if (opp_code & 0b0100) and print_down:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x, y + cell_height + border_size),
                (x + cell_width + border_size, y + cell_height + border_size),
                border_size,
            )
        # west border
        if opp_code & 0b1000:
            pygame.draw.line(
                self.screen,
                wall_color,
                (x, y),
                (x, y + cell_height + border_size),
                border_size,
            )
        # si tout les murs sont ferme, c'est le 42 pattern, le mettre en couleur
        if opp_code == 15:
            pygame.draw.rect(
                self.screen,
                wall_color,
                (
                    x,
                    y,
                    self.cell_width + self.border_size,
                    self.cell_height + self.border_size,
                ),
            )

    def _print_skin(self, skin: Surface, x_cell, y_cell) -> None:
        """A function that print a Skin on the maze."""
        self.screen.blit(
            skin,
            (
                self.PADDING + x_cell * (self.border_size + self.cell_width),
                self.PADDING + y_cell * (self.border_size + self.cell_height),
            ),
        )

    def _print_HUD(self) -> None:
        """Print a HUD in the top right corner, that display the number of life and the player score and the highest score."""

        x1 = self.screen.get_width() - 300
        x2 = self.screen.get_width()
        y1 = 0
        y2 = 100

        # affichage le HUD
        self.rect = pygame.Rect(x1, y1, x2, y2)
        pygame.draw.rect(self.screen, (170, 75, 75), self.rect)
        pygame.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (x1, y2), (x2, y2), 3)

        # affichage du text dans le HUD
        life_nb = self.hud_font.render("Life number: ", False, (0, 0, 0))
        timer = self.hud_font.render("Time: ", False, (0, 0, 0))
        current_score = self.hud_font.render("Current score: ", False, (0, 0, 0))
        highest_score = self.hud_font.render("Highest score: ", False, (0, 0, 0))
        self.screen.blit(life_nb, (x1 + 5, y1))
        self.screen.blit(timer, (x1 + 5, y1 + 25))
        self.screen.blit(current_score, (x1 + 5, y1 + 50))
        self.screen.blit(highest_score, (x1 + 5, y1 + 75))

        # affichage des valeurs NB LIFE, TIME, HIGHSCORE ...
        player_lives = self.hud_font.render(f"{self.player.lives}", False, (0, 0, 0))
        self.screen.blit(player_lives, (x1 + life_nb.get_width() + 5, y1))

    def _reset_all_param(self) -> None:
        """Reset param for all ghosts and the player"""
        self.player.reset_param()
        self.blinky.reset_param()
        self.inky.reset_param()
        self.pinky.reset_param()
        self.clyde.reset_param()

    def _show_game(self) -> None:
        """The Game simulation"""
        game_running = True
        clock = time.Clock()
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.queud_direction = "N"
                    if event.key == pygame.K_DOWN:
                        self.player.queud_direction = "S"
                    if event.key == pygame.K_RIGHT:
                        self.player.queud_direction = "E"
                    if event.key == pygame.K_LEFT:
                        self.player.queud_direction = "W"
                    if event.key == pygame.K_SPACE:
                        is_paused = True
                        while is_paused:
                            pygame.time.wait(1000)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        is_paused = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if self._btn_back_rect.collidepoint(x, y):
                        game_running = False
                        self.run()
                        return
                    
            self.screen.blit(self.bg, (0, 0))
            self.blinky.play()
            self.inky.play()
            self.pinky.play()
            self.clyde.play()
            self._print_maze()
            self._print_HUD()

            # deplacer le personnage
            self.player.update_player()
            self._print_skin(self.player.skin, self.player.pixel_x, self.player.pixel_y)
            # moins bon en perf de recharger l'image a chaque fois
            blinky_surface = (self.vulnerable_skin if self.blinky.is_vulnerable
                              else self.blinky_skin)
            self._print_skin(
                blinky_surface,
                self.blinky.pixel_x,
                self.blinky.pixel_y,
            )
            pinky_surface = (self.vulnerable_skin if self.pinky.is_vulnerable
                              else self.pinky_skin)
            self._print_skin(
                pinky_surface,
                self.pinky.pixel_x,
                self.pinky.pixel_y,
            )
            inky_surface = (self.vulnerable_skin if self.inky.is_vulnerable
                              else self.inky_skin)
            self._print_skin(
                inky_surface,
                self.inky.pixel_x,
                self.inky.pixel_y,
            )
            clyde_surface = (self.vulnerable_skin if self.clyde.is_vulnerable
                              else self.clyde_skin)
            self._print_skin(
                clyde_surface,
                self.clyde.pixel_x,
                self.clyde.pixel_y,
            )
            for pacgum in self.pacgums.values():
                if pacgum.visible:
                    self._print_skin(
                        self.pacgums_skin,
                        pacgum.pixel_x, pacgum.pixel_y
                    )
            for super_pacgum in self.super_pacgums.values():
                if super_pacgum.visible:
                    self._print_skin(self.super_pacgums_skin,
                        super_pacgum.pixel_x, super_pacgum.pixel_y
                    )
            # Si le zombie attrape le joueur, Game Over
            for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
                    if (abs(self.player.pixel_x - ghost.pixel_x) < 0.6 and
                       abs(self.player.pixel_y - ghost.pixel_y) < 0.6):
                        if ghost.is_vulnerable:
                            ghost.reset_param()
                            self.player.score += 200
                        else:
                            self.player.lives -= 1
                            if self.player.lives <= 0:
                                print("Game Over...")
                                return
                            pygame.time.wait(1000)
                            self._reset_all_param()

            pygame.display.flip()
            clock.tick(60)

    def _show_game_over(self) -> None:
        """The Game Over screen
        Save score -> enter player Name
        New_Game_BTN
        Exti_BTN"""
        pass
