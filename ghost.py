from enum import Enum
from abc import ABC, abstractmethod
from mazegenerator.mazegenerator import MazeGenerator


class Player:
    def __init__(self, lives: int, maze_height: int, maze_width: int):
        self.lives: int = lives
        self.x: int = maze_width // 2
        self.y: int = maze_height // 2
        self.direction: str = None


class Ghost(ABC):
    def __init__(self, color: str, spawn_x: int, spawn_y: int, is_frozen: bool = False):
        self.color = color
        self.x = spawn_x
        self.y = spawn_y
        self.alive = True
        self.spawn = (spawn_x, spawn_y)
        self.target: tuple[int] = self.spawn
        self.is_vulnerable = False
        self.is_frozen = is_frozen
        self.respawn_timer = 0
    
    @abstractmethod
    def next_move(self, player: Player, maze: MazeGenerator): 
        pass

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


class Blinky(Ghost): # chases, dest player pos
    """Follows Pac-Man directly during Chase mode, and heads to the upper-right corner
    during Scatter mode. He also has an "angry" mode that is triggered when there are a
    certain number of dots left in the maze."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(self, player: Player, maze: MazeGenerator) -> tuple[int, int]:
        """
        DFS, prend en target la position du joueur, renvoi le prochain mouvement du drone.
        a recall a chaque mouvement pour connaitre la prochaine dest en fonction du mouv du joueur
        """
        if not self.is_frozen and self.alive:
            if self.is_vulnerable:
                self.target = self.spawn
            else:
                self.target = (player.x, player.y)
            visited = set()
            stack = [(self.x, self.y, [(self.x, self.y)])]

            while stack:
                x, y, path = stack.pop()

                if self.is_vulnerable:
                    if x == player.x and y == player.y:
                        continue

                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if x == self.target[0] and y == self.target[1]:
                    return path[1]
                moves = self.get_moves_possible(maze, x, y)
                for move in moves:
                    if move == 'DOWN':
                        new_y = y + 1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'UP':
                        new_y = y -1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'RIGHT':
                        new_x = x + 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    elif move == 'LEFT':
                        new_x = x - 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    else:
                        pass



class Pinky(Ghost): # ambushes, dest 2 case devant le player
    """Chases towards the spot 2 Pac-Dots in front of Pac-Man. Due to a bug in the original
    game's coding, if Pac-Man faces upwards, Pinky's target will be 2 Pac-Dots in front of and 2
    to the left of Pac-Man. During Scatter mode, she heads towards the upper-left corner."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(self, player: Player, maze: MazeGenerator) -> tuple[int, int]:
        """
        DFS, prend en target la position du joueur, renvoi le prochain mouvement du drone.
        a recall a chaque mouvement pour connaitre la prochaine dest en fonction du mouv du joueur
        """
        if not self.is_frozen and self.alive:
            if self.is_vulnerable:
                self.target = self.spawn

            else:
                if player.direction is None:
                    self.target = (player.x, player.y)

                elif player.direction == "UP":
                    if player.y - 2 >= 0:
                        self.target = (player.x, player.y - 2)
                    else:
                        self.target = (player.x, player.y)

                elif player.direction == "DOWN":
                    if player.y + 2 <= maze._height - 1:
                        self.target = (player.x, player.y + 2)
                    else:
                        self.target = (player.x, player.y)

                elif player.direction == "RIGHT":
                    if player.x + 2 <= maze._width - 1:
                        self.target = (player.x + 2, player.y)
                    else:
                        self.target = (player.x, player.y)

                elif player.direction == "LEFT":
                    if player.x - 2 >= 0:
                        self.target = (player.x -2, player.y)
                    else:
                        self.target = (player.x, player.y)

            visited = set()
            stack = [(self.x, self.y, [(self.x, self.y)])]

            while stack:
                x, y, path = stack.pop()

                if self.is_vulnerable:
                    if x == player.x and y == player.y:
                        continue

                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if x == self.target[0] and y == self.target[1]:
                    return path[1]
                moves = self.get_moves_possible(maze, x, y)
                for move in moves:
                    if move == 'DOWN':
                        new_y = y + 1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'UP':
                        new_y = y -1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'RIGHT':
                        new_x = x + 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    elif move == 'LEFT':
                        new_x = x - 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    else:
                        pass


class Inky(Ghost): # unpredictable, dest = distance entre blinky et pinky target * 2
    """During Chase mode, his target is a bit complex. His target is relative to both
    Blinky and Pac-Man, where the distance Blinky is from Pinky's target is doubled to
    get Inky's target. He heads to the lower-right corner during Scatter mode."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(self, player: Player, maze: MazeGenerator, blinky: Blinky, pinky: Pinky) -> tuple[int, int]:
        """
        DFS, prend en target la position du joueur, renvoi le prochain mouvement du drone.
        a recall a chaque mouvement pour connaitre la prochaine dest en fonction du mouv du joueur
        """
        if not self.is_frozen and self.alive:
            if self.is_vulnerable:
                self.target = self.spawn
            else:
                self.target = (blinky.target[0] - pinky.target[0], blinky.target[1] - pinky.target[1])
            visited = set()
            stack = [(self.x, self.y, [(self.x, self.y)])]

            while stack:
                x, y, path = stack.pop()

                if self.is_vulnerable:
                    if x == player.x and y == player.y:
                        continue

                if (x, y) in visited:
                    continue
                visited.add((x, y))

                if x == self.target[0] and y == self.target[1]:
                    return path[1]
                moves = self.get_moves_possible(maze, x, y)
                for move in moves:
                    if move == 'DOWN':
                        new_y = y + 1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'UP':
                        new_y = y -1
                        stack.append([x, new_y, path + [(x, new_y)]])
                    elif move == 'RIGHT':
                        new_x = x + 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    elif move == 'LEFT':
                        new_x = x - 1
                        stack.append([new_x, y, path + [(new_x, y)]])
                    else:
                        pass


class Clyde(Ghost): # weird 
    """Chases directly after Pac-Man, but tries to head to his Scatter corner when within
    an 8-Dot radius of Pac-Man. His Scatter Mode corner is the lower-left."""
    def __init__(self, color, spawn_x, spawn_y, is_frozen = False):
        super().__init__(color, spawn_x, spawn_y, is_frozen)

    def next_move(player_pos: tuple[int], maze):
        pass

PlayerTest = Player(3, 10, 10)
BlinkyTest = Blinky("red", 0, 0)
maze = MazeGenerator()
print(BlinkyTest.next_move(PlayerTest, maze))
PinkyTest = Pinky("pink", 14, 14)
print(PinkyTest.next_move(PlayerTest, maze))