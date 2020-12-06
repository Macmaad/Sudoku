"""
Creating a Sudoku Game. Read README for more information and the algorithm that
it is using to work.
"""
from random import randint


class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []


def remove_n_random_numbers(n, game_grid):
    """  When we have solver our Sudoku, to give an empty game to the
    user we need to remove up to n values (minimum numbers on grid must be 17).

    While we don't remove the total of numbers we want. It keeps setting values to 0.

    :param n: Int with total of numbers to remove.
    :param game_grid: Full 9x9 grid for game without 0.
    :return: Game grid with 81 - n 0.
    """
    removed = 0
    while removed < n:
        row, column = randint(0, 8), randint(0, 8)
        if game_grid[row][column] != 0:
            removed += 1
            game_grid[row][column] = 0
    return game_grid


def is_row_complete(row):
    """
    Validates when we are solving the sudoku if the row is complete. We do
    this just checking if the sum of the values == 45.  n = 9 n(n + 1)/2

    Using python sum() method to add over the list.

    :param row: Row list that we want to check
    :return: True if the sum == 45 else False
    """
    return sum(row) == 45


def is_column_complete(column_index, game_grid):
    """
    Validate if the column is complete. It works with the sum of the values on
    the column. If the sum matches 45 the column is complete.

    Adding all the values that are on the column and with the sum() method
    we can get the sum of that list.

    :param column_index: Column index that we want to check.
    :param game_grid: Game grid
    :return: True if the sum == 45 else False
    """
    column_values = []
    for row in game_grid:
        column_values.append(row[column_index])
    return sum(column_values) == 45


def is_solved(game_grid):
    """
    Check if the game is solved with the "is_column_complete" and "is_row_complete"
    method.
    :param game_grid: Actual grid that we are solving
    :return: True if both functions for all the rows and columns are solved else False
    """
    for i in range(0, 9):
        if not is_row_complete(game_grid[i]) or not is_column_complete(i, game_grid):
            return False
    return True


def get_allowed_values_in_row(row, game_grid):
    """
    When we are filing the grid we need to check which values are allowed on the row
    that we are going to insert a new number.

    :param row: Index ot the row we are working.
    :param game_grid: Game grid.
    :return: Set of allowed values for the row.
    """
    all_values = {i for i in range(1, 10)}
    unique_row_values = set(game_grid[row])
    unique_row_values.discard(0)
    allowed_row_values = {i for i in all_values if i not in unique_row_values}

    return allowed_row_values


def get_allowed_values_in_column(column, game_grid):
    """
    When we are filling the game grid we need to check the allowed
    values for the columns.

    :param column: Index for the column that we are working.
    :param game_grid: Game grid. 9x9 matrix
    :return: Set with the allowed values that we can use on that place.
    """
    all_values = {i for i in range(1, 10)}
    unique_column_values = set()
    for row in game_grid:
        unique_column_values.add(row[column])
    unique_column_values.discard(0)
    allowed_column_values = {i for i in all_values if i not in unique_column_values}

    return allowed_column_values


def get_allowed_values_in_sub_matrix(row, column, game_grid):
    """
    We also need to check the allowed values for the 3x3 matrix where the cell is.
    :param row: Index for the row that we are working
    :param column: Index for the column we are working.
    :param game_grid: Complete 9x9 matrix for the game grid on the actual state.
    :return: Set with the allowed values for the 3x3 matrix.
    """
    all_values = {i for i in range(1, 10)}
    unique_sub_matrix_values = set()
    row_for_sub_matrix = int(row/3) * 3
    column_for_sub_matrix = int(column/3) * 3
    for i in range(row_for_sub_matrix, row_for_sub_matrix + 3):
        for j in range(column_for_sub_matrix, column_for_sub_matrix + 3):
            unique_sub_matrix_values.add(game_grid[i][j])
    unique_sub_matrix_values.discard(0)
    allowed_sub_matrix_values = {i for i in all_values if i not in unique_sub_matrix_values}

    return allowed_sub_matrix_values


def get_possible_values_for_space(row, column, game_grid):
    """
    With the get_allowed_values_in_row, get_allowed_values_in_column and get_allowed_values_in_sub_matrix
    we can make the intersection to know the allowed value for the cel [row][column] that we are working.

    :param row: Index of the row where the actual cell is working.
    :param column: Index of the column where the actual cell is working.
    :param game_grid: Complete 9x9 game grid.
    :return: Set with the allowed values for the cell.
    """
    missing_values_in_row = get_allowed_values_in_row(row, game_grid)
    missing_values_in_column = get_allowed_values_in_column(column, game_grid)
    missing_values_in_sub_matrix = get_allowed_values_in_sub_matrix(row, column, game_grid)

    return missing_values_in_row.intersection(missing_values_in_column.intersection(missing_values_in_sub_matrix))


def get_next_empty_space(game_grid):
    """
    Looking all over the rows get the next index for the row and column
    that has a 0 as a value.
    :param game_grid: Complete 9x9 game grid.
    :return: The row index and column index of the cell with value = 0
    """
    m, n = None, None
    for i, row in enumerate(game_grid):
        for j, column in enumerate(game_grid):
            if game_grid[i][j] == 0:
                return i, j
    return m, n


def solve(game_grid, nodes_list, head):
    """
    Using DFS search tree (recursive) it solves the game.

    If the game is solved returns True
    else
    Check for an empty space and get the allowed values for that spaces
    While looping through the list of allowed values if recursively
    looks for the next one or returns if one is not valid.

    :param game_grid: 9x9 Game grid.
    :return: Game grid 9x9 without any value = 0 ore False if there is not solution.
    """

    if is_solved(game_grid):
        return True
    else:
        row, column = get_next_empty_space(game_grid)
        if row is None or column is None:
            return False

        else:
            values = get_possible_values_for_space(row, column, game_grid)
            for value in values:
                new_head = Tree(value)
                head.children.append(new_head)
                game_grid[row][column] = value
                nodes_list.append(value)

                if solve(game_grid, nodes_list, new_head):
                    return True
                game_grid[row][column] = 0

    return False


def solve_handler(game_grid, head):
    """
    As a main()
    :param head:
    :param game_grid: Complete 9x9 Grid
    :return: Solved game grid.
    """
    nodes_list = []
    solve(game_grid, nodes_list, head)
    return game_grid, nodes_list


def set_3_3_sub_matrix_initial_values(grid):
    """
    With a 9x9 grid with all the values as 0. It sets unique values form 1 -9 to each
    3x3 matrix over the diagonal of matrix
    :param grid: Grid with all values = 0
    :return: Grid with all values = 0 except all the 3x3 matrix on the diagonal.
    """
    for i in range(3):
        numbers = []
        while len(numbers) < 9:
            new_number = randint(1, 9)
            if new_number not in numbers:
                numbers.append(new_number)
        for j in range(i * 3, i * 3 + 3):
            for k in range(i * 3, i * 3 + 3):
                grid[j][k] = numbers.pop()
    return grid


def create_initial_grid():
    """
    Handle initial creation of the Game.
    :return: 9x9 matrix with all 3x3 sub matrix on the diagonal filled.
    """
    empty_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    grid_with_sub_matrix = set_3_3_sub_matrix_initial_values(empty_grid)
    return grid_with_sub_matrix


def create_sudoku(head):
    """
    Just like other main handler.
    :return:
    """
    initial_game = create_initial_grid()
    solved_game, nodes_list = solve_handler(initial_game, head)

    for row in solved_game:
        print(row, end="\n")
    print("\n")

    user_game_output = remove_n_random_numbers(60, solved_game)
    print(nodes_list)

    return user_game_output


if __name__ == '__main__':
    tree_node = Tree(None)
    game = create_sudoku(tree_node)
    for game_row in game:
        print(game_row, end="\n")
