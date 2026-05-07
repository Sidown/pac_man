from enum import Enum
from abc import ABC, abstractmethod
from mazegenerator.mazegenerator import MazeGenerator


class Ghost(ABC):
    def __init__(self, color: str, spawn_x: int, spawn_y: int, is_frozen: bool = False):
        self.color = color
        self.x = spawn_x
        self.y = spawn_y
        self.alive = True
        self.spawn = (spawn_x, spawn_y)
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
    
    @abstractmethod
    def next_move(self, player_pos: tuple[int], maze: MazeGenerator): 
        pass

    def respawn(self):
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.alive = True

    def die(self):
        self.alive = False
        self.is_vulnerable = False
        self.respawn_timer = 10

    def get_moves_possible(self, maze: MazeGenerator):
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


class Blinky(Ghost): # chases a* algo, dest player pos
    """Follows Pac-Man directly during Chase mode, and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is triggered when there are a
    certain number of dots left in the maze."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(self, player_pos: tuple[int], maze: MazeGenerator):
        if not self.is_frozen and self.alive and not self.is_vulnerable:
            player_x = player_pos[0]
            player_y = player_pos[1]
            queue = {}
            


        


class Pinky(Ghost): # ambushes a* algo, dest 2 case devant le player
    """Chases towards the spot 2 Pac-Dots in front of Pac-Man. Due to a bug in the original
    game's coding, if Pac-Man faces upwards, Pinky's target will be 2 Pac-Dots in front of and 2
    to the left of Pac-Man. During Scatter mode, she heads towards the upper-left corner."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(player_pos: tuple[int], maze):
        pass


class Inky(Ghost): # unpredictable a* algo, dest = distance entre blinky et pinky target * 2
    """During Chase mode, his target is a bit complex. His target is relative to both
    Blinky and Pac-Man, where the distance Blinky is from Pinky's target is doubled to
    get Inky's target. He heads to the lower-right corner during Scatter mode."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(player_pos: tuple[int], maze):
        pass


class Clyde(Ghost): # weird 
    """Chases directly after Pac-Man, but tries to head to his Scatter corner when within
    an 8-Dot radius of Pac-Man. His Scatter Mode corner is the lower-left."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(player_pos: tuple[int], maze):
        pass
