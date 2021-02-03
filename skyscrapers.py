"""Functions for checking validity of 3d board game setting.

    Functions
    ---------
        read_input - read game board file from path
        check_not_finished_board - check if skyscraper board is not finished
        check_uniqueness_in_rows - check buildings of unique height in each row
        check_uniqueness_in_columns - check buildings of unique height in each column
        check_visibility - check visibility for a given line of houses from both sides
        check_horizontal_visibility - check row-wise visibility
        check_vertical_visibility - check column-wise visibility
        check_skyscrapers - check if the board of skyscrapers is valid
"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("docs/check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    with open(path) as input_file:
        contents = input_file.readlines()

    return [line.strip() for line in contents]


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*',\
                                    '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215',\
                                    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215',\
                                    '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        for cell in row:
            if cell == '?':
                return False

    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in all rows have unique height, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215',\
                                    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***22**', '412453*', '423145*', '*543215',\
                                    '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215',\
                                    '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215',\
                                    '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row_idx in range(1, len(board) - 1):
        heights = set()

        for cell_idx in range(1, len(board[row_idx]) - 1):
            if board[row_idx][cell_idx] == '*':
                continue

            if board[row_idx][cell_idx] in heights:
                return False

            heights.add(board[row_idx][cell_idx])

    return True


def check_uniqueness_in_columns(board: list):
    """
    Check buildings of unique height in each column.

    Return True if buildings in all columns column have unique height, False otherwise.

    >>> check_uniqueness_in_columns(['***21**', '412453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_columns(['***21**', '412453*', '4231452', '*543215',\
                                        '*352142', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_columns(['***21**', '412453*', '423145*', '*543215',\
                                        '*35214*', '*41534*', '*2*1***'])
    False
    >>> check_uniqueness_in_columns(['***21**', '432453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for col_idx in range(1, len(board[0]) - 1):
        heights = set()

        for row_idx in range(1, len(board) - 1):
            if board[row_idx][col_idx] == '*':
                continue

            if board[row_idx][col_idx] in heights:
                return False

            heights.add(board[row_idx][col_idx])

    return True


def check_visibility(line: str) -> bool:
    """
    Check visibility for a given line of houses from both sides.

    >>> check_visibility('412354*')
    True
    >>> check_visibility('4123542')
    True
    >>> check_visibility('312354*')
    False
    >>> check_visibility('3123545')
    False
    >>> check_visibility('*12354*')
    True
    >>> check_visibility('*125342')
    True
    """
    heights = list(map(int, line[1:-1]))

    # check visibility for leftmost hint
    if line[0] != '*':
        idx = 0
        count = 0
        curr_max = float('-inf')

        while idx < len(heights):
            if heights[idx] > curr_max:
                count += 1
                curr_max = heights[idx]

            idx += 1

        if count != int(line[0]):
            return False

    # check visibility for rightmost hint
    if line[-1] != '*':
        idx = len(heights) - 1
        count = 0
        curr_max = float('-inf')

        while idx >= 0:
            if heights[idx] > curr_max:
                count += 1
                curr_max = heights[idx]

            idx -= 1

        if count != int(line[-1]):
            return False

    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row_idx in range(1, len(board) - 1):
        if not check_visibility(board[row_idx]):
            return False

    return True


def check_vertical_visibility(board: list):
    """
    Check column-wise visibility (left-right and vice versa)

    Return True if all vertical hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_vertical_visibility(['***21**', '412453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_vertical_visibility(['***21**', '412453*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_vertical_visibility(['***21**', '452413*', '423145*', '*543215',\
                                        '*35214*', '*41532*', '*2*1***'])
    False
    """
    for col_idx in range(1, len(board[0]) - 1):
        line = "".join([board[row_idx][col_idx]
                        for row_idx, _ in enumerate(board)])

        if not check_visibility(line):
            return False

    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("docs/check.txt")
    True
    """
    board = read_input(input_path)

    is_finished = check_not_finished_board(board)
    is_unique = check_uniqueness_in_rows(
        board) and check_uniqueness_in_columns(board)

    if not (is_finished and is_unique):
        return False

    is_horizontally_valid = check_horizontal_visibility(board)
    is_vertically_valid = check_vertical_visibility(board)

    return is_horizontally_valid and is_vertically_valid


if __name__ == '__main__':
    import doctest
    doctest.testmod()
