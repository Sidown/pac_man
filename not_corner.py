from mazegenerator.mazegenerator import MazeGenerator


def not_corner(maze: MazeGenerator, x: int, y: int) -> bool:
    """
    check if a position is a corner of the maze
    arguments:
    maze -> the current maze
    x -> column of the cell
    y -> row of the cell
    return value:
    True if the cell is not a corner
    False otherwise
    """
    if x == 0 and y == 0:
        return False
    if x == 0 and y == len(maze.maze) - 1:
        return False
    if x == len(maze.maze[0]) - 1 and y == 0:
        return False
    if x == len(maze.maze[0]) - 1 and y == len(maze.maze) - 1:
        return False
    return True
