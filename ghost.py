from abc import ABC, abstractmethod
from collections import deque
from math import dist

from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface

from pacgum import Pacgum, SuperPacgum


class Player:
    """Player class"""

    def __init__(
        self,
        skin_path: str,
        lives: int,
        maze_height: int,
        maze_width: int,
        maze: MazeGenerator,
        pacgums: dict[tuple[int, int], Pacgum],
        super_pacgums: dict[tuple[int, int], SuperPacgum],
    ):
        self.skin_path: str = skin_path
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
        self.skin: Surface | None = None
        self.score: int = 0
        self.speed: float = 0.10
        self.maze = maze
        self.pacgums: dict[tuple[int, int], Pacgum] = pacgums
        self.super_pacgums: dict[tuple[int, int], SuperPacgum] = super_pacgums
        self.pacgum_effect: bool = False
        self.timer_effect = 0

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
        """update the player position and player movement pixel by pixel"""
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


class Ghost(ABC):
    """abstract class for ghost"""

    def __init__(
        self,
        skin: str,
        spawn_x: int,
        spawn_y: int,
        maze: MazeGenerator,
        player: Player,
        is_frozen: bool = False,
    ):
        self.actual_skin = skin
        self.default_skin = skin
        self.vulnerable_skin = "./assets/skin/ghosts/blue_ghost.png"
        self.x = spawn_x
        self.y = spawn_y
        self.next_x = spawn_x
        self.next_y = spawn_y
        self.pixel_x = float(spawn_x)
        self.pixel_y = float(spawn_y)
        self.alive = True
        self.spawn = (spawn_x, spawn_y)
        self.target: tuple[int] = self.spawn
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
        self.speed = 0.05
        self.move_progress = 1.0
        self.maze = maze
        self.player = player
        self.direction = "UP"

    @abstractmethod
    def next_move(self):
        """Abstract method to get the next move of the ghost"""
        pass

    def play(self):
        """Move the ghost"""
        if self.move_progress >= 1.0:
            self.x = self.next_x
            self.y = self.next_y
            move = self.next_move()

            opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
            directions = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0),
            }

            # check si next move est un demi tour
            if move != (self.x, self.y):
                direction_x = move[0] - self.x
                direction_y = move[1] - self.y
                current_direction = next(
                    (
                        direction
                        for direction, (dx, dy) in directions.items()
                        if dx == direction_x and dy == direction_y
                    ),
                    None,
                )
                if current_direction and current_direction == opposite.get(
                    self.direction
                ):
                    moves = self.get_moves_possible(self.maze, self.x, self.y)
                    forward = [m for m in moves if m != opposite.get(self.direction)]
                    if forward:
                        move_chosen = forward[0]
                        direction_x, direction_y = directions[move_chosen]
                        move = (self.x + direction_x, self.y + direction_y)
                        self.direction = move_chosen

            # force un mouvement si pas de deplacement
            if move == (self.x, self.y):
                moves = self.get_moves_possible(self.maze, self.x, self.y)
                forward = [m for m in moves if m != opposite.get(self.direction)]
                # check si mouvement autre que demi tour possible
                if forward:
                    move_chosen = forward[0]
                    direction_x, direction_y = directions[move_chosen]
                    move = (self.x + direction_x, self.y + direction_y)
                    self.direction = move_chosen
                # si pas de mouvement autre que demi tour : demi tour
                elif moves:
                    move_chosen = moves[0]
                    direction_x, direction_y = directions[move_chosen]
                    move = (self.x + direction_x, self.y + direction_y)
                    self.direction = move_chosen

            self.next_x = move[0]
            self.next_y = move[1]
            self.move_progress = 0.0

        self.move_progress = min(1.0, self.move_progress + self.speed)
        self.pixel_x = self.x + (self.next_x - self.x) * self.move_progress
        self.pixel_y = self.y + (self.next_y - self.y) * self.move_progress

    def respawn(self):
        """Respawn the ghost when killed"""
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.alive = True

    def die(self):
        """Kill the ghost"""
        # self.alive = False
        self.reset_param()
        # self.respawn_timer = 10

    def get_moves_possible(self, maze: MazeGenerator, x, y):
        """get a list of possible moves"""
        possible = []
        if x >= len(maze.maze[0]) or y >= len(maze.maze) or x < 0 or y < 0:
            return []
        current_case_value = maze.maze[y][x]
        if not (current_case_value & 1):
            possible.append("UP")
        if not (current_case_value & 4):
            possible.append("DOWN")
        if not (current_case_value & 8):
            possible.append("LEFT")
        if not (current_case_value & 2):
            possible.append("RIGHT")

        return possible

    def reset_param(self) -> None:
        """Reset the Ghost parameters for a new game."""
        self.x, self.y = (
            self.next_x,
            self.next_y,
        ) = self.spawn
        self.actual_skin = self.default_skin
        self.is_vulnerable = False

    def player_boosted(self) -> bool:
        """check if the player is boosted with super pacgums"""
        return self.player.pacgum_effect


class Blinky(Ghost):  # chases, dest player pos
    """Follows Pac-Man directly during Chase mode, and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is triggered when there are a
    certain number of dots left in the maze."""

    def __init__(self, skin, spawn_x, spawn_y, maze, player, is_frozen=False):
        super().__init__(skin, spawn_x, spawn_y, maze, player, is_frozen)

    def next_move(self) -> tuple[int, int]:
        if self.player_boosted():
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False
        if self.is_frozen:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.target = self.spawn
            self.actual_skin = self.vulnerable_skin
        else:
            self.actual_skin = self.default_skin
            self.target = (self.player.x, self.player.y)

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        queue = deque()
        visited = {(self.x, self.y)}

        moves = self.get_moves_possible(self.maze, self.x, self.y)

        for move in moves:
            new_x, new_y = self.x, self.y
            if move == "UP":
                new_y -= 1
            elif move == "DOWN":
                new_y += 1
            elif move == "LEFT":
                new_x -= 1
            elif move == "RIGHT":
                new_x += 1

            if (new_x, new_y) not in visited:
                queue.append((new_x, new_y, move, (new_x, new_y)))
                visited.add((new_x, new_y))

        while queue:
            current_x, current_y, move_name, first_step = queue.popleft()
            if (current_x, current_y) == self.target:
                self.direction = move_name
                return first_step

            for move in self.get_moves_possible(self.maze, current_x, current_y):
                new_x, new_y = current_x, current_y
                if move == "UP":
                    new_y -= 1
                elif move == "DOWN":
                    new_y += 1
                elif move == "LEFT":
                    new_x -= 1
                elif move == "RIGHT":
                    new_x += 1

                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, move_name, first_step))

        return (self.x, self.y)


class Pinky(Ghost):  # ambushes, dest 2 case devant le player
    """Chases towards the spot 2 Pac-Dots in front of Pac-Man. Due to a bug in the original
    game's coding, if Pac-Man faces upwards, Pinky's target will be 2 Pac-Dots in front of and 2
    to the left of Pac-Man. During Scatter mode, she heads towards the upper-left corner."""

    def __init__(self, skin, spawn_x, spawn_y, maze, player, is_frozen=False):
        super().__init__(skin, spawn_x, spawn_y, maze, player, is_frozen)

    def next_move(self) -> tuple[int, int]:
        if self.player_boosted():
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.actual_skin = self.vulnerable_skin
        else:
            self.actual_skin = self.default_skin
            if self.player.direction == "UP" and self.player.y - 2 >= 0:
                self.target = (self.player.x, self.player.y - 2)
            elif (
                self.player.direction == "DOWN"
                and self.player.y + 2 <= self.maze._height - 1
            ):
                self.target = (self.player.x, self.player.y + 2)
            elif (
                self.player.direction == "RIGHT"
                and self.player.x + 2 <= self.maze._width - 1
            ):
                self.target = (self.player.x + 2, self.player.y)
            elif self.player.direction == "LEFT" and self.player.x - 2 >= 0:
                self.target = (self.player.x - 2, self.player.y)
            else:
                self.target = (self.player.x, self.player.y)

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        queue = deque()
        visited = {(self.x, self.y)}

        moves = self.get_moves_possible(self.maze, self.x, self.y)

        for move in moves:
            new_x, new_y = self.x, self.y
            if move == "UP":
                new_y -= 1
            elif move == "DOWN":
                new_y += 1
            elif move == "LEFT":
                new_x -= 1
            elif move == "RIGHT":
                new_x += 1

            if (new_x, new_y) not in visited:
                queue.append((new_x, new_y, move, (new_x, new_y)))
                visited.add((new_x, new_y))

        while queue:
            current_x, current_y, move_name, first_step = queue.popleft()
            if (current_x, current_y) == self.target:
                self.direction = move_name
                return first_step

            for move in self.get_moves_possible(self.maze, current_x, current_y):
                new_x, new_y = current_x, current_y
                if move == "UP":
                    new_y -= 1
                elif move == "DOWN":
                    new_y += 1
                elif move == "LEFT":
                    new_x -= 1
                elif move == "RIGHT":
                    new_x += 1

                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, move_name, first_step))

        return (self.x, self.y)


class Inky(Ghost):  # unpredictable, dest = distance entre blinky et pinky target * 2
    """During Chase mode, his target is a bit complex. His target is relative to both
    Blinky and Pac-Man, where the distance Blinky is from Pinky's target is doubled to
    get Inky's target. He heads to the lower-right corner during Scatter mode."""

    def __init__(
        self, skin, spawn_x, spawn_y, maze, player, blinky, pinky, is_frozen=False
    ):
        super().__init__(skin, spawn_x, spawn_y, maze, player, is_frozen)
        self.blinky = blinky
        self.pinky = pinky

    def next_move(self) -> tuple[int, int]:
        if self.player_boosted():
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.actual_skin = self.vulnerable_skin
        else:
            self.actual_skin = self.default_skin
            self.target = (
                self.blinky.target[0] - self.pinky.target[0],
                self.blinky.target[1] - self.pinky.target[1],
            )

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        queue = deque()
        visited = {(self.x, self.y)}

        moves = self.get_moves_possible(self.maze, self.x, self.y)

        for move in moves:
            new_x, new_y = self.x, self.y
            if move == "UP":
                new_y -= 1
            elif move == "DOWN":
                new_y += 1
            elif move == "LEFT":
                new_x -= 1
            elif move == "RIGHT":
                new_x += 1

            if (new_x, new_y) not in visited:
                queue.append((new_x, new_y, move, (new_x, new_y)))
                visited.add((new_x, new_y))

        while queue:
            current_x, current_y, move_name, first_step = queue.popleft()
            if (current_x, current_y) == self.target:
                self.direction = move_name
                return first_step

            for move in self.get_moves_possible(self.maze, current_x, current_y):
                new_x, new_y = current_x, current_y
                if move == "UP":
                    new_y -= 1
                elif move == "DOWN":
                    new_y += 1
                elif move == "LEFT":
                    new_x -= 1
                elif move == "RIGHT":
                    new_x += 1

                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, move_name, first_step))

        return (self.x, self.y)


class Clyde(Ghost):  # weird
    """Chases directly after Pac-Man, but tries to head to his Scatter corner when within
    an 8-Dot radius of Pac-Man. His Scatter Mode corner is the lower-left."""

    def __init__(self, skin, spawn_x, spawn_y, maze, player, is_frozen=False):
        super().__init__(skin, spawn_x, spawn_y, maze, player, is_frozen)

    def next_move(self) -> tuple[int, int]:
        if self.player_boosted():
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if (
            self.is_vulnerable
            or dist((self.x, self.y), (self.player.x, self.player.y)) <= 3
        ):
            self.target = self.spawn
            if self.is_vulnerable:
                self.actual_skin = self.vulnerable_skin
        else:
            self.actual_skin = self.default_skin
            self.target = (self.player.x, self.player.y)

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        queue = deque()
        visited = {(self.x, self.y)}

        moves = self.get_moves_possible(self.maze, self.x, self.y)

        for move in moves:
            new_x, new_y = self.x, self.y
            if move == "UP":
                new_y -= 1
            elif move == "DOWN":
                new_y += 1
            elif move == "LEFT":
                new_x -= 1
            elif move == "RIGHT":
                new_x += 1

            if (new_x, new_y) not in visited:
                queue.append((new_x, new_y, move, (new_x, new_y)))
                visited.add((new_x, new_y))

        while queue:
            current_x, current_y, move_name, first_step = queue.popleft()
            if (current_x, current_y) == self.target:
                self.direction = move_name
                return first_step

            for move in self.get_moves_possible(self.maze, current_x, current_y):
                new_x, new_y = current_x, current_y
                if move == "UP":
                    new_y -= 1
                elif move == "DOWN":
                    new_y += 1
                elif move == "LEFT":
                    new_x -= 1
                elif move == "RIGHT":
                    new_x += 1

                if (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, move_name, first_step))

        return (self.x, self.y)


# PlayerTest = Player(3, 10, 10)
# BlinkyTest = Blinky("red", 0, 0)
# maze = MazeGenerator()
# print(BlinkyTest.next_move(PlayerTest, maze))
# PinkyTest = Pinky("pink", 14, 14)
# print(PinkyTest.next_move(PlayerTest, maze))
# InkyTest = Inky("blue", 5, 5)
# print(InkyTest.next_move(PlayerTest, maze, BlinkyTest, PinkyTest))
# ClydeTest = Clyde("green", 0, 0)
# print(ClydeTest.next_move(PlayerTest, maze))
