
import random


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Teachers part
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


def next_empty(Board, i, j):
    idx = i * len(Board[0]) + j
    for idx in range(i * len(Board[0]) + j, len(Board[0]) * len(Board)):
        x = idx // len(Board[0])
        y = idx % len(Board[0])
        if Board[x][y] == '*':
            return (x, y)
    return (-1, -1)


def make_board(x, y):
    return [['*' for x in range(y)] for x in range(x)]


def make_tiles(n):
    Tiles = []
    for x in range(0, n + 1):
        for y in range(x, n + 1):
            Tiles = Tiles + [[x, y]]
    return Tiles


def check(Board, i, j, ori):
    # Horizontal
    r = False
    if ori == 0:
        if j < len(Board[i]) - 1:
            if Board[i][j] == '*' and Board[i][j + 1] == '*':
                r = True
    # Vertical
    elif ori == 1:
        if i < len(Board) - 1:
            if Board[i][j] == '*' and Board[i + 1][j] == '*':
                r = True
    return r


def place_tile(Board, i, j, ori, tile):
    Board[i][j] = tile[0]
    if ori == 0:
        Board[i][j + 1] = tile[1]
    else:
        Board[i + 1][j] = tile[1]


def create_puzzle(n):
    """
    es posible que el algoritmo generador falle y no encuentre un tablero válido
    Si sucede, retorna falso y no genera ningún archivo de salida
    """

    board = make_board(n + 1, n + 2)
    tiles = make_tiles(n)
    random.shuffle(tiles)
    solution = []

    current_pos = (0, 0)
    while tiles != []:
        next_tile = tiles.pop()
        random.shuffle(next_tile)
        current_pos = next_empty(board, current_pos[0], current_pos[1])
        ori = random.randint(0, 1)
        if not (check(board, current_pos[0], current_pos[1], ori)):
            ori = (ori + 1) % 2
        if check(board, current_pos[0], current_pos[1], ori):
            place_tile(board, current_pos[0], current_pos[1], ori, next_tile)
            solution = solution + [ori]
        else:
            return False
    toFile("TableroDoble" + str(n), n, board, solution)

    return board


def toFile(filename, n, board, solution):
    file = open(filename + ".txt", "w")
    file.write(str(n) + "\n")
    file.write("\n")

    # tablero
    for fila in board:
        for e in fila:
            file.write(str(e) + " ")
        file.write("\n")
    file.write("\n")

    for i in solution:
        file.write(str(i) + " ")
    file.write("\n")






"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Our part
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""




"""
This function calculates the amount of tiles the set has according to the base matrix
It tells 10 tiles if the set is double 3, 21 tiles if it is double 5, 28 tiles if it is double 6, etc
It receives the base matrix
It returns an integer with the amount of tiles of the set
"""


def get_tiles_amount(matrix):
    return (len(matrix) * len(matrix[0])) // 2




"""
This function calculates the value of the set according to the base matrix
It tells if the set is double 3, double 5, double 6, etc
It receives the base matrix
It returns an integer with the value of the set
"""


def get_set_size(matrix):
    return len(matrix) - 1


"""
This function checks if a given combination is valid or not
It receives a string that represents how the tiles might be accommodated
This string is just a bunch of 0 and 1, 0 is horizontal and 1 vertical
It returns True if the combination is valid
It returns False if the combination iss wrong
"""


def is_this_combination_valid(possible_solution, num_matrix, set_size):
    horizontal_length = set_size+2
    vertical_length = set_size+1

    i = 0
    j = 0

    found_tiles = []

    # This is an auxiliary matrix that helps to know which tiles are already taken
    # False means free space and True means taken space
    aux_matrix = [[False]*horizontal_length for _ in range(vertical_length)]

    # This for checks the accommodation of each tile in the given combination
    for accommodation in possible_solution:
        # Checks where is a tile available to try

        while i < vertical_length:
            tile_used = False

            if not aux_matrix[i][j]:
                # We found a free space

                if accommodation == "1":
                    # The tile has to go vertical

                    if i+1 == vertical_length:
                        # Index out of range
                        return False

                    if aux_matrix[i+1][j]:
                        # The space down is already taken
                        return False

                    # Creates/calculates the given tile
                    tile = (num_matrix[i][j], num_matrix[i+1][j])

                    if tile in found_tiles:
                        # It is a repeated tile
                        return False

                    # This tile is fine

                    # Adds tile to list
                    found_tiles.append(tile)
                    found_tiles.append(tile[::-1])

                    # Puts this space and the one at the right as taken
                    aux_matrix[i][j] = True
                    aux_matrix[i+1][j] = True

                    tile_used = True

                else:
                    # The tile has to go horizontal

                    if j+1 == horizontal_length:
                        # Index out of range
                        return False

                    if aux_matrix[i][j+1]:
                        # The space at the right is already taken
                        return False

                    # Creates/calculates the given tile
                    tile = (num_matrix[i][j], num_matrix[i][j+1])

                    if tile in found_tiles:
                        # It is a repeated tile
                        return False

                    # This tile is fine

                    # Adds tile to list
                    found_tiles.append(tile)
                    found_tiles.append(tile[::-1])

                    # Puts this space and the one down as taken
                    aux_matrix[i][j] = True
                    aux_matrix[i][j+1] = True

                    tile_used = True

            # Moves the index for the next iteration
            j += 1
            if j == horizontal_length:
                j = 0
                i += 1

            if tile_used:
                break

    # There were no errors, possible solution completely valid
    return True


"""
This function passes a number from decimal to binary
It receives an integer that is the number
It returns a String that is the same number in binary
"""


def dec_to_bin(x, size):
    my_string = str(bin(x)[2:])

    while len(my_string) < size:
        my_string = "0" + my_string

    return my_string



"""
This function finds the solution of the domino matrix by brute strength
It tries every possible permutation until getting the right one
It receives an integer that is the value of the set
Tells if its double 3, double 5, double 6, etc
It returns a string with the first correct permutation it finds
"""


def brute_strength_solution(matrix):
    set_size = get_set_size(matrix)
    amount_tiles = get_tiles_amount(matrix)
    solutions_list = []

    # This for tries every possible permutation
    for i in range(0, 2 ** amount_tiles):
        possible_solution = dec_to_bin(i, amount_tiles)  # The permutation corresponding to this iteration
        # Checks if this permutation is correct
        if is_this_combination_valid(possible_solution, matrix, set_size):
            # Found a correct accommodation of the tiles
            solutions_list.append(possible_solution)

    return solutions_list


def backtracking_solution(matrix):
    return False


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Testing
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


for i in range(1, 14):
    matrix = False
    while not matrix:  # This loop is very necessary to make sure we get a matrix and never get False
        matrix = create_puzzle(i)


    print(brute_strength_solution(matrix))
    # print(backtracking_solution(matrix))
