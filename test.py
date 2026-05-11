# from mazegenerator.mazegenerator import MazeGenerator


# def get_moves_possible(x, y, maze: MazeGenerator):
#     possible = []
#     current_case_value = maze.maze[y][x]

#     if not (current_case_value & 1):
#         possible.append("UP")
#     if not (current_case_value & 4):
#         possible.append("DOWN")
#     if not (current_case_value & 8):
#         possible.append("LEFT")
#     if not (current_case_value & 2):
#         possible.append("RIGHT")
    
#     return possible


# def is_valid_move(current_pos, next_pos, grid_size):
#     """Check if the move is valid from current_num to next_num (Right or Down)."""
#     # Convert the numbers to their (row, col) positions in the grid
#     current_row, current_col = current_pos[1], current_pos[0]
#     next_row, next_col = (next_pos - 1) // grid_size, (next_pos - 1) % grid_size

#     # Valid moves are Right (same row, next column) or Down (next row, same column)
#     return (next_row == current_row and next_col == current_col + 1) or (next_col == current_col and next_row == current_row + 1)


# def dfs(current_pos: tuple[int, int], path: list, solutions: list, start_pos: tuple[int, int],
#         goal_pos: tuple[int, int], grid_size = 15):

#     if current_pos == goal_pos:
#         solutions.append(path.copy())
#         return solutions

#     moves = [current_pos[0] + 1, current_pos[0] - 1, current_pos[1] + 1, current_pos[1] - 1]

#     for next_pos in moves:
#         if next_pos <= (15 * 15 - 1) and not is_valid_move(current_pos, next_pos, grid_size):
#             path.append(next_pos)
#             dfs(next_pos, path, solutions, start_pos, goal_pos, grid_size)
#             path.pop()


# maze = MazeGenerator()
# solutions = []
# path = []
# print(dfs((0,0), path, solutions, (0,0), (10,10)))


if self.is_vulnerable or dist((self.x, self.y), (player.x, player.y)) <= 3:
                self.target = self.spawn