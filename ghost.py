from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
from math import dist

from mazegenerator.mazegenerator import MazeGenerator
from pygame import Surface


class Player:
    def __init__(self, lives: int, maze_height: int, maze_width: int):
        self.lives: int = lives
        self.x: int = maze_width // 2
        self.y: int = maze_height // 2
        self.direction: str = ""
        self.skin: Surface | None = None
        self.score = 0
        self.speed = 1


class Ghost(ABC):
    def __init__(
        self,
        skin: str,
        spawn_x: int,
        spawn_y: int,
        maze: MazeGenerator,
        player: Player,
        is_frozen: bool = False,
    ):
        self.skin = skin
        self.x = spawn_x
        self.y = spawn_y
        self.alive = True
        self.spawn = (spawn_x, spawn_y)
        self.target: tuple[int] = self.spawn
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
        self.speed = 0.8
        self.maze = maze
        self.player = player
        self.direction = "UP"
        self.opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

    @abstractmethod
    def next_move(self):
        pass

    def play(self):
        move = self.next_move()
        self.x = move[0]
        self.y = move[1]

    def respawn(self):
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.alive = True

    def die(self):
        self.alive = False
        self.is_vulnerable = False
        self.respawn_timer = 10

    def get_moves_possible(self, maze: MazeGenerator, x, y):
        possible = []
        if x >= maze._width or y >= maze._height or x < 0 or y < 0:
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


class Blinky(Ghost):  # chases, dest player pos
    """Follows Pac-Man directly during Chase mode, and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is triggered when there are a
    certain number of dots left in the maze."""

    def __init__(self, skin, spawn_x, spawn_y, maze, player, is_frozen=False):
        super().__init__(skin, spawn_x, spawn_y, maze, player, is_frozen)

    def next_move(self) -> tuple[int, int]:
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.target = self.spawn
        else:
            self.target = (self.player.x, self.player.y)

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        print(self.x, self.y, self.target)
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
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.target = self.spawn
        else:
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
        print(self.x, self.y, self.target)
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
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if self.is_vulnerable:
            self.target = self.spawn
        else:
            self.target = (
                self.blinky.target[0] - self.pinky.target[0],
                self.blinky.target[1] - self.pinky.target[1],
            )

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        print(self.x, self.y, self.target)
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
        if self.is_frozen or not self.alive:
            return (self.x, self.y)

        if (
            self.is_vulnerable
            or dist((self.x, self.y), (self.player.x, self.player.y)) <= 3
        ):
            self.target = self.spawn
        else:
            self.target = (self.player.x, self.player.y)

        if (self.x, self.y) == self.target:
            return (self.x, self.y)
        print(self.x, self.y, self.target)
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
