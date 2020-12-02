def is_row_complete(row):
    return sum(row) == 45


def is_column_complete(column_index, game_grid):
    column_values = []
    for row in game_grid:
        column_values.append(row[column_index])
    return sum(column_values) == 45


def is_solved(game_grid):
    for i in range(0, 9):
        if not is_row_complete(game_grid[i]) or not is_column_complete(i, game_grid):
            return False
    return True


def get_allowed_values_in_row(row, game_grid):
    all_values = {i for i in range(1, 10)}
    unique_row_values = set(game_grid[row])
    unique_row_values.discard(0)
    allowed_row_values = {i for i in all_values if i not in unique_row_values}

    return allowed_row_values


def get_allowed_values_in_column(column, game_grid):
    all_values = {i for i in range(1, 10)}
    unique_column_values = set()
    for row in game_grid:
        unique_column_values.add(row[column])
    unique_column_values.discard(0)
    allowed_column_values = {i for i in all_values if i not in unique_column_values}

    return allowed_column_values


def get_allowed_values_in_sub_matrix(row, column, game_grid):
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
    missing_values_in_row = get_allowed_values_in_row(row, game_grid)
    missing_values_in_column = get_allowed_values_in_column(column, game_grid)
    missing_values_in_sub_matrix = get_allowed_values_in_sub_matrix(row, column, game_grid)

    return missing_values_in_row.intersection(missing_values_in_column.intersection(missing_values_in_sub_matrix))


def get_next_empty_space(game_grid):
    m, n = None, None
    for i, row in enumerate(game_grid):
        for j, column in enumerate(game_grid):
            if game_grid[i][j] == 0:
                return i, j
    return m, n


def solve(game_grid):

    if is_solved(game_grid):
        return True
    else:
        row, column = get_next_empty_space(game_grid)
        if row is None or column is None:
            return False

        else:
            values = get_possible_values_for_space(row, column, game_grid)
            for value in values:
                game_grid[row][column] = value

                if solve(game_grid):
                    return True
                game_grid[row][column] = 0

    return False


def game_handler(game_grid):
    solve(game_grid)
    for row in game_grid:
        print(row, end="\n")


if __name__ == '__main__':
    initial_game = [
        [4, 0, 8, 0, 0, 0, 0, 0, 0]
        , [0, 0, 0, 0, 2, 0, 0, 0, 6]
        , [0, 0, 2, 0, 0, 0, 0, 3, 8]
        , [0, 0, 0, 0, 0, 0, 5, 0, 0]
        , [0, 0, 0, 0, 0, 0, 4, 0, 0]
        , [0, 0, 0, 6, 7, 0, 0, 2, 1]
        , [0, 0, 6, 0, 0, 0, 0, 0, 0]
        , [0, 1, 0, 0, 3, 0, 7, 0, 0]
        , [3, 2, 0, 0, 0, 1, 0, 0, 4]
    ]
    game_handler(initial_game)
