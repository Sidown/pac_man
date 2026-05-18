import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface

from ghost import Blinky, Clyde, Inky, Pinky, Player
from not_corner import not_corner
from pacgum import Pacgum, SuperPacgum
from theme import Theme


class GameScene:
    def __init__(
        self, screen: Surface, theme: Theme, width_height: tuple[int, int]
    ) -> None:
        self.current_scene = "game"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.WIDTH, self.HEIGHT = width_height
        self.PADDING = 80
        self.paused = False
        self.maze = MazeGenerator(
            size=(15, 15),
            entry_cell=(0, 0),
            exit_cell=(-1, -1),
            seed=42,
        )
        self.maze.generate()
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

        self.pacgums = {}
        for y, row in enumerate(self.maze.maze):
            for x, _ in enumerate(row):
                if self.maze.maze[y][x] != 15 and not_corner(self.maze, x, y):
                    self.pacgums.update(
                        {(x, y): Pacgum(20, (x, y), "./assets/skin/other/dot.png",
                                        self.cell_width, self.cell_height)}
                    )
        super_pacgums_coord = [
            (0, 0),
            (0, len(self.maze.maze) - 1),
            (len(self.maze.maze[0]) - 1, 0),
            (len(self.maze.maze[0]) - 1, len(self.maze.maze) - 1)
        ]
        self.super_pacgums = {}
        for coord in super_pacgums_coord:
            self.super_pacgums.update(
                {coord: SuperPacgum(100, coord, "./assets/skin/other/sdot.png",
                                    self.cell_width, self.cell_height)}
            )

        self.player = Player(
            3,
            14,
            14,
            self.maze,
            self.pacgums,
            self.super_pacgums,
            self.cell_height,
            self.cell_width
        )

        self.blinky = Blinky(
            "./assets/skin/ghosts/blinky.png",
            0, 0,
            self.maze,
            self.player,
            self.cell_width,
            self.cell_height
        )
        self.pinky = Pinky(
            "./assets/skin/ghosts/pinky.png",
            0,
            len(self.maze.maze) - 1,
            self.maze,
            self.player,
            self.cell_width,
            self.cell_height
        )
        self.inky = Inky(
            "./assets/skin/ghosts/inky.png",
            len(self.maze.maze[0]) - 1,
            0,
            self.maze,
            self.player,
            self.cell_width,
            self.cell_height,
            self.blinky,
            self.pinky
        )
        self.clyde = Clyde(
            "./assets/skin/ghosts/clyde.png",
            len(self.maze.maze[0]) - 1,
            len(self.maze.maze) - 1,
            self.maze,
            self.player,
            self.cell_width,
            self.cell_height
        )

        self.skin_index = 0
        self.skin_timer = 0
        self.animation_speed = 0.3
        self.life_skin = pygame.transform.scale(
            pygame.image.load("assets/skin/pacman.png"),
            (self.cell_width, self.cell_height),
        )
        self.score_font = pygame.font.Font(
            self.theme.font_path, self.theme.text_size)

    def _print_life(self) -> None:
        nb_life = self.player.lives
        width = 0
        for life in range(nb_life):
            self.screen.blit(
                self.life_skin,
                (
                    self.PADDING + width,
                    self.PADDING
                    + (self.maze_height * self.cell_height)
                    + (2 * self.cell_height),
                ),
            )
            width += self.life_skin.get_width() + 5

    def _print_score(self) -> None:
        score_text = self.score_font.render(f"Score: {self.player.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (self.PADDING, 15))

    def _update_pacman_skin(self) -> None:
        self.skin_timer += self.animation_speed
        if self.skin_timer >= 1:
            self.skin_timer = 0
            self.skin_index = (
                (self.skin_index + 1) % 3
            )  # car 3 images par pacman direction.
        if self.player.direction == "N":
            self.player.skin = self.player.skin_dict["N"][self.skin_index]
        if self.player.direction == "S":
            self.player.skin = self.player.skin_dict["S"][self.skin_index ]
        if self.player.direction == "W":
            self.player.skin = self.player.skin_dict["W"][self.skin_index]
        if self.player.direction == "E":
            self.player.skin = self.player.skin_dict["E"][self.skin_index]

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

    def _game_over(self) -> None:
        self.current_scene = "game_over"

    def handle_events(self, events) -> str:
        for event in events:
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
                    self.paused = not self.paused
        return self.current_scene

    def update(self):
        if self.paused:
            return
        self.blinky.play()
        self.inky.play()
        self.pinky.play()
        self.clyde.play()
        self.player.update_player()
        if self.player.direction != "":
            self._update_pacman_skin()
        for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
            if (
                abs(self.player.pixel_x - ghost.pixel_x) < 0.6
                and abs(self.player.pixel_y - ghost.pixel_y) < 0.6
            ):
                if ghost.is_vulnerable:
                    # skin de ghost devient eyes.png
                    # ghost.skin = self.eyes_skin
                    # ghost fait le chemin pour aller a son spawn
                    #  reset param
                    ghost.die()
                    self.player.score += 200
                else:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        print("Game Over...")
                        self._game_over()
                    pygame.time.wait(1000)
                    self._reset_all_param()

    def draw(self):
        self.screen.fill(self.theme.game_background_color)
        if self.paused:
            pause_text = pygame.font.Font(self.theme.font_path, 56).render(
                "PAUSED", True, (255, 0, 100)
            )
            self.screen.blit(
                pause_text,
                pause_text.get_rect(
                    center=(
                        (self.WIDTH // 2),
                        (self.HEIGHT // 2),
                    )
                ),
            )
        else:
            self._print_maze()
            self._print_skin(self.player.skin, self.player.pixel_x, self.player.pixel_y)
            blinky_surface = (
                self.blinky.vulnerable_skin if self.blinky.is_vulnerable
                else self.blinky.default_skin
            )
            self._print_skin(
                blinky_surface,
                self.blinky.pixel_x,
                self.blinky.pixel_y,
            )
            pinky_surface = (
                self.pinky.vulnerable_skin if self.pinky.is_vulnerable
                else self.pinky.default_skin
            )
            self._print_skin(
                pinky_surface,
                self.pinky.pixel_x,
                self.pinky.pixel_y,
            )
            inky_surface = (
                self.inky.vulnerable_skin if self.inky.is_vulnerable
                else self.inky.default_skin
            )
            self._print_skin(
                inky_surface,
                self.inky.pixel_x,
                self.inky.pixel_y,
            )
            clyde_surface = (
                self.clyde.vulnerable_skin if self.clyde.is_vulnerable
                else self.clyde.default_skin
            )
            self._print_skin(
                clyde_surface,
                self.clyde.pixel_x,
                self.clyde.pixel_y,
            )
            for pacgum in self.pacgums.values():
                if pacgum.visible:
                    self._print_skin(pacgum.skin, pacgum.pixel_x, pacgum.pixel_y)
            for super_pacgum in self.super_pacgums.values():
                if super_pacgum.visible:
                    self._print_skin(
                        super_pacgum.skin,
                        super_pacgum.pixel_x,
                        super_pacgum.pixel_y,
                    )
            self._print_life()
            self._print_score()
