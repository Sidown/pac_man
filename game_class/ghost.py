from abc import ABC, abstractmethod
from collections import deque
from math import dist
from typing import Optional

from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface, image, transform

from .cheat import Cheat
from .player import Player


class Ghost(ABC):
    """
    Abstract class for all the ghosts.
    Manage movement, vulnerability, collision and skin.
    """

    def __init__(
        self,
        skin: str,
        cell_width: float,
        cell_height: float,
    ) -> None:
        """
        Initialise a Ghost with its sprite and default state.
        Arguments:
        skin -> path to the ghost default sprite
        cell_width -> Width of a maze cell in pixels
        cell_height -> Height of a maze cell in pixels
        """
        self.actual_skin: Surface = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.default_skin: Surface = transform.scale(
            image.load(skin),
            (cell_width, cell_height),
        )
        self.vulnerable_skin: Surface = transform.scale(
            image.load("./assets/skin/ghosts/blue_ghost.png"),
            (cell_width, cell_height),
        )
        self.return_spawn_skin: Surface = transform.scale(
            image.load("./assets/skin/ghosts/eyes.png"),
            (cell_width, cell_height),
        )
        self.coord: tuple[int, int] = (0, 0)
        self.next_coord: tuple[int, int] = (0, 0)
        self.pixel_coord: tuple[float, float] = (0, 0)
        self.died: bool = False
        self.spawn: tuple[int, int] = (0, 0)
        self.target: tuple[int, int] = self.spawn
        self.is_vulnerable: bool = False
        self.respawn_timer: int = 0
        self.speed: float = 0.05
        self.move_progress: float = 1.0
        self.direction: str = "UP"
        self.just_respawned: bool = False

    @abstractmethod
    def next_move(
        self, maze: MazeGenerator, player: Player, cheat: Cheat
    ) -> tuple[int, int]:
        """
        Return the next cell the ghost should move to.
        Arguments:
        maze -> The current maze
        player -> The player
        cheat -> the cheat class

        return value:
        (x, y) coordinate of next cell
        """
        pass

    def play(self, maze: MazeGenerator, player: Player, cheat: Cheat) -> None:
        """
        Move the ghost pixel by pixel.
        arguments:
        maze -> the current maze
        player -> the player
        cheat -> the cheat class
        """
        if self.move_progress >= 1.0:
            self.coord = self.next_coord
            self._update_vulnerability(player)
            if not cheat.freeze:
                move = self.next_move(maze, player, cheat)

                opposite = {
                    "UP": "DOWN",
                    "DOWN": "UP",
                    "LEFT": "RIGHT",
                    "RIGHT": "LEFT",
                }
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
                        forward = [
                            m for m in moves
                            if m != opposite.get(self.direction)
                        ]
                        if forward:
                            move_chosen = forward[0]
                            direction_x, direction_y = directions[move_chosen]
                            move = (
                                self.coord[0] + direction_x,
                                self.coord[1] + direction_y,
                            )
                            self.direction = move_chosen

                # force un mouvement si pas de deplacement
                if move == self.coord:
                    moves = self.get_moves_possible(maze, self.coord)
                    forward = [m for m in moves
                               if m != opposite.get(self.direction)]
                    # check si mouvement autre que demi tour possible
                    if forward:
                        move_chosen = forward[0]
                        direction_x, direction_y = directions[move_chosen]
                        move = (
                            self.coord[0] + direction_x,
                            self.coord[1] + direction_y,
                        )
                        self.direction = move_chosen
                    # si pas de mouvement autre que demi tour : demi tour
                    elif moves:
                        move_chosen = moves[0]
                        direction_x, direction_y = directions[move_chosen]
                        move = (
                            self.coord[0] + direction_x,
                            self.coord[1] + direction_y,
                        )
                        self.direction = move_chosen

                self.next_coord = (move[0], move[1])
                self.move_progress = 0.0

        self.move_progress = min(1.0, self.move_progress + self.speed)
        self.pixel_coord = (
            (self.coord[0] + (
                self.next_coord[0]
                - self.coord[0])
                * self.move_progress),
            (self.coord[1] + (
                self.next_coord[1]
                - self.coord[1])
                * self.move_progress),
        )

    def respawn(self) -> None:
        """
        Change the coordinate of the ghost when killed
        to his spawn point.
        """
        self.coord = self.spawn

    def die(self) -> None:
        """
        Mark the ghost as dead and send it to it's spawn point.
        """
        self.died = True
        self.target = self.spawn
        self.speed = 0.2
        self.is_vulnerable = False

    def get_moves_possible(
        self, maze: MazeGenerator, coord: tuple[int, int]
    ) -> list[str]:
        """
        Return the list of valid moves directeions from coord
        arguments:
        maze -> the current maze
        coord -> the coordinate x, y of the cell to check
        return value:
        A list of direction strings "UP", "DOWN", "RIGHT", "LEFT"
        """
        possible = []
        if (
            coord[0] >= len(maze.maze[0])
            or coord[1] >= len(maze.maze)
            or coord[0] < 0
            or coord[1] < 0
        ):
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

    def player_boosted(self, player: Player) -> bool:
        """
        Check if the player is boosted with super pacgums.
        arguments:
        player -> The player
        """
        return player.pacgum_effect

    def collide_with_player(self, player: Player) -> bool:
        """
        Check if the ghost overlap the player position.
        arguments:
        player -> the player
        """
        if (
            abs(player.pixel_x - self.pixel_coord[0]) < 0.6
            and abs(player.pixel_y - self.pixel_coord[1]) < 0.6
        ):
            return True
        return False

    @property
    def current_skin(self) -> Surface:
        """
        Return the correct skin for the ghost depending of the
        current game state.
        """
        if self.died:
            return self.return_spawn_skin
        if self.is_vulnerable:
            self.speed = 0.03
            return self.vulnerable_skin
        self.speed = 0.05
        return self.default_skin

    def _update_vulnerability(self, player: Player) -> None:
        """
        Update the ghost vulnerability.
        Arguments:
        player -> the player
        """
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


class Blinky(Ghost):  # chases, dest player pos
    """
    Follows Pac-Man directly during Chase mode,
    and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is
    triggered when there are a
    certain number of dots left in the maze, wich increases his
    speed and change his skin.
    """

    def __init__(self, skin: str, cell_width: float,
                 cell_height: float) -> None:
        """
        Initialise Blinky and load his angry skin.
        Arguments:
        skin -> path to the skin file
        cell_width -> width of the maze cell in pixel
        cell_height -> height of the maze cell in pixel
        """
        super().__init__(skin, cell_width, cell_height)
        self.angry_skin: Surface = transform.scale(
            image.load("assets/skin/ghosts/angry_blinky.png"),
            (cell_width, cell_height),
        )

    def set_parameters(self, maze: MazeGenerator, player: Player) -> None:
        """
        Set Blinky spawn position in the maze.
        Arguments:
        maze -> The current maze
        player -> The player
        """
        self.spawn = (len(maze.maze[0]) - 1, 0)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))

    @property
    def angry_mod(self) -> None:
        """
        Activate angry mode: increace speed and change the skin
        """
        self.speed = 0.08
        self.default_skin = self.angry_skin

    def next_move(
        self, maze: MazeGenerator, player: Player, cheat: Cheat
    ) -> tuple[int, int]:
        """
        Return the next cell using BFS with player as the target
        or the spawn if vulnerable.
        Arguments:
        maze -> the current maze
        player -> the player
        cheat -> the cheat class
        return value:
        x,y coordinates of the next cell to move to
        """
        if cheat.freeze:
            return self.coord

        if self.is_vulnerable or self.died:
            self.target = self.spawn
        else:
            self.target = (player.x, player.y)

        if self.coord == self.target:
            return self.coord
        queue: deque[tuple[int, int, str, tuple[int, int]]] = deque()
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

    def __init__(self, skin: str, cell_width: float,
                 cell_height: float) -> None:
        """
        Initialise Pinky.

        Arguments:
        skin -> path to the skin file
        cell_width -> width of the maze cell in pixels
        cell_height -> height of the maze cell in pixels
        """
        super().__init__(skin, cell_width, cell_height)

    def set_parameters(self, player: Player) -> None:
        """
        Set Pinky spawn.

        Arguments:
        player -> the player
        """
        self.spawn = (0, 0)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))

    def next_move(
        self, maze: MazeGenerator, player: Player, cheat: Cheat
    ) -> tuple[int, int]:
        """
        Return the next cell using BFS with a point
        ahead of the player as the target
        or the spawn if vulnerable.
        Arguments:
        maze -> the current maze
        player -> the player
        cheat -> the cheat class
        return value:
        x,y coordinates of the next cell to move to
        """
        if cheat.freeze:
            return self.coord

        if self.is_vulnerable or self.died:
            self.target = self.spawn
        else:
            if player.direction == "UP" and player.y - 2 >= 0:
                self.target = (player.x, player.y - 2)

            elif (player.direction == "DOWN"
                  and player.y + 2 <= maze._height - 1):
                self.target = (player.x, player.y + 2)

            elif (player.direction == "RIGHT"
                  and player.x + 2 <= maze._width - 1):
                self.target = (player.x + 2, player.y)

            elif player.direction == "LEFT" and player.x - 2 >= 0:
                self.target = (player.x - 2, player.y)

            else:
                self.target = (player.x, player.y)

        if self.coord == self.target:
            return self.coord
        queue: deque[tuple[int, int, str, tuple[int, int]]] = deque()
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


class Inky(Ghost):
    """During Chase mode, his target is a bit complex.
    His target is relative to both Blinky and Pac-Man, where the distance
    Blinky is from Pinky's target is doubled to get Inky's target.
    He heads to the lower-right corner during Scatter mode."""

    def __init__(self, skin: str, cell_width: float,
                 cell_height: float) -> None:
        """
        Initialise Inky.

        Arguments:
        skin -> Path to the skin file
        cell_width -> Width of the maze cell in pixels
        cell_height -> Height of the maze cell in pixels
        """
        super().__init__(skin, cell_width, cell_height)

    def play(
        self,
        maze: MazeGenerator,
        player: Player,
        cheat: Cheat,
        blinky: Optional[Blinky] = None,
        pinky: Optional[Pinky] = None,
    ) -> None:
        """
        Override play to update internal blinky/pinky references.

        Arguments:
            maze -> The current maze
            player -> The player
            cheat -> The cheat class
            blinky -> Blinky
            pinky -> Pinky
        """
        if blinky:
            self._blinky = blinky
        if pinky:
            self._pinky = pinky
        super().play(maze, player, cheat)

    def set_parameters(
        self, maze: MazeGenerator, player: Player, blinky: Blinky, pinky: Pinky
    ) -> None:
        """
        Set Inky spawn.
        Arguments:
        maze -> the current maze
        player -> the player
        blinky -> Blinky
        pinky -> Pinky
        """
        self.spawn = (len(maze.maze[0]) - 1, len(maze.maze) - 1)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))
        self._blinky = blinky
        self._pinky = pinky

    def next_move(
        self, maze: MazeGenerator, player: Player, cheat: Cheat
    ) -> tuple[int, int]:
        """
        Return the next cell using BFS toward Inky target.

        Arguments:
        maze -> the current maze
        player -> the player
        cheat -> the cheat class
        return value:
        x,y coord of the next cell to move to
        """
        if cheat.freeze:
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
        queue: deque[tuple[int, int, str, tuple[int, int]]] = deque()
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


class Clyde(Ghost):  # weird
    """Chases directly after Pac-Man, but tries to
    head to his Scatter corner when within
    an 8-Dot radius of Pac-Man.
    His Scatter Mode corner is the lower-left."""

    def __init__(self, skin: str, cell_width: float,
                 cell_height: float) -> None:
        """
        Initialise Clyde.
        Arguments:
        skin -> path to the skin file
        cell_width -> width of the maze cell in pixels
        cell_height -> height of the maze cell in pixels
        """
        super().__init__(skin, cell_width, cell_height)

    def set_parameters(self, maze: MazeGenerator, player: Player) -> None:
        """
        Set clyde spawn.
        Arguments;
        maze -> the current maze
        player -> the player
        """
        self.spawn = (0, len(maze.maze) - 1)
        self.coord = self.spawn
        self.next_coord = self.spawn
        self.target = (player.x, player.y)
        self.pixel_coord = (float(self.spawn[0]), float(self.spawn[1]))

    def next_move(
        self, maze: MazeGenerator, player: Player, cheat: Cheat
    ) -> tuple[int, int]:
        """
        Return the next cell, chase the player unless within 3 cells or
        vulnerable.
        Arguments:
        maze -> the current maze
        player -> the player
        cheat -> the cheat class
        return value:
        x,y coord of the next cell to move to
        """
        if cheat.freeze:
            return self.coord

        if (
            self.is_vulnerable
            or self.died
            or dist(self.coord, (player.x, player.y)) <= 3
        ):
            self.target = self.spawn
        else:
            self.target = (player.x, player.y)

        if self.coord == self.target:
            return self.coord
        queue: deque[tuple[int, int, str, tuple[int, int]]] = deque()
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
