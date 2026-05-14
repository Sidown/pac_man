from mazegenerator.mazegenerator import MazeGenerator


def not_corner(maze: MazeGenerator, x: int, y: int) -> bool:
    """check if a position is a corner of the maze"""
    if x == 0 and y == 0:
        return False
    if x == 0 and y == len(maze.maze) - 1:
        return False
    if x == len(maze.maze[0]) - 1 and y == 0:
        return False
    if x == len(maze.maze[0]) - 1 and y == len(maze.maze) - 1:
        return False
    return True