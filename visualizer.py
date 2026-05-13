import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Rect, Surface, time

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
    ) -> None:
        self.WIDTH = 960
        self.HEIGHT = 720
        self.PADDING = 150
        self.maze: MazeGenerator = maze
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
        self.blinky: Blinky = blinky
        self.pinky: Pinky = pinky
        self.inky: Inky = inky
        self.clyde: Clyde = clyde
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
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if btn_back_to_main_menu.rect.collidepoint(x, y):
                btn_back_to_main_menu.set_color((200, 200, 200))
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    self.run()
                    return

        curr_x = self.PADDING
        curr_y = self.PADDING

        # afficher le maze
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

    def _is_neighbor(
        self, current_cell: tuple[int, int], next_cell: tuple[int, int], opp_code: int
    ) -> bool:
        """A function to know if the movement to the next cell is possible."""
        curr_x, curr_y = current_cell
        next_x, next_y = next_cell
        # print(f"curr_x: {curr_x} | curr_y: {curr_y}")
        # print(f"next_x: {next_x} | next_y: {next_y}")
        # if player want to go up:
        if curr_y > next_y:
            # print("I want to go up")
            if not opp_code & 0b0001:
                return True
        # if player want to go down:
        elif curr_y < next_y:
            # print("I want to go to down")
            if not opp_code & 0b0100:
                return True
        # if player want to go right:
        elif curr_x < next_x:
            # print("I want to go to the right")
            if not opp_code & 0b0010:
                return True
        elif curr_x > next_x:
            # print("I want to go to the left")
            if not opp_code & 0b1000:
                return True
        else:
            return False
        return False

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

    def _print_skin(self, skin: Surface, x_cell, y_cell) -> None:
        """A function that print a Skin on the maze."""
        self.screen.blit(
            skin,
            (
                self.PADDING + x_cell * (self.border_size + self.cell_width),
                self.PADDING + y_cell * (self.border_size + self.cell_height),
            ),
        )

    def _update_player(self):
        """update the player position and player movement pixel by pixel"""
        player = self.player
        if player.move_progress >= 1.0:
            player.x = player.next_x
            player.y = player.next_y
            direction_x, direction_y = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0),
            }.get(player.queud_direction, (0, 0))

            new_x, new_y = player.x + direction_x, player.y + direction_y
            if direction_x != 0 or direction_y != 0:
                if self._is_neighbor(
                    (player.x, player.y),
                    (new_x, new_y),
                    self.maze.maze[player.y][player.x],
                ):
                    player.next_x, player.next_y = new_x, new_y
                    player.direction = player.queud_direction
                    player.move_progress = 0.0

            direction_x, direction_y = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0),
            }.get(player.direction, (0, 0))
            new_x, new_y = player.x + direction_x, player.y + direction_y
            if direction_x != 0 or direction_y != 0:
                if self._is_neighbor(
                    (player.x, player.y),
                    (new_x, new_y),
                    self.maze.maze[player.y][player.x],
                ):
                    player.next_x, player.next_y = new_x, new_y
                    player.move_progress = 0.0
                    return

        player.move_progress = min(1.0, player.move_progress + player.speed)
        player.pixel_x = player.x + (player.next_x - player.x) * player.move_progress
        player.pixel_y = player.y + (player.next_y - player.y) * player.move_progress

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
        font = pygame.font.Font("assets/fonts/shlop rg.otf", 28)
        life_nb = font.render("Life number: ", False, (0, 0, 0))
        current_score = font.render("Current score: ", False, (0, 0, 0))
        highest_score = font.render("Highest score: ", False, (0, 0, 0))
        self.screen.blit(life_nb, (x1 + 5, y1))
        self.screen.blit(current_score, (x1 + 5, y1 + 32))
        self.screen.blit(highest_score, (x1 + 5, y1 + 64))

        # affichage des valeurs NB LIFE, HIGHSCORE ...
        player_lives = font.render(f"{self.player.lives}", False, (0, 0, 0))
        self.screen.blit(player_lives, (x1 + life_nb.get_width() + 5, y1))
        pass

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
            self.screen.blit(self.bg, (0, 0))
            self.blinky.play()
            self.inky.play()
            self.pinky.play()
            self.clyde.play()
            self._print_maze()
            self._print_HUD()

            # deplacer le personnage
            self._update_player()
            self._print_skin(self.player.skin, self.player.pixel_x, self.player.pixel_y)
            # moins bon en perf de recharger l'image a chaque fois
            self._print_skin(
                pygame.transform.scale(
                    pygame.image.load(self.blinky.skin),
                    (self.cell_width, self.cell_height),
                ),
                self.blinky.pixel_x,
                self.blinky.pixel_y,
            )
            self._print_skin(
                pygame.transform.scale(
                    pygame.image.load(self.pinky.skin),
                    (self.cell_width, self.cell_height),
                ),
                self.pinky.pixel_x,
                self.pinky.pixel_y,
            )
            self._print_skin(
                pygame.transform.scale(
                    pygame.image.load(self.inky.skin),
                    (self.cell_width, self.cell_height),
                ),
                self.inky.pixel_x,
                self.inky.pixel_y,
            )
            self._print_skin(
                pygame.transform.scale(
                    pygame.image.load(self.clyde.skin),
                    (self.cell_width, self.cell_height),
                ),
                self.clyde.pixel_x,
                self.clyde.pixel_y,
            )
            # Si le zombie attrape le joueur, Game Over
            if (
                ((self.player.x == self.blinky.x) and (self.player.y == self.blinky.y))
                or ((self.player.x == self.pinky.x) and (self.player.y == self.pinky.y))
                or ((self.player.x == self.inky.x) and (self.player.y == self.inky.y))
                or ((self.player.x == self.clyde.x) and (self.player.y == self.clyde.y))
            ):
                # continue  # a supprimer plus tard
                print(f"life: {self.player.lives}")
                self.player.lives -= 1
                if self.player.lives <= 0:
                    print("Game Over...")
                    return
                # relancer le jeu depuis le debut
                pygame.time.wait(1000)
                self.player.x, self.player.y = (
                    self.player.next_x,
                    self.player.next_y,
                ) = self.player.spawn
                self.player.direction = self.player.queud_direction = ""
                print(f"player.x= {self.player.x}, player.y= {self.player.y}")
                self.blinky.x, self.blinky.y = (
                    self.blinky.next_x,
                    self.blinky.next_y,
                ) = self.blinky.spawn
                self.inky.x, self.inky.y = self.inky.next_x, self.inky.next_y = (
                    self.inky.spawn
                )
                self.pinky.x, self.pinky.y = self.pinky.next_x, self.pinky.next_y = (
                    self.pinky.spawn
                )
                self.clyde.x, self.clyde.y = self.clyde.next_x, self.clyde.next_y = (
                    self.clyde.spawn
                )
                game_running = False
                self._show_game()
            pygame.display.flip()
            clock.tick(10)
        return

    def _show_game_over(self) -> None:
        """The Gane Over screen"""
        pass
