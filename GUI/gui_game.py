import sys
from typing import cast

import pygame
from pygame import Surface
from pygame.event import Event

from game_class.cheat import Cheat
from game_class.game import Game
from game_class.ghost import Blinky, Clyde, Inky, Pinky
from game_class.player import Player
from parser import Config

from .checkbox import Checkbox
from .scene import Scene
from .score import HighScore
from .ui_elements.button import Button
from .ui_elements.theme import Theme


class GameScene(Scene):
    """
    the main scene of the game
    """

    def __init__(
        self,
        screen: Surface,
        theme: Theme,
        width_height: tuple[int, int],
        config: Config,
        player: Player,
        highscore: HighScore,
        cheat: Cheat,
    ) -> None:
        """
        Initialise the GameScene
        arguments:
        screen -> the pygame surface
        theme -> the visual theme
        width_height -> width and height of the window in pixels
        config -> the game configuration
        player -> the player
        highscore -> the highscore manager
        cheat -> the cheat class
        """
        self.time_elapsed = 0
        self.time_last_frame = 0
        self.current_scene = "game"
        self.screen: Surface = screen
        self.theme: Theme = theme
        self.player: Player = player
        self.WIDTH: int = width_height[0]
        self.HEIGHT: int = width_height[1]
        self.PADDING = 80
        self.paused = False
        self.game = Game((self.WIDTH, self.HEIGHT), self.PADDING, config,
                         self.player)
        self.skin_index = 0
        self.skin_timer = 0
        self.animation_speed = 0.3
        self.current_level_index = 0
        self.score_font = pygame.font.Font(self.theme.font_path,
                                           self.theme.text_size)
        self.highscore: HighScore = highscore
        self.highscore.load_high_score()
        self.cheat = cheat

        self.invincibility_checkbox = Checkbox(
            self.screen,
            self.WIDTH // 2.5,
            self.HEIGHT / 2.4,
            1,
            caption="Invincibility",
        )
        self.freeze_checkbox = Checkbox(
            self.screen,
            self.WIDTH // 2.5,
            self.HEIGHT / 2,
            2,
            caption="Freeze Ghosts",
        )
        self.skip_checkbox = Checkbox(
            self.screen,
            self.WIDTH // 2.5,
            self.HEIGHT / 1.7,
            3,
            caption="Skip Levels (press Return)",
        )

        self.btn_back_to_menu = Button(
            self.screen,
            self.theme.text_size,
            self.theme.font_path,
            self.theme.text_color,
            (0, 0, 0),
            "Back to Main Menu",
            self._back_to_menu_callback,
            (50, 50),
            False,
            (100, 100, 100),
            self.theme.btn_on_mouse_over_text_color,
        )

        self.timeless_checkbox = Checkbox(
            self.screen,
            self.WIDTH // 2.5,
            self.HEIGHT / 1.8,
            3,
            caption="No Timer",
        )

    def load_level(self) -> None:
        """
        Load the current level from the Game class
        """
        level = self.game.get_level(self.current_level_index)
        self.maze = level.maze
        self.maze_height = len(self.maze.maze)
        self.maze_width = len(self.maze.maze[0])
        self.cell_width = level.cell_width
        self.cell_height = level.cell_height
        self.pacgums = level.pacgums
        self.super_pacgums = level.super_pacgums
        self.blinky: Blinky = cast(Blinky, level.ghosts["blinky"])
        self.pinky: Pinky = cast(Pinky, level.ghosts["pinky"])
        self.inky: Inky = cast(Inky, level.ghosts["inky"])
        self.clyde: Clyde = cast(Clyde, level.ghosts["clyde"])
        self.life_skin = pygame.transform.scale(
            pygame.image.load("assets/skin/pacman.png"),
            (self.cell_width, self.cell_height),
        )
        self.score_font = pygame.font.Font(self.theme.font_path,
                                           self.theme.text_size)
        self.player._set_pacgum_pos(self.pacgums, self.super_pacgums)
        self.player._set_skins(self.cell_width, self.cell_height)
        self.player.spawn = self._check_spawn_is_valid(
            (self.player.spawn[0], self.player.spawn[1])
        )
        self.player.respawn()
        self.time_elapsed = 0
        self.time_last_frame = 0
    def _print_life(self) -> None:
        """
        Draw player life
        """
        nb_life = self.player.lives
        width = 0
        for life in range(nb_life):
            self.screen.blit(
                self.life_skin,
                (self.PADDING + width, self.HEIGHT - self.PADDING),
            )
            width += self.life_skin.get_width() + 5

    def _print_level(self) -> None:
        """
        display the current level number
        """
        level_text = self.score_font.render(
            f"level: {self.current_level_index + 1}", True, self.theme.text_color
        )
        self.screen.blit(
            level_text,
            (
                self.WIDTH - level_text.get_width() - self.PADDING,
                self.HEIGHT - self.PADDING,
            ),
        )

    def _print_score(self) -> None:
        """
        display the current player score
        """
        score_text = self.score_font.render(
            f"Score: {self.highscore.current_score}", True, self.theme.text_color
        )
        self.screen.blit(score_text, (self.PADDING, 15))

    def _print_timer(self) -> None:
        """
        Display the current level timer
        """
        level = self.game.get_level(self.current_level_index)
        time_remaining = max(0, (level.max_time - self.time_elapsed) // 1000)
        timer_text = self.score_font.render(
            f"Timer: {time_remaining}", True, self.theme.text_color
        )
        self.screen.blit(timer_text, (self.PADDING * 5, 15))

    def _show_maze(self, curr_x: float, curr_y: float) -> None:
        """
        print every cell of the maze
        arguments:
        curr_x -> starting pixel x coord
        curr_y -> starting pixel y coord
        """
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
        """
        draw the wall of a cell maze
        arguments:
        x -> pixel x coord of the cell
        y -> pixel y coord of the cell
        cell_width -> width of the cell in pixel
        cell_height -> height of the cell in pixel
        opp_code -> wall bitmask for the cell
        print_east -> if need to print the east border for last column
        print_down -> if need to print the south border for lar row
        """
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
        # si tout les murs sont ferme, c'est le 42 pattern,
        # le mettre en couleur
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

    def _print_skin(self, skin: Surface, x_cell: float, y_cell: float) -> None:
        """
        A function that print a Skin on the maze.
        arguments:
        skin -> the skin to draw
        x_cell -> x position of the cell
        y_cell -> y position of the cell
        """
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
        self.player.respawn()
        self.blinky.reset_param()
        self.inky.reset_param()
        self.pinky.reset_param()
        self.clyde.reset_param()

    def _game_over(self) -> None:
        """
        change the scene for the game over scene
        """
        self.current_scene = "game_over"

    def handle_events(self, events: list[Event]) -> str:
        """
        handle keyboard input and cheat checkbox events
        arguments:
        events -> list of pygame events to process
        return value:
        the scene to display next
        """
        for event in events:
            self.btn_back_to_menu.handle_event(event)
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
            if self.skip_checkbox.update_checkbox(event):
                self._skip_level(self.cheat)
            if self.timeless_checkbox.update_checkbox(event):
                self._timeless(self.cheat)

        return self.current_scene

    def update(self) -> None:
        """
        Move ghost, update player and check collision
        """
        if self.paused:
            return
        remaining_pacgums = 0
        for key in self.pacgums.keys():
            if self.pacgums[key].visible:
                remaining_pacgums += 1
        if (
            remaining_pacgums <= len(self.pacgums) // 5
            and not self.blinky.is_vulnerable
        ):
            self.blinky.angry_mod
        self.blinky.play(self.maze, self.player, self.cheat)
        self.inky.play(self.maze, self.player, self.cheat,
                       self.blinky, self.pinky)
        self.pinky.play(self.maze, self.player, self.cheat)
        self.clyde.play(self.maze, self.player, self.cheat)
        self.player.update_player(self.maze, self.highscore)
        for ghost in [self.blinky, self.pinky, self.inky, self.clyde]:
            if ghost.collide_with_player(self.player):
                if ghost.is_vulnerable:
                    ghost.die()
                    self.highscore.current_score += 200
                elif not ghost.died and not self.cheat.invincible:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self._game_over()
                        return
                    pygame.time.wait(200)
                    self._reset_all_param()
                    break
        if all(not pacgum.visible for pacgum in self.pacgums.values()):
            self._next_level()
        if not self.paused and not self.cheat.timeless:
            now = pygame.time.get_ticks()
            if self.time_last_frame > 0:
                self.time_elapsed += now - self.time_last_frame
            self.time_last_frame = now
            level = self.game.get_level(self.current_level_index)
            time_ramaining = level.max_time - self.time_elapsed
            if time_ramaining <= 0:
                self._game_over()
                return

    def _print_highscore(self) -> None:
        """Print the Highscore."""
        if len(self.highscore.scores) == 0:
            highest_score = 0
        else:
            highest_score = int(self.highscore.scores[0][1])
        highscore_text = self.score_font.render(
            f"HighScore: {highest_score}", True, self.theme.text_color
        )
        self.screen.blit(highscore_text, (self.WIDTH // 2 + 120, 15))

    def _next_level(self) -> None:
        """
        Advance to the next level or show victory scene if all levels
        are done
        """
        self.current_level_index += 1
        if self.current_level_index >= len(self.game.level_configs):
            self.current_scene = "victory"
            return
        # old_score = self.highscore.current_score
        old_lives = self.player.lives
        self.load_level()
        spawn_x, spawn_y = self._check_spawn_is_valid(
            ((self.maze_width // 2), (self.maze_height // 2))
        )
        self.player.spawn = (spawn_x, spawn_y)
        self.player.respawn()
        # self.player.score = old_score
        self.player.lives = old_lives

    def _invincibility(self, cheat: Cheat) -> None:
        """
        Activate or desactivate the invincibility cheat depending on
        the corresponding checkbox
        arguments:
        cheat -> the cheat class
        """
        if self.invincibility_checkbox.checked:
            cheat.invincible = True
        else:
            cheat.invincible = False

    def _freeze_ghost(self, cheat: Cheat) -> None:
        """
        Activate or desactivate the freeze ghost cheat depending on
        the corresponding checkbox
        arguments:
        cheat -> the cheat class
        """
        if self.freeze_checkbox.checked:
            cheat.freeze = True
        else:
            cheat.freeze = False

    def _skip_level(self, cheat: Cheat) -> None:
        """
        Activate or desactivate the skip level cheat depending on
        the corresponding checkbox
        arguments:
        cheat -> the cheat class
        """
        if self.skip_checkbox.checked:
            cheat.skip = True
        else:
            cheat.skip = False
        
    def _timeless(self, cheat: Cheat) -> None:
        """
        Deactivate timer when checked
        arguments:
        cheat -> the cheat class
        """
        if self.timeless_checkbox.checked:
            cheat.timeless = True
            self.time_last_frame = 0
        else:
            cheat.timeless = False

    def _check_spawn_is_valid(self, coordinate: tuple[int, int]
                              ) -> tuple[int, int]:
        """
        Find the nearest non closed cell starting from coordinate
        arguments:
        coordinate -> starting x,y maze position
        return value:
        a valid x,y spawn coord
        """
        spawn_x, spawn_y = coordinate
        while self.maze.maze[spawn_y][spawn_x] == 15:
            spawn_y = spawn_y - 1
            spawn_x = spawn_x - 1
            if spawn_x < 0 or spawn_y < 0:
                sys.exit()
        return (spawn_x, spawn_y)

    def _back_to_menu_callback(self) -> None:
        """
        reset the player and return to the main menu
        """
        self.player.new_game()
        self.highscore.current_score = 0
        self.current_scene = "main_menu"

    def draw(self) -> None:
        """
        draw the game scene or the pause
        """
        self.screen.fill(self.theme.game_background_color)
        if self.paused:
            self.btn_back_to_menu.draw(self.screen)
            pause_text = pygame.font.Font(self.theme.font_path, 56).render(
                "PAUSED", True, (255, 0, 100)
            )
            self.screen.blit(
                pause_text,
                pause_text.get_rect(
                    center=(
                        (self.WIDTH // 2),
                        (self.PADDING * 2),
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
                        (self.PADDING * 3),
                    )
                ),
            )
            self.invincibility_checkbox.draw()
            self.freeze_checkbox.draw()
            self.skip_checkbox.draw()
            self.timeless_checkbox.draw()

        else:
            self._print_maze()
            assert self.player.skin is not None, "Player skin not loaded"
            self._print_skin(self.player.skin, self.player.pixel_x,
                             self.player.pixel_y)
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
            self._print_timer()
            self._print_highscore()
            self._print_level()
