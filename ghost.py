from enum import Enum
from abc import ABC, abstractmethod


class Ghost(ABC):
    def __init__(self, color: str, spawn_x: int, spawn_y: int, is_frozen = False):
        self.color = color
        self.x = spawn_x
        self.y = spawn_y
        self.alive = True
        self.spawn = (spawn_x, spawn_y)
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
    
    @abstractmethod
    def next_move(player_pos: tuple[int]): 
        pass

    def respawn(self):
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.alive = True

    def die(self):
        self.alive = False
        self.is_vulnerable = False
        self.respawn_timer = 10

    def get_moves_possible(self, maze):
        possible = []
        current_case_value = maze.maze[self.y][self.x]

        if not (current_case_value & 1):
            possible.append("UP")
        if not (current_case_value & 4):
            possible.append("DOWN")
        if not (current_case_value & 8):
            possible.append("LEFT")
        if not (current_case_value & 2):
            possible.append("RIGHT")
        
        return possible


class Blinky(Ghost): # chases
    def next_move(player_pos):
        pass


class Pinky(Ghost): # ambushes
    def next_move(player_pos):
        pass


class Inky(Ghost): # unpredictable
    def next_move(player_pos):
        pass


class Clyde(Ghost): # weird
    def next_move(player_pos):
        pass
