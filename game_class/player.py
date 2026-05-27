from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface, image, transform

from .pacgum import Pacgum, SuperPacgum


class Player:
    """Player class representing pacman"""

    def __init__(
        self,
        lives: int,
        spawn_x: int,
        spawn_y: int,
    ) -> None:
        """
        Initialise the player
        arguments:
        lives -> number of lives at the start of the game
        spawn_x -> x spawn cell
        spawn_y -> y spawn cell
        """
        self.default_lives: int = lives
        self.lives: int = self.default_lives
        self.x: int = spawn_x
        self.y: int = spawn_y
        self.spawn: tuple[int, int] = (spawn_x, spawn_y)
        self.next_x: int = self.x
        self.next_y: int = self.y
        self.pixel_x = float(self.x)
        self.pixel_y = float(self.y)
        self.move_progress: float = 1.0
        self.direction: str = ""
        self.queud_direction: str = ""
        self.score: int = 0
        self.speed: float = 0.10
        self.pacgum_effect: bool = False
        self.timer_effect = 0
        self.skin_timer = 0.0
        self.skin_index = 0
        self.animation_speed = 0.3

    def _set_skins(self, cell_width: float, cell_height: float) -> None:
        """
        Load and scale the skins
        arguments:
        cell_width -> width of a maze cell in pixels
        cell_height -> height of a maze cell in pixels
        """
        self.skin: Surface | None = transform.scale(
            image.load("assets/skin/pacman.png"),
            (cell_width, cell_height),
        )
        self.skin_dict = {
            "N": [
                transform.scale(
                    image.load(f"assets/skin/pacman-up/{i}.png"),
                    (cell_width, cell_height),
                )
                for i in range(1, 4)
            ],
            "S": [
                transform.scale(
                    image.load(f"assets/skin/pacman-down/{i}.png"),
                    (cell_width, cell_height),
                )
                for i in range(1, 4)
            ],
            "W": [
                transform.scale(
                    image.load(f"assets/skin/pacman-left/{i}.png"),
                    (cell_width, cell_height),
                )
                for i in range(1, 4)
            ],
            "E": [
                transform.scale(
                    image.load(f"assets/skin/pacman-right/{i}.png"),
                    (cell_width, cell_height),
                )
                for i in range(1, 4)
            ],
        }

    def _set_pacgum_pos(
        self,
        pacgums: dict[tuple[int, int], Pacgum],
        super_pacgums: dict[tuple[int, int], SuperPacgum],
    ) -> None:
        """
        Set the pacgums and super pacgums dicts for this level
        arguments:
        pacgums -> dict of coord as key and pacgum as value
        super_pacgums -> dict of coord as key and super pacgum as value
        """
        self.pacgums: dict[tuple[int, int], Pacgum] = pacgums
        self.super_pacgums: dict[tuple[int, int], SuperPacgum] = super_pacgums

    def reset_param(self) -> None:
        """Reset the player parameters for a new life."""
        self.x, self.y = (
            self.next_x,
            self.next_y,
        ) = self.spawn
        self.direction = self.queud_direction = ""
        self.timer_effect = 0
        self.pacgum_effect = False

    def new_game(self) -> None:
        """
        reset player parameters for a new game
        """
        self.reset_param()
        self.score = 0
        self.lives = self.default_lives

    def _is_neighbor(
        self, current_cell: tuple[int, int], next_cell: tuple[int, int],
        opp_code: int
    ) -> bool:
        """
        A function to know if the movement to the next cell is possible.
        arguments:
        current_cell -> x,y coord of the actual cell
        next_cell-> x,y coor of the next cell
        opp_code -> bitmask of the current cell
        return value:
        true if the move if valid
        false otherwise
        """
        curr_x, curr_y = current_cell
        next_x, next_y = next_cell
        if curr_y > next_y:
            if not opp_code & 0b0001:
                return True
        elif curr_y < next_y:
            if not opp_code & 0b0100:
                return True
        elif curr_x < next_x:
            if not opp_code & 0b0010:
                return True
        elif curr_x > next_x:
            if not opp_code & 0b1000:
                return True
        else:
            return False
        return False

    def update_player(self, maze: MazeGenerator) -> None:
        """
        update the player position, player movement pixel by
        pixel and player skin
        arguments:
        maze -> the current maze
        """
        if self.timer_effect > 0:
            self.timer_effect -= 1
        if self.timer_effect == 0 and self.pacgum_effect:
            self.pacgum_effect = False

        DIRECTIONS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        opposite = opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}

        if self.move_progress < 1.0 and self.queud_direction == opposite.get(
            self.direction
        ):
            self.next_x, self.next_y, self.x, self.y = (
                self.x,
                self.y,
                self.next_x,
                self.next_y,
            )
            self.direction = self.queud_direction
            self.move_progress = 1.0 - self.move_progress
            self.queud_direction = ""

        if self.move_progress >= 1.0:
            self.x = self.next_x
            self.y = self.next_y

            moved = False
            for direction in [self.queud_direction, self.direction]:
                if not direction:
                    continue

                direction_x, direction_y = DIRECTIONS.get(direction, (0, 0))
                new_x, new_y = self.x + direction_x, self.y + direction_y

                if self._is_neighbor(
                    (self.x, self.y), (new_x, new_y), maze.maze[self.y][self.x]
                ):
                    self.next_x, self.next_y = new_x, new_y
                    self.direction = direction
                    self.move_progress = 0.0
                    moved = True
                    break

            if not moved:
                self.pixel_x = float(self.x)
                self.pixel_y = float(self.y)
                self._update_skin()
                return

        self.move_progress = min(1.0, self.move_progress + self.speed)
        self.pixel_x = self.x + (self.next_x - self.x) * self.move_progress
        self.pixel_y = self.y + (self.next_y - self.y) * self.move_progress

        if (self.x, self.y) in self.pacgums:
            if self.pacgums[(self.x, self.y)].visible:
                self.pacgums[(self.x, self.y)].visible = False
                self.score += self.pacgums[(self.x, self.y)].points

        if (self.x, self.y) in self.super_pacgums:
            if self.super_pacgums[(self.x, self.y)].visible:
                self.super_pacgums[(self.x, self.y)].visible = False
                self.score += self.super_pacgums[(self.x, self.y)].points
                self.pacgum_effect = True
                self.timer_effect = 360

        self._update_skin()

    def _update_skin(self) -> None:
        """
        change the skin of the player to correspond to the direction
        and the frame
        """
        if self.direction:
            self.skin_timer += self.animation_speed
            if self.skin_timer >= 1:
                self.skin_timer = 0
                self.skin_index = (self.skin_index + 1) % 3
            self.skin = self.skin_dict[self.direction][self.skin_index]
