import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface, time

from ghost import Blinky, Clyde, Inky, Pinky, Player
from pacgum import Pacgum, SuperPacgum
from theme import Button, Text, Theme


class Visualizer:
    """"""

    def __init__(
        self,
        maze: MazeGenerator,
        theme: Theme,
        blinky: Blinky,
        pinky: Pinky,
        inky: Inky,
        clyde: Clyde,
        player: Player,
        pacgums: dict[tuple[int], Pacgum],
        super_pacgums: dict[tuple[int], SuperPacgum],
    ) -> None:
        self.WIDTH = 960
        self.HEIGHT = 720
        self.PADDING = 80
        self.maze: MazeGenerator = maze
        self.theme: Theme = theme
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
        self.player: Player = player
        self.player.skin = pygame.transform.scale(
            pygame.image.load("assets/skin/skin_survivor.png"),
            (self.cell_width, self.cell_height),
        )
        self.vulnerable_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/ghosts/blue_ghost.png"),
            (self.cell_width, self.cell_height),
        )
        self.blinky: Blinky = blinky
        self.blinky_skin = pygame.transform.scale(
            pygame.image.load(self.blinky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.pinky: Pinky = pinky
        self.pinky_skin = pygame.transform.scale(
            pygame.image.load(self.pinky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.inky: Inky = inky
        self.inky_skin = pygame.transform.scale(
            pygame.image.load(self.inky.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.clyde: Clyde = clyde
        self.clyde_skin = pygame.transform.scale(
            pygame.image.load(self.clyde.actual_skin),
            (self.cell_width, self.cell_height),
        )
        self.pacgums: dict[tuple[int], Pacgum] = pacgums
        self.pacgums_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/other/dot.png"),
            (self.cell_width, self.cell_height),
        )
        self.super_pacgums: dict[tuple[int], SuperPacgum] = super_pacgums
        self.super_pacgums_skin = pygame.transform.scale(
            pygame.image.load("./assets/skin/other/sdot.png"),
            (self.cell_width, self.cell_height),
        )

        pygame.init()

    def manage_mouse_click(self, btn_game, btn_high_score, btn_instruction, btn_exit):
        """Managed mouse click"""
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            if btn_game.rect.collidepoint(x, y):
                btn_game.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    self._show_game()
            if btn_high_score.rect.collidepoint(x, y):
                btn_high_score.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("let's view the highest score!")
            if btn_instruction.rect.collidepoint(x, y):
                btn_instruction.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    print("let's view the highest score!")
            if btn_exit.rect.collidepoint(x, y):
                btn_exit.on_mouse_over()
                pressed = pygame.mouse.get_pressed()
                if pressed[0]:
                    pygame.quit()

    def _show_instructions(self) -> None:
        """Show the Game instructions."""
        """
        === Instructions ===
        You are PacMan, a little yellow guy.
        Four ghosts are chassing you, Inky, Blinky, Pinky and Clyde.
        Your goal is to eat all the Pacgum of the level.
        When you have eat all the PacGum, you will go to the next level of the game.
        There are 10 level to complete if you want to win the game.
        Also if you eat a ghost you will earn extra point.
        Ghosts are eatable for a short amount of time if you eat a Super Pac-Gum before.
        Try to survive and do the best score possible. Good Luck."""

    def _show_main_menu(self) -> None:
        """Show the home page of the Pac-Man game."""

        header = Text(
            self.screen,
            self.theme.header_size,
            self.theme.font_path,
            self.theme.title_color,
            self.theme.background_color,
            "PACMAN",
            ((self.WIDTH // 2), 50),
            True,
            False,
        )

        btn_game = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "New Game",
            ((self.WIDTH // 2), 250),
            True,
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        btn_high_score = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "View High Score",
            ((self.WIDTH // 2), 350),
            True,
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        btn_instruction = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "View Instructions",
            ((self.WIDTH // 2), 450),
            True,
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        btn_exit = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            self.theme.background_color,
            "Exit",
            ((self.WIDTH // 2), 550),
            True,
            False,
            self.theme.btn_on_mouse_over_background_color,
            self.theme.btn_on_mouse_over_text_color,
        )

        header.create()
        btn_game.create()
        btn_high_score.create()
        btn_instruction.create()
        btn_exit.create()

        self.manage_mouse_click(btn_game, btn_high_score, btn_instruction, btn_exit)

    def run(self) -> None:
        """The full game visualisation"""
        pygame.display.set_caption("Pac-Man")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.theme.background_color)
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
                    self.theme.wall_size,
                    self.theme.wall_color,
                    print_right,
                    print_down,
                )
                curr_x += self.cell_width + (self.theme.wall_size)
            curr_x = self.PADDING
            curr_y += self.cell_height + (self.theme.wall_size)

    def _print_maze(self) -> None:
        """Print the maze."""

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
                self.theme.wall_color,
                (x, y),
                (x + cell_width + self.theme.wall_size, y),
                self.theme.wall_size,
            )
        # east border
        if (opp_code & 0b0010) and print_east:
            pygame.draw.line(
                self.screen,
                self.theme.wall_color,
                (x + self.theme.wall_size + cell_width, y),
                (
                    x + cell_width + self.theme.wall_size,
                    y + cell_height + self.theme.wall_size,
                ),
                self.theme.wall_size,
            )
        # south border
        if (opp_code & 0b0100) and print_down:
            pygame.draw.line(
                self.screen,
                self.theme.wall_color,
                (x, y + cell_height + self.theme.wall_size),
                (
                    x + cell_width + self.theme.wall_size,
                    y + cell_height + self.theme.wall_size,
                ),
                self.theme.wall_size,
            )
        # west border
        if opp_code & 0b1000:
            pygame.draw.line(
                self.screen,
                self.theme.wall_color,
                (x, y),
                (x, y + cell_height + self.theme.wall_size),
                self.theme.wall_size,
            )
        # si tout les murs sont ferme, c'est le 42 pattern, le mettre en couleur
        if opp_code == 15:
            pygame.draw.rect(
                self.screen,
                self.theme.wall_color,
                (
                    x,
                    y,
                    self.cell_width + self.theme.wall_size,
                    self.cell_height + self.theme.wall_size,
                ),
            )

    def _print_skin(self, skin: Surface, x_cell, y_cell) -> None:
        """A function that print a Skin on the maze."""
        self.screen.blit(
            skin,
            (
                self.PADDING
                + (self.theme.wall_size / 2)
                + x_cell * (self.theme.wall_size + self.cell_width),
                self.PADDING
                + (self.theme.wall_size / 2)
                + y_cell * (self.theme.wall_size + self.cell_height),
            ),
        )

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
            self.screen.fill(self.theme.game_background_color)
            self.screen.blit(self.screen, (0, 0))
            self.blinky.play()
            self.inky.play()
            self.pinky.play()
            self.clyde.play()
            self._print_maze()

            # deplacer le personnage
            self.player.update_player()
            self._print_skin(self.player.skin, self.player.pixel_x, self.player.pixel_y)
            # moins bon en perf de recharger l'image a chaque fois
            blinky_surface = (
                self.vulnerable_skin if self.blinky.is_vulnerable else self.blinky_skin
            )
            self._print_skin(
                blinky_surface,
                self.blinky.pixel_x,
                self.blinky.pixel_y,
            )
            pinky_surface = (
                self.vulnerable_skin if self.pinky.is_vulnerable else self.pinky_skin
            )
            self._print_skin(
                pinky_surface,
                self.pinky.pixel_x,
                self.pinky.pixel_y,
            )
            inky_surface = (
                self.vulnerable_skin if self.inky.is_vulnerable else self.inky_skin
            )
            self._print_skin(
                inky_surface,
                self.inky.pixel_x,
                self.inky.pixel_y,
            )
            clyde_surface = (
                self.vulnerable_skin if self.clyde.is_vulnerable else self.clyde_skin
            )
            self._print_skin(
                clyde_surface,
                self.clyde.pixel_x,
                self.clyde.pixel_y,
            )
            for pacgum in self.pacgums.values():
                if pacgum.visible:
                    self._print_skin(self.pacgums_skin, pacgum.pixel_x, pacgum.pixel_y)
            for super_pacgum in self.super_pacgums.values():
                if super_pacgum.visible:
                    self._print_skin(
                        self.super_pacgums_skin,
                        super_pacgum.pixel_x,
                        super_pacgum.pixel_y,
                    )
            # Si le zombie attrape le joueur, Game Over
            for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
                if (
                    abs(self.player.pixel_x - ghost.pixel_x) < 0.6
                    and abs(self.player.pixel_y - ghost.pixel_y) < 0.6
                ):
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
            clock.tick(10)
        return

    def _show_game_over(self) -> None:
        """The Game Over screen
        Save score -> enter player Name
        New_Game_BTN
        Exti_BTN"""
        pass
