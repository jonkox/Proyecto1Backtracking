import random
import timeit

#region teacher
"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Teachers part
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


def next_empty(board, i, j):
    idx = i * len(board[0]) + j
    for idx in range(i * len(board[0]) + j, len(board[0]) * len(board)):
        x = idx // len(board[0])
        y = idx % len(board[0])
        if board[x][y] == '*':
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
#endregion

#region students
"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Our part
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
solutions_list = [] #save te valid solutions
"""
This function calculates the amount of tiles the set has according to the base matrix
It tells 10 tiles if the set is double 3, 21 tiles if it is double 5, 28 tiles if it is double 6, etc
It receives the base matrix
It returns an integer with the amount of tiles of the set
"""


def get_tiles_amount(matrix):
    return (len(matrix) * len(matrix[0])) // 2


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
This function checks if a given combination is valid or not
It receives a string that represents how the tiles might be accommodated
This string is just a bunch of 0 and 1, 0 is horizontal and 1 vertical
It returns True if the combination is valid
It returns False if the combination iss wrong
"""


def is_this_combination_valid(possible_solution, num_matrix, horizontal_length, vertical_length):
    i = 0
    j = 0

    found_tiles = []

    # This is an auxiliary matrix that helps to know which tiles are already taken
    # False means free space and True means taken space
    aux_matrix = [[False] * horizontal_length for _ in range(vertical_length)]

    # This for checks the accommodation of each tile in the given combination
    for accommodation in possible_solution:
        tile_used = False  # Needed for a validation

        # Checks where is a tile available to try
        while i < vertical_length:

            if not aux_matrix[i][j]:
                # We found a free space

                if accommodation == "1":
                    # The tile has to go vertical

                    if i + 1 == vertical_length:
                        # Index out of range
                        return False

                    if aux_matrix[i + 1][j]:
                        # The space down is already taken
                        return False

                    # Creates/calculates the given tile
                    tile = (num_matrix[i][j], num_matrix[i + 1][j])

                    if tile in found_tiles:
                        # It is a repeated tile
                        return False

                    # This tile is fine

                    # Adds tile to list
                    found_tiles.append(tile)
                    found_tiles.append(tile[::-1])

                    # Puts this space and the one at the right as taken
                    aux_matrix[i][j] = True
                    aux_matrix[i + 1][j] = True

                    tile_used = True

                else:
                    # The tile has to go horizontal

                    if j + 1 == horizontal_length:
                        # Index out of range
                        return False

                    if aux_matrix[i][j + 1]:
                        # The space at the right is already taken
                        return False

                    # Creates/calculates the given tile
                    tile = (num_matrix[i][j], num_matrix[i][j + 1])

                    if tile in found_tiles:
                        # It is a repeated tile
                        return False

                    # This tile is fine

                    # Adds tile to list
                    found_tiles.append(tile)
                    found_tiles.append(tile[::-1])

                    # Puts this space and the one down as taken
                    aux_matrix[i][j] = True
                    aux_matrix[i][j + 1] = True

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
This function finds the solution of the domino matrix by brute strength
It tries every possible permutation until getting the right one
It receives an integer matrix that represent the domino values
It returns a list with each correct permutation
"""


def brute_strength_solution(matrix):
    amount_tiles = get_tiles_amount(matrix)
    solutions_list.clear()
    limit = 2 ** amount_tiles

    vertical_length = len(matrix)
    horizontal_length = vertical_length + 1

    for i in range(0, limit):
        possible_solution = dec_to_bin(i, amount_tiles)  # The permutation corresponding to this iteration
        # Checks if this permutation is correct
        if is_this_combination_valid(possible_solution, matrix, horizontal_length, vertical_length):
            # Found a correct accommodation of the tiles
            solutions_list.append(possible_solution)

    return


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Backtracking
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

backtrackingList = []  # Holds the correct solutions of the BACKTRACKING method

"""
This function exactly copies a matrix
It is kind of silly
It was necessary because Python works by reference and it gave trouble in another algorithm
It receives a matrix
It returns an exact copy of the input matrix
"""


def copy_matrix(input_matrix):
    output_matrix = []
    for sublist in input_matrix:
        my_sublist = []
        for element in sublist:
            my_sublist.append(element)
        output_matrix.append(my_sublist)

    return output_matrix


"""
This function makes sure that a new tile can be added vertically to the solution that is being formed
Parameters:
    num_matrix is an integer matrix that represents the domino values
    vertical_length is and integer that tells the vertical range, needed to know if we are out of index
    horizontal_length is and integer that tells the horizontal range, needed to know if we are out of index
    i is an integer that is the vertical index
    j is an integer that is the horizontal index
    found_tiles is a list that stores the values of tiles we have found, avoids repeated tiles
    aux_matrix is a boolean matrix, identical in size to num_matrix, that tells which spaces are free and which ones are taken
Returns:
    Returns False if it is not valid

    If it is valid returns i and j in the new positions to maintain the order
    (Doesnt return, but by reference also modifies the outer scope aux_matrix and found_tiles and maintains the order)
"""


def vertical_verification(num_matrix, vertical_length, horizontal_length, i, j, found_tiles, aux_matrix):
    tile_used = False  # Needed for a validation
    while i < vertical_length:

        if not aux_matrix[i][j]:
            # We found a free space
            if i + 1 == vertical_length:
                # Index out of range
                return False

            if aux_matrix[i + 1][j]:
                # The space down is already taken
                return False

            # Creates/calculates the given tile
            tile = (num_matrix[i][j], num_matrix[i + 1][j])

            if tile in found_tiles:
                # It is a repeated tile
                return False

            # This tile is fine
            tile_used = True

            # Adds tile to list
            found_tiles.append(tile)
            found_tiles.append(tile[::-1])

            # Puts this space and the one at the right as taken
            aux_matrix[i][j] = True
            aux_matrix[i + 1][j] = True

        # Moves the index for the next iteration
        j += 1
        if j == horizontal_length:
            j = 0
            i += 1

        if tile_used:
            # There were no errors, possible solution completely valid
            return i, j


"""
This function makes sure that a new tile can be added horizontally to the solution that is being formed
Parameters:
    num_matrix is an integer matrix that represents the domino values
    vertical_length is and integer that tells the vertical range, needed to know if we are out of index
    horizontal_length is and integer that tells the horizontal range, needed to know if we are out of index
    i is an integer that is the vertical index
    j is an integer that is the horizontal index
    found_tiles is a list that stores the values of tiles we have found, avoids repeated tiles
    aux_matrix is a boolean matrix, identical in size to num_matrix, that tells which spaces are free and which ones are taken
Returns:
    Returns False if it is not valid

    If it is valid returns i and j in the new positions to maintain the order
    (Doesnt return, but by reference also modifies the outer scope aux_matrix and found_tiles and maintains the order)
"""


def horizontal_verification(num_matrix, vertical_length, horizontal_length, i, j, found_tiles, aux_matrix):
    tile_used = False  # Needed for a validation
    while i < vertical_length:

        if not aux_matrix[i][j]:
            # We found a free space
            if j + 1 == horizontal_length:
                # Index out of range
                return False

            if aux_matrix[i][j + 1]:
                # The space at the right is already taken
                return False

            # Creates/calculates the given tile
            tile = (num_matrix[i][j], num_matrix[i][j + 1])

            if tile in found_tiles:
                # It is a repeated tile
                return False

            # This tile is fine
            tile_used = True

            # Adds tile to list
            found_tiles.append(tile)
            found_tiles.append(tile[::-1])

            # Puts this space and the one down as taken
            aux_matrix[i][j] = True
            aux_matrix[i][j + 1] = True

        # Moves the index for the next iteration
        j += 1
        if j == horizontal_length:
            j = 0
            i += 1

        if tile_used:
            # There were no errors, possible solution completely valid
            return i, j


"""
Functioning:
    This is a recursive function generates every possible permutation of the domino matrix by backtracking
    This is based on the binary tree idea
    It generates every possible permutation tile by tile
    It makes the trim by validating each added tile to the possible solution
    In case a tile is incorrect it stops with the solution and does not even try its children
    and instead tries with the previous possibilities
    The base case is when all the tiles are checked and accepted
Parameters:
    solution is string that is the possible solution that is being formed, if everything is fine it increases a tile (character) per each call
    num_matrix is an integer matrix that represent the domino values
    amount_tiles, vertical_length, horizontal_length are integers needed for some validations and always passed to avoid calculating them over and over
    i and j are the indexes that tell from where we were left, useful to avoid starting from the very first position,
        if everything is fine they change per each call
    found_tiles is a list to check all the found tiles at that moment, needed to avoid repetition, if everything is fine they change per each call 
    aux_matrix is a boolean matrix identical in size to num_matrix that tells which spaces are taken and which ones are free
        if everything is its values change per each call

It fills a list with each correct permutation
"""


def backtracking_aux(solution, num_matrix, amount_tiles, vertical_length, horizontal_length, i, j, found_tiles,aux_matrix):
    # Base case
    if len(solution) == amount_tiles:
        backtrackingList.append(solution)

    # Creating the possible solution
    else:
        # Horizontal child
        tiles_result = found_tiles[:]
        aux_result = copy_matrix(aux_matrix)  # Copy needed to avoid errors, python works by reference

        # Trim
        result = horizontal_verification(num_matrix, vertical_length, horizontal_length, i, j, tiles_result, aux_result)

        if not result:
            # An error occurred, no point of continuing with this branch and its children
            pass
        else:
            # It had no problem we continue with this path
            x, y = result
            backtracking_aux(solution + "0", num_matrix, amount_tiles, vertical_length, horizontal_length, x, y,tiles_result, aux_result)

        # Vertical child
        tiles_result = found_tiles[:]
        aux_result = copy_matrix(aux_matrix)  # Copy needed to avoid errors, python works by reference

        # Trim
        result = vertical_verification(num_matrix, vertical_length, horizontal_length, i, j, tiles_result, aux_result)

        if not result:
            # An error occurred, no point of continuing with this branch and its children
            pass
        else:
            # It had no problem we continue with this path
            x, y = result
            backtracking_aux(solution + "1", num_matrix, amount_tiles, vertical_length, horizontal_length, x, y,tiles_result, aux_result)


"""
This function finds the correct solutions of the domino matrix by backtracking
Actually this is not the backtracking algorithm, this function makes the necessary pre-steps to apply the algorithm
It receives an integer matrix that represent the domino values
It fills a list with each correct permutation
"""


def backtracking_solution(matrix):
    backtrackingList.clear()

    amount_tiles = get_tiles_amount(matrix)
    vertical_length = len(matrix)
    horizontal_length = vertical_length + 1
    # This is an auxiliary matrix that helps to know which tiles are already taken
    # False means free space and True means taken space
    aux_matrix = [[False] * horizontal_length for _ in range(vertical_length)]

    # Calls the real recursive backtracking function
    backtracking_aux("", matrix, amount_tiles, vertical_length, horizontal_length, 0, 0, [],aux_matrix)
#endregion

#region testings
"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Testing
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This function writes on a.txt file the time of each algorithm solving a set
It receives as parameter the time of brute strength, time of backtracking and the size of the set
It writes on the .txt file
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""


def write_set(brute_time, backtracking_time, set):
    # Corrects format, avoids scientific notation
    brute_time = format(float(brute_time), '.8f')
    backtracking_time = format(float(backtracking_time), '.8f')

    # Writes on file
    file = open("pruebas.txt", "a")
    file.write("Set doble " + set + " - fuerza bruta - " + brute_time + "s \n")
    file.write("Set doble " + set + " - backtracking - " + backtracking_time + "s \n")
    file.write("\n")
    file.close()


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This function writes on a.txt file the average time of each algorithm solving a set many times
It receives as parameter the average time of brute strength, average time of backtracking and the size of the set
It writes on the .txt file
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
"""

def write_average(brute_average, backtracking_average, set):
    # Corrects format, avoids scientific notation
    brute_average = format(float(brute_average), '.8f')
    backtracking_average = format(float(backtracking_average), '.8f')

    # Writes on file
    file = open("pruebas.txt", "a")
    file.write("Promedio de fuerza bruta con set doble " + set + ": " + brute_average + "s \n")
    file.write("Promedio de backtracking con set doble " + set + ": " + backtracking_average + "s \n")
    file.write("\n")
    file.write(
        "\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    file.write("\n\n")
    file.close()


# To avoid repeated text
file = open("pruebas.txt", "w")
file.write("")
file.close()

# From set double 1 to set double 9
for i in range(1, 10):
    # To get averages
    bruteSum = 0
    backtrackingSum = 0

    # Three cases for set
    for j in range(0, 3):
        Matrix = False
        while not Matrix:  # This loop is very necessary to make sure we get a matrix and never get False
            Matrix = create_puzzle(i)

        # Respective times of this case
        bruteTime = timeit.timeit(lambda: brute_strength_solution(Matrix), number=1)
        backtrackingTime = timeit.timeit(lambda: backtracking_solution(Matrix), number=1)

        # Saving on a .txt the times
        write_set(bruteTime, backtrackingTime, str(i))

        # Forming the averages
        bruteSum += bruteTime
        backtrackingSum += backtrackingTime

    # Saving on a .txt the average of this set
    write_average(bruteSum / 3, backtrackingSum / 3, str(i))
    """


def proofs(n, cantidad_de_pruebas, algoritmo):
    time = 0

    Matrix = False
    while not Matrix:  # This loop is very necessary to make sure we get a matrix and never get False
        Matrix = create_puzzle(n)

    #evaluates which algorithm will use
    if algoritmo == 0:

        for i in range(cantidad_de_pruebas):
            time += timeit.timeit(lambda: brute_strength_solution(Matrix), number=1)

    if algoritmo == 1:

        for i in range(cantidad_de_pruebas):
            time += timeit.timeit(lambda: backtracking_solution(Matrix), number=1)


    #divide between the amount of proofs
    time = time / cantidad_de_pruebas

    #formats the result in case that it become in cientific notation
    if n == 1 or n == 0:
        time = "{:f}".format(time)

    #print the info
    print("La medición se hizo con un n= ",n," unas ", i, " veces.")
    print("Su promedio de tiempo de ejecucion es -> ", time)



Matrix = False
while not Matrix:  # This loop is very necessary to make sure we get a matrix and never get False
    Matrix = create_puzzle(12)


print("prueba sola->",timeit.timeit(lambda: backtracking_solution(Matrix), number=1))



#endregion
