import pygame
from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface

from game import Game
from parser import Config
from player import Player
from scene import Scene
from score import HighScore
from theme import Theme, Button
from checkbox import Checkbox


class GameScene(Scene):
    def __init__(
        self,
        screen: Surface,
        theme: Theme,
        width_height: tuple[int, int],
        config: Config,
        player: Player,
        highscore: HighScore,
        cheat
    ) -> None:
        self.current_scene = "game"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.player: Player = player
        self.WIDTH, self.HEIGHT = width_height
        self.PADDING = 80
        self.paused = False
        self.game = Game((self.WIDTH, self.HEIGHT), self.PADDING, config, self.player)
        self.current_level = 0
        # self.load_level(self.current_level)
        self.skin_index = 0
        self.skin_timer = 0
        self.animation_speed = 0.3
        self.current_level_index = 0
        self.score_font = pygame.font.Font(self.theme.font_path, self.theme.text_size)
        self.highscore: HighScore = highscore
        self.highscore.load_high_score()
        self.cheat = cheat

        self.invincibility_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 3.5, 1,
                                               caption="Invincibility")
        self.freeze_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 2.6, 2,
                                               caption="Freeze Ghosts")
        self.pacgum_checkbox = Checkbox(self.screen, self.WIDTH // 2.5,
                                               self.HEIGHT / 2.1, 3,
                                               caption="Skip Levels")

    def _cheat_callback(self) -> None:
        self.current_scene = "cheat"

    def load_level(self) -> None:
        level = self.game.get_level(self.current_level_index)
        self.maze = level.maze
        self.maze_height = len(self.maze.maze)
        self.maze_width = len(self.maze.maze[0])
        self.cell_width = level.cell_width
        self.cell_height = level.cell_height
        self.pacgums = level.pacgums
        self.super_pacgums = level.super_pacgums
        # self.player = level.player
        self.blinky = level.ghosts["blinky"]
        self.pinky = level.ghosts["pinky"]
        self.inky = level.ghosts["inky"]
        self.clyde = level.ghosts["clyde"]
        self.life_skin = pygame.transform.scale(
            pygame.image.load("assets/skin/pacman.png"),
            (self.cell_width, self.cell_height),
        )
        self.score_font = pygame.font.Font(self.theme.font_path, self.theme.text_size)
        self.player._set_pacgum_pos(self.pacgums, self.super_pacgums)
        self.player._set_skins(self.cell_width, self.cell_height)

    def _print_life(self) -> None:
        nb_life = self.player.lives
        width = 0
        for life in range(nb_life):
            self.screen.blit(
                self.life_skin,
                (self.PADDING + width, self.HEIGHT - self.PADDING),
            )
            width += self.life_skin.get_width() + 5

    def _print_score(self) -> None:
        score_text = self.score_font.render(
            f"Score: {self.player.score}", True, self.theme.text_color
        )
        self.screen.blit(score_text, (self.PADDING, 15))

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
                    # self.theme.wall_size,
                    # self.theme.wall_color,
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
                if event.key == pygame.K_RETURN and self.cheat.skip:
                    self._next_level()
            if self.invincibility_checkbox.update_checkbox(event):
                self._invincibility(self.cheat)
            if self.freeze_checkbox.update_checkbox(event):
                self._freeze_ghost(self.cheat)
            if self.pacgum_checkbox.update_checkbox(event):
                self._skip_level(self.cheat)

        return self.current_scene

    def update(self):
        if self.paused:
            return
        remaining_pacgums = 0
        for key in self.pacgums.keys():
            if self.pacgums[key].visible:
                remaining_pacgums += 1
        if remaining_pacgums <= len(self.pacgums) // 5:
            self.blinky.angry_mod
        self.blinky.play(self.maze, self.player, self.cheat)
        self.inky.play(self.maze, self.player, self.cheat, self.blinky, self.pinky)
        self.pinky.play(self.maze, self.player, self.cheat)
        self.clyde.play(self.maze, self.player, self.cheat)
        self.player.update_player(self.maze)
        for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
            if ghost.collide_with_player(self.player):
                if ghost.is_vulnerable:
                    ghost.die()
                    self.player.score += 200
                elif not ghost.died and not self.cheat.invincible:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        # sauvegarder le score. le joueur a perdu
                        self._game_over()
                        return
                    pygame.time.wait(1000)
                    self._reset_all_param()
        if all(not pacgum.visible for pacgum in self.pacgums.values()):
            self._next_level()

    def _print_highscore(self) -> None:
        """Print the Highscore."""
        if len(self.highscore.scores) == 0:
            highest_score = 0
        else:
            highest_score = self.highscore.scores[0][1]
        highscore_text = self.score_font.render(
            f"HighScore: {highest_score}", True, self.theme.text_color
        )
        self.screen.blit(highscore_text, (self.WIDTH // 2, 15))

    def _next_level(self):
        self.current_level_index += 1
        if self.current_level_index >= len(self.game.level_configs):
            # sauvegarder le score. le joueur a gagne
            self.current_scene = "game_over"  # changer la scene, c'est victory_scene
            return
        old_score = self.player.score
        old_lives = self.player.lives
        self.load_level()
        # remettre le player a son spawn
        # TODO: CHECK LE SPAWN HORS 42.
        self.player.spawn = (self.maze_width // 2, self.maze_height // 2)
        self.player.reset_param()
        self.player.score = old_score
        self.player.lives = old_lives

    def _invincibility(self, cheat):
        if self.invincibility_checkbox.checked:
            cheat.invincible = True
            print(f"invincibility checked, value: {cheat.invincible}")
        else:
            cheat.invincible = False
            print(f"invincibility unchecked, value: {cheat.invincible}")

    def _freeze_ghost(self, cheat):
        if self.freeze_checkbox.checked:
            cheat.freeze = True
            print(f"freeze checked, value: {cheat.freeze}")
        else:
            cheat.freeze = False
            print(f"freeze unchecked, value: {cheat.freeze}")

    def _skip_level(self, cheat):
        if self.pacgum_checkbox.checked:
            cheat.skip = True
            print(f"skip checked, value: {cheat.skip}")
        else:
            cheat.skip = False
            print(f"skip unchecked, value: {cheat.skip}")

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
                        (self.PADDING),
                    )
                ),
            )
            cheat_text = pygame.font.Font(self.theme.font_path, 36).render(
                "Cheats (for loosers only):", True, (255, 255, 255)
            )
            self.screen.blit(
                cheat_text,
                cheat_text.get_rect(
                    center=(
                        (self.WIDTH // 2),
                        (self.PADDING * 2),
                    )
                ),
            )
            self.invincibility_checkbox.draw()
            self.freeze_checkbox.draw()
            self.pacgum_checkbox.draw()

        else:
            self._print_maze()
            self._print_skin(self.player.skin, self.player.pixel_x, self.player.pixel_y)
            self._print_skin(
                self.blinky.current_skin,
                self.blinky.pixel_coord[0],
                self.blinky.pixel_coord[1],
            )
            self._print_skin(
                self.pinky.current_skin,
                self.pinky.pixel_coord[0],
                self.pinky.pixel_coord[1],
            )
            self._print_skin(
                self.inky.current_skin,
                self.inky.pixel_coord[0],
                self.inky.pixel_coord[1],
            )
            self._print_skin(
                self.clyde.current_skin,
                self.clyde.pixel_coord[0],
                self.clyde.pixel_coord[1],
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
            self._print_highscore()
