from mazegenerator.mazegenerator import MazeGenerator
from pacgum import Pacgum, SuperPacgum
from pygame import Surface, transform, image


class Player:
    """Player class"""

    def __init__(
        self,
        lives: int,
        maze_height: int,
        maze_width: int,
        maze: MazeGenerator,
        pacgums: dict[tuple[int, int], Pacgum],
        super_pacgums: dict[tuple[int, int], SuperPacgum],
        cell_height,
        cell_width
    ):
        self.maze = maze
        self.lives: int = lives
        self.x: int = maze_width // 2
        self.y: int = maze_height // 2
        self.spawn: tuple[int, int] = (self.x, self.y)
        self.next_x: int = maze_width // 2
        self.next_y: int = maze_height // 2
        self.pixel_x = float(maze_width // 2)
        self.pixel_y = float(maze_height // 2)
        self.move_progress: float = 1.0
        self.direction: str = ""
        self.queud_direction: str = ""
        self.skin: Surface | None = transform.scale(
            image.load("assets/skin/pacman.png"),
            (cell_width, cell_height),
        )
        self.skin_dict = {"N": [transform.scale(
                image.load(f"assets/skin/pacman-up/{i}.png"),
                (cell_width, cell_height)) for i in range(1, 4)],
                "S": [transform.scale(
                image.load(f"assets/skin/pacman-down/{i}.png"),
                (cell_width, cell_height)) for i in range(1, 4)],
                "W": [transform.scale(
                image.load(f"assets/skin/pacman-left/{i}.png"),
                (cell_width, cell_height)) for i in range(1, 4)],
                "E": [transform.scale(
                image.load(f"assets/skin/pacman-right/{i}.png"),
                (cell_width, cell_height)) for i in range(1, 4)]}
        self.score: int = 0
        self.speed: float = 0.10
        self.pacgums: dict[tuple[int, int], Pacgum] = pacgums
        self.super_pacgums: dict[tuple[int, int], SuperPacgum] = super_pacgums
        self.pacgum_effect: bool = False
        self.timer_effect = 0
        self.skin_timer = 0
        self.skin_index = 0
        self.animation_speed = 0.3

    def reset_param(self) -> None:
        """Reset the player parameters for a new game."""
        self.x, self.y = (
            self.next_x,
            self.next_y,
        ) = self.spawn
        self.direction = self.queud_direction = ""
        self.timer_effect = 0
        self.pacgum_effect = False

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

    def update_player(self):
        """update the player position, player movement pixel by pixel and player skin"""
        if self.timer_effect > 0:
            self.timer_effect -= 1
        if self.timer_effect == 0 and self.pacgum_effect is True:
            self.pacgum_effect = False
        if self.move_progress >= 1.0:
            self.x = self.next_x
            self.y = self.next_y
            direction_x, direction_y = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0),
            }.get(self.queud_direction, (0, 0))

            new_x, new_y = self.x + direction_x, self.y + direction_y
            if direction_x != 0 or direction_y != 0:
                if self._is_neighbor(
                    (self.x, self.y),
                    (new_x, new_y),
                    self.maze.maze[self.y][self.x],
                ):
                    self.next_x, self.next_y = new_x, new_y
                    self.direction = self.queud_direction
                    self.move_progress = 0.0

            direction_x, direction_y = {
                "N": (0, -1),
                "S": (0, 1),
                "E": (1, 0),
                "W": (-1, 0),
            }.get(self.direction, (0, 0))
            new_x, new_y = self.x + direction_x, self.y + direction_y
            if direction_x != 0 or direction_y != 0:
                if self._is_neighbor(
                    (self.x, self.y),
                    (new_x, new_y),
                    self.maze.maze[self.y][self.x],
                ):
                    self.next_x, self.next_y = new_x, new_y
                    self.move_progress = 0.0
                    return

        self.move_progress = min(1.0, self.move_progress + self.speed)
        self.pixel_x = self.x + (self.next_x - self.x) * self.move_progress
        self.pixel_y = self.y + (self.next_y - self.y) * self.move_progress
        if (self.x, self.y) in self.pacgums:
            if self.pacgums[self.x, self.y].visible:
                self.pacgums[self.x, self.y].visible = False
                self.score += self.pacgums[self.x, self.y].points
        if (self.x, self.y) in self.super_pacgums:
            if self.super_pacgums[self.x, self.y].visible:
                self.super_pacgums[self.x, self.y].visible = False
                self.score += self.super_pacgums[self.x, self.y].points
                self.pacgum_effect = True
                self.timer_effect = 360
        
        self.skin_timer += self.animation_speed
        if self.skin_timer >= 1:
            self.skin_timer = 0
            self.skin_index = (
                (self.skin_index + 1) % 3
            )  # car 3 images par pacman direction.
        if self.direction == "N":
            self.skin = self.skin_dict["N"][self.skin_index]
        if self.direction == "S":
            self.skin = self.skin_dict["S"][self.skin_index ]
        if self.direction == "W":
            self.skin = self.skin_dict["W"][self.skin_index]
        if self.direction == "E":
            self.skin = self.skin_dict["E"][self.skin_index]