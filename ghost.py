from abc import ABC, abstractmethod
from collections import deque
from math import dist

from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface, transform, image

from player import Player


class Ghost(ABC):
    """abstract class for ghost"""

    def __init__(
        self,
        skin: str,
        # spawn_x: int,
        # spawn_y: int,
        # maze: MazeGenerator,
        # player: Player,
        cell_width,
        cell_height,
        is_frozen: bool = False,
    ):
        self.actual_skin = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.default_skin = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.vulnerable_skin = transform.scale(
            image.load("./assets/skin/ghosts/blue_ghost.png"),
            (cell_width, cell_height),
        )
        self.return_spawn_skin = transform.scale(
            image.load("./assets/skin/ghosts/eyes.png"),
            (cell_width, cell_height),
        )
        self.coord: tuple[int] = (0, 0)
        self.next_coord: tuple[int] = (0, 0)
        self.pixel_coord: tuple[float] = (0, 0)
        self.died: bool = False
        self.spawn: tuple[int] = (0, 0)
        self.target: tuple[int] = self.spawn
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
        self.speed = 0.05
        self.move_progress = 1.0
        self.direction = "UP"
        self.just_respawned = False

    @abstractmethod
    def next_move(self):
        """Abstract method to get the next move of the ghost"""
        pass

    def play(self, maze: MazeGenerator, player):
        """Move the ghost"""
        if self.move_progress >= 1.0:
            self.coord = self.next_coord
            self._update_vulnerability(player)
            move = self.next_move(maze, player)

            opposite = {"UP": "DOWN", "DOWN": "UP",
                        "LEFT": "RIGHT", "RIGHT": "LEFT"}
            directions = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0),
            }

            # check si next move est un demi tour
            if move != self.coord:
                direction_x = move[0] - self.coord[0]
                direction_y = move[1] - self.coord[1]
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
                    moves = self.get_moves_possible(maze, self.coord)
                    forward = [m for m in moves if
                               m != opposite.get(self.direction)]
                    if forward:
                        move_chosen = forward[0]
                        direction_x, direction_y = directions[move_chosen]
                        move = (self.coord[0] + direction_x,
                                self.coord[1] + direction_y)
                        self.direction = move_chosen

            # force un mouvement si pas de deplacement
            if move == self.coord:
                moves = self.get_moves_possible(maze, self.coord)
                forward = [m for m in moves if
                           m != opposite.get(self.direction)]
                # check si mouvement autre que demi tour possible
                if forward:
                    move_chosen = forward[0]
                    direction_x, direction_y = directions[move_chosen]
                    move = (self.coord[0] + direction_x,
                            self.coord[1] + direction_y)
                    self.direction = move_chosen
                # si pas de mouvement autre que demi tour : demi tour
                elif moves:
                    move_chosen = moves[0]
                    direction_x, direction_y = directions[move_chosen]
                    move = (self.coord[0] + direction_x,
                            self.coord[1] + direction_y)
                    self.direction = move_chosen

            self.next_coord = (move[0], move[1])
            self.move_progress = 0.0

        self.move_progress = min(1.0, self.move_progress + self.speed)
        self.pixel_coord = (self.coord[0] + (self.next_coord[0] -
                                             self.coord[0]) *
                                             self.move_progress,
                            self.coord[1] + (self.next_coord[1] -
                                             self.coord[1]) *
                                             self.move_progress)

    def respawn(self):
        """Respawn the ghost when killed"""
        self.coord = self.spawn

    def die(self):
        """Kill the ghost"""
        self.died = True
        self.target = self.spawn
        self.speed = 0.2
        self.is_vulnerable = False

    def get_moves_possible(self, maze: MazeGenerator, coord: tuple[int]):
        """get a list of possible moves"""
        possible = []
        if (coord[0] >= len(maze.maze[0]) or coord[1] >= len(maze.maze)
           or coord[0] < 0 or coord[1] < 0):
            return []
        current_case_value = maze.maze[coord[1]][coord[0]]
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
        self.coord = self.next_coord = self.spawn
        self.actual_skin = self.default_skin
        self.is_vulnerable = False
        self.died = False
        self.just_respawned = False

    def player_boosted(self, player) -> bool:
        """check if the player is boosted with super pacgums"""
        return player.pacgum_effect

    def collide_with_player(self, player) -> bool:
        """check if the ghost collide with the player"""
        if (
                abs(player.pixel_x - self.pixel_coord[0]) < 0.6
                and abs(player.pixel_y - self.pixel_coord[1]) < 0.6
           ):
            return True
        return False

    @property
    def current_skin(self):
        if self.died:
            return self.return_spawn_skin
        if self.is_vulnerable:
            self.speed = 0.03
            return self.vulnerable_skin
        self.speed = 0.05
        return self.default_skin

    def _update_vulnerability(self, player):
        if self.died:
            self.is_vulnerable = False
            if self.coord == self.spawn:
                self.died = False
                self.speed = 0.05
                self.just_respawned = True
        elif self.just_respawned:
            if not self.player_boosted(player):
                self.just_respawned = False
            self.is_vulnerable = False
        elif self.player_boosted(player):
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False

    @abstractmethod
    def set_parameters(self):
        pass


class Blinky(Ghost):  # chases, dest player pos
    """Follows Pac-Man directly during Chase mode,
    and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is
    triggered when there are a
    certain number of dots left in the maze."""

    def __init__(self, skin, cell_width, cell_height, is_frozen=False):
        super().__init__(skin, cell_width, cell_height, is_frozen)
        self.angry_skin = transform.scale(
            image.load("assets/skin/ghosts/angry_blinky.jpg"),
            (cell_width, cell_height),
        )

    def set_parameters(self, maze, player):
        self.spawn = (len(maze.maze[0]) - 1, 0)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))

    @property
    def angry_mod(self):
        self.speed = 0.08
        self.default_skin = self.angry_skin

    def next_move(self, maze, player) -> tuple[int, int]:
        if self.is_frozen:
            return self.coord

        if self.is_vulnerable or self.died:
            self.target = self.spawn
        else:
            self.target = (player.x, player.y)

        if self.coord == self.target:
            return self.coord
        queue = deque()
        visited = {self.coord}

        moves = self.get_moves_possible(maze, self.coord)

        for move in moves:
            new_x, new_y = self.coord
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

            for move in self.get_moves_possible(maze, (current_x, current_y)):
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

        return self.coord


class Pinky(Ghost):  # ambushes, dest 2 case devant le player
    """Chases towards the spot 2 Pac-Dots in front of Pac-Man.
    Due to a bug in the original game's coding, if Pac-Man faces upwards,
    Pinky's target will be 2 Pac-Dots in front of and 2
    to the left of Pac-Man. During Scatter mode,
    she heads towards the upper-left corner."""

    def __init__(self, skin, cell_width, cell_height, is_frozen=False):
        super().__init__(skin, cell_width, cell_height, is_frozen)

    def set_parameters(self, player):
        self.spawn = (0, 0)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))
        
    def next_move(self, maze, player) -> tuple[int, int]:
        if self.is_frozen:
            return self.coord

        if self.is_vulnerable or self.died:
            self.target = self.spawn
        else:
            if player.direction == "UP" and player.y - 2 >= 0:
                self.target = (player.x, player.y - 2)
            elif (
                player.direction == "DOWN"
                and player.y + 2 <= maze._height - 1
            ):
                self.target = (player.x, player.y + 2)
            elif (
                player.direction == "RIGHT"
                and player.x + 2 <= maze._width - 1
            ):
                self.target = (player.x + 2, player.y)
            elif player.direction == "LEFT" and player.x - 2 >= 0:
                self.target = (player.x - 2, player.y)
            else:
                self.target = (player.x, player.y)

        if self.coord == self.target:
            return self.coord
        queue = deque()
        visited = {self.coord}

        moves = self.get_moves_possible(maze, self.coord)

        for move in moves:
            new_x, new_y = self.coord
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

            for move in self.get_moves_possible(maze,
                                                (current_x,
                                                 current_y)):
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

        return self.coord


class Inky(Ghost): 
    """During Chase mode, his target is a bit complex.
    His target is relative to both Blinky and Pac-Man, where the distance
    Blinky is from Pinky's target is doubled to get Inky's target.
    He heads to the lower-right corner during Scatter mode."""

    def __init__(self, skin, cell_width, cell_height, is_frozen=False):
        super().__init__(skin, cell_width, cell_height, is_frozen)

    def play(self, maze, player, blinky=None, pinky=None):
        if blinky:
            self._blinky = blinky
        if pinky:
            self._pinky = pinky
        super().play(maze, player)

    def set_parameters(self, maze, player, blinky, pinky):
        self.spawn = (len(maze.maze[0]) - 1, len(maze.maze) - 1)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))
        self._blinky = blinky
        self._pinky = pinky

    def next_move(self, maze, player) -> tuple[int, int]:
        if self.is_frozen:
            return self.coord

        if self.is_vulnerable or self.died:
            self.target = self.spawn
        elif dist(self.coord, (player.x, player.y)) <= 3:
            self.target = (player.x, player.y)
        else:
            self.target = (
                self._blinky.target[0] - self._pinky.target[0],
                self._blinky.target[1] - self._pinky.target[1],
            )

        if self.coord == self.target:
            return self.coord
        queue = deque()
        visited = {self.coord}

        moves = self.get_moves_possible(maze, self.coord)

        for move in moves:
            new_x, new_y = self.coord
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

            for move in self.get_moves_possible(maze, (current_x,
                                                current_y)):
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

        return self.coord


class Clyde(Ghost):  # weird
    """Chases directly after Pac-Man, but tries to
    head to his Scatter corner when within
    an 8-Dot radius of Pac-Man.
    His Scatter Mode corner is the lower-left."""

    def __init__(self, skin, cell_width, cell_height, is_frozen=False):
        super().__init__(skin, cell_width, cell_height, is_frozen)

    def set_parameters(self, maze, player):
        self.spawn = (0, len(maze.maze) - 1)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))

    def next_move(self, maze, player) -> tuple[int, int]:
        if self.is_frozen:
            return self.coord

        if (
            self.is_vulnerable or self.died
            or dist(self.coord, (player.x, player.y)) <= 3
        ):
            self.target = self.spawn
        else:
            self.target = (player.x, player.y)
        
        if self.coord == self.target:
            return self.coord
        queue = deque()
        visited = {self.coord}

        moves = self.get_moves_possible(maze, self.coord)

        for move in moves:
            new_x, new_y = self.coord
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

            for move in self.get_moves_possible(maze, (current_x,
                                                current_y)):
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

        return self.coord


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
