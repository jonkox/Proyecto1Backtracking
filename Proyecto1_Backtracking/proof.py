#region imports
from tkinter import Tk, Label, Button, Spinbox
from random import randint
import timeit
import main
from main import create_puzzle
#endregion


def calculate_centered_start(length):
    i = (7 - length) // 2

    # i = j
    # i = 10 - length = 11-1 - length = 11 - length - 1 = 11 - (length +1)
    # If you think it the vertical relationship has to be always kept, example (0, 0)

    return i, i

def paint_matrix_gui(buttons, n,function, label,solution):
    colorList = ["white", "yellow", "blue", "green yellow","CadetBlue1","dodger blue", "orchid1", "salmon","brown2",
                 "LightPink1", "SteelBlue1", "snow3", "dark slate gray", "papaya whip", "khaki", "medium sea green"]

    #reset all the buttons
    for row in buttons:
        for column in row:
            column.configure(bg="gray1", text="")

    #region set parameters

    # Validate which case are we going to use

    if function == 0:

        #Get the numbers matrix
        matrix = False
        while matrix == False:
            num_matrix = create_puzzle(n)
            if num_matrix != False:
                matrix = True

        #Get a solution with our algorithm

        if n == 1 or n == 0:
            elapsedTime = timeit.timeit(lambda: main.brute_strength_solution(num_matrix), number=1)
            elapsedTime = "{:f}".format(elapsedTime)


        else:
            elapsedTime = timeit.timeit(lambda: main.brute_strength_solution(num_matrix), number=1)




        possible_solution = main.solutions_list
        possible_solution = possible_solution[randint(0, len(possible_solution)-1)]


        #Set horizontal and vertical values
        horizontal_length = len(num_matrix[0])
        vertical_length = len(num_matrix)

    if function == 1:

        matrix = False
        while matrix == False:
            num_matrix = create_puzzle(n)
            if num_matrix != False:
                matrix = True
        if n == 1 or n == 0:
            elapsedTime = timeit.timeit(lambda: main.backtracking_solution(num_matrix), number=1)
            elapsedTime = "{:f}".format(elapsedTime)


        else:
            elapsedTime = timeit.timeit(lambda: main.backtracking_solution(num_matrix), number=1)

        randomSolution = randint(0, len(main.backtrackingList) - 1)
        possible_solution = main.backtrackingList[randomSolution]

        horizontal_length = len(num_matrix[0])
        vertical_length = len(num_matrix)


    i = 0
    j = 0

    x, y = calculate_centered_start(vertical_length)
    x = 0
    y =0


    # This is an auxiliary matrix that helps to know which tiles are already taken
    # False means free space and True means taken space
    painted_matrix = [[False] * horizontal_length for _ in range(vertical_length)]

    #endregion

    myRandomColor = 0
    # This for checks the accommodation of each tile in the given combination
    for accommodation in possible_solution:
        tile_used = False  # Needed for a validation

        # Checks where is a tile available to try
        while i < vertical_length:
            if myRandomColor == len(colorList) - 1:
                myRandomColor = 0
            if not painted_matrix[i][j]:
                # We found a free space
                tile_used = True

                if accommodation == "1":
                    # The tile has to go vertical

                    # Puts this space and the one at the right as taken
                    painted_matrix[i][j] = True
                    painted_matrix[i + 1][j] = True

                    # Paints the matrix cells
                    buttons[x][y].configure(bg=colorList[myRandomColor])
                    buttons[x+1][y].configure(bg=colorList[myRandomColor])

                    # Gives value to the matrix cells
                    buttons[x][y].configure(text=str(num_matrix[i][j]))
                    buttons[x + 1][y].configure(text=str(num_matrix[i+1][j]),fg="white")

                else:
                    # The tile has to go horizontal

                    # Puts this space and the one down as taken
                    painted_matrix[i][j] = True
                    painted_matrix[i][j + 1] = True

                    # Paints the matrix cells
                    buttons[x][y].configure(bg=colorList[myRandomColor])
                    buttons[x][y+1].configure(bg=colorList[myRandomColor])

                    # Gives value to the matrix cells
                    buttons[x][y].configure(text=str(num_matrix[i][j]),fg="white")
                    buttons[x][y+1].configure(text=str(num_matrix[i][j+1]),fg="white")

            # Moves the index for the next iteration
            j += 1
            y += 1
            myRandomColor += 1
            if j == horizontal_length:
                j = 0
                i += 1

                y = 0
                x += 1

            if tile_used:
                break

    #Update labels
    label.configure(text="Tiempo de Ejecución ->  " + str(elapsedTime),fg="white")
    solution.configure(text=str(possible_solution),fg="white")



"""Main window: this function show the main window to can see both solutions to a problem"""
def main_window():

    #region creacion y configuracion de la window
    window = Tk()

    # titulo
    window.title("DOMINOSA")

    # se le da tamaño a la window principal
    window.geometry("625x900")
    # color a la window principal
    window.configure(bg="gray1")

    etiqueta = Label(window, text="DOMINOSA", bg="red",fg= "white", padx=88, pady=5, font="Helvetica 25",relief="solid").place(x=150, y=5)

    window.resizable(False, False)

    window.iconbitmap('domino.ico')

    #endregion

    # region rowS
    buttons = []
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    row10 = []

    # endregion

    #region columnas
    # region COLUMNA 1

    button_game1x1 = Button(window, width=4, bg="black", state="disabled", height=2, text="")
    button_game1x1.place(x=100, y=100)
    buttons.append(button_game1x1)
    row1.append(button_game1x1)

    button_game1x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game1x2.place(x=100, y=142)
    buttons.append(button_game1x2)
    row2.append(button_game1x2)

    button_game1x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game1x3.place(x=100, y=184)
    buttons.append(button_game1x3)
    row3.append(button_game1x3)

    button_game1x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x4.place(x=100, y=226)
    buttons.append(button_game1x4)
    row4.append(button_game1x4)

    button_game1x5 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x5.place(x=100, y=268)
    buttons.append(button_game1x5)
    row5.append(button_game1x5)

    button_game1x6 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x6.place(x=100, y=310)
    buttons.append(button_game1x6)
    row6.append(button_game1x6)

    button_game1x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game1x7.place(x=100, y=352)
    buttons.append(button_game1x7)
    row7.append(button_game1x7)

    button_game1x8 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x8.place(x=100, y=394)
    buttons.append(button_game1x8)
    row8.append(button_game1x8)

    button_game1x9 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x9.place(x=100, y=436)
    buttons.append(button_game1x9)
    row9.append(button_game1x9)

    button_game1x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game1x10.place(x=100, y=478)
    buttons.append(button_game1x10)
    row10.append(button_game1x10)

    # endregion

    # region COLUMNA 2
    button_game2x1 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x1.place(x=140, y=100)
    buttons.append(button_game2x1)
    row1.append(button_game2x1)

    button_game2x2 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game2x2.place(x=140, y=142)
    buttons.append(button_game2x2)
    row2.append(button_game2x2)

    button_game2x3 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game2x3.place(x=140, y=184)
    buttons.append(button_game2x3)
    row3.append(button_game2x3)

    button_game2x4 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x4.place(x=140, y=226)
    buttons.append(button_game2x4)
    row4.append(button_game2x4)

    button_game2x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x5.place(x=140, y=268)
    buttons.append(button_game2x5)
    row5.append(button_game2x5)

    button_game2x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x6.place(x=140, y=310)
    buttons.append(button_game2x6)
    row6.append(button_game2x6)

    button_game2x7 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game2x7.place(x=140, y=352)
    buttons.append(button_game2x7)
    row7.append(button_game2x7)

    button_game2x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x8.place(x=140, y=394)
    buttons.append(button_game2x8)
    row8.append(button_game2x8)

    button_game2x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game2x9.place(x=140, y=436)
    buttons.append(button_game2x9)
    row9.append(button_game2x9)

    button_game2x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game2x10.place(x=140, y=478)
    buttons.append(button_game2x10)
    row10.append(button_game2x10)

    # endregion

    # region COLUMNA 3
    button_game3x1 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game3x1.place(x=180, y=100)
    buttons.append(button_game3x1)
    row1.append(button_game3x1)

    button_game3x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x2.place(x=180, y=142)
    buttons.append(button_game3x2)
    row2.append(button_game3x2)

    button_game3x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x3.place(x=180, y=184)
    buttons.append(button_game3x3)
    row3.append(button_game3x3)

    button_game3x4 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x4.place(x=180, y=226)
    buttons.append(button_game3x4)
    row4.append(button_game3x4)

    button_game3x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x5.place(x=180, y=268)
    buttons.append(button_game3x5)
    row5.append(button_game3x5)

    button_game3x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x6.place(x=180, y=310)
    buttons.append(button_game3x6)
    row6.append(button_game3x6)

    button_game3x7 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game3x7.place(x=180, y=352)
    buttons.append(button_game3x7)
    row7.append(button_game3x7)

    button_game3x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x8.place(x=180, y=394)
    buttons.append(button_game3x8)
    row8.append(button_game3x8)

    button_game3x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game3x9.place(x=180, y=436)
    buttons.append(button_game3x9)
    row9.append(button_game3x9)

    button_game3x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game3x10.place(x=180, y=478)
    buttons.append(button_game3x10)
    row10.append(button_game3x10)

    # endregion

    # region COLUMNA 4
    button_game4x1 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game4x1.place(x=220, y=100)
    buttons.append(button_game4x1)
    row1.append(button_game4x1)

    button_game4x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x2.place(x=220, y=142)
    buttons.append(button_game4x2)
    row2.append(button_game4x2)

    button_game4x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x3.place(x=220, y=184)
    buttons.append(button_game4x3)
    row3.append(button_game4x3)

    button_game4x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game4x4.place(x=220, y=226)
    buttons.append(button_game4x4)
    row4.append(button_game4x4)

    button_game4x5 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game4x5.place(x=220, y=268)
    buttons.append(button_game4x5)
    row5.append(button_game4x5)

    button_game4x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x6.place(x=220, y=310)
    buttons.append(button_game4x6)
    row6.append(button_game4x6)

    button_game4x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x7.place(x=220, y=352)
    buttons.append(button_game4x7)
    row7.append(button_game4x7)

    button_game4x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x8.place(x=220, y=394)
    buttons.append(button_game4x8)
    row8.append(button_game4x8)

    button_game4x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game4x9.place(x=220, y=436)
    buttons.append(button_game4x9)
    row9.append(button_game4x9)

    button_game4x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game4x10.place(x=220, y=478)
    buttons.append(button_game4x10)
    row10.append(button_game4x10)

    # endregion

    # region COLUMNA 5
    button_game5x1 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x1.place(x=260, y=100)
    buttons.append(button_game5x1)
    row1.append(button_game5x1)

    button_game5x2 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game5x2.place(x=260, y=142)
    buttons.append(button_game5x2)
    row2.append(button_game5x2)

    button_game5x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x3.place(x=260, y=184)
    buttons.append(button_game5x3)
    row3.append(button_game5x3)

    button_game5x4 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x4.place(x=260, y=226)
    buttons.append(button_game5x4)
    row4.append(button_game5x4)

    button_game5x5 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game5x5.place(x=260, y=268)
    buttons.append(button_game5x5)
    row5.append(button_game5x5)

    button_game5x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x6.place(x=260, y=310)
    buttons.append(button_game5x6)
    row6.append(button_game5x6)

    button_game5x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x7.place(x=260, y=352)
    buttons.append(button_game5x7)
    row7.append(button_game5x7)

    button_game5x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x8.place(x=260, y=394)
    buttons.append(button_game5x8)
    row8.append(button_game5x8)

    button_game5x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game5x9.place(x=260, y=436)
    buttons.append(button_game5x9)
    row9.append(button_game5x9)

    button_game5x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game5x10.place(x=260, y=478)
    buttons.append(button_game5x10)
    row10.append(button_game5x10)

    # endregion

    # region COLUMNA 6

    button_game6x1 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x1.place(x=300, y=100)
    buttons.append(button_game6x1)
    row1.append(button_game6x1)

    button_game6x2 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game6x2.place(x=300, y=142)
    buttons.append(button_game6x2)
    row2.append(button_game6x2)

    button_game6x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x3.place(x=300, y=184)
    buttons.append(button_game6x3)
    row3.append(button_game6x3)

    button_game6x4 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x4.place(x=300, y=226)
    buttons.append(button_game6x4)
    row4.append(button_game6x4)

    button_game6x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x5.place(x=300, y=268)
    buttons.append(button_game6x5)
    row5.append(button_game6x5)

    button_game6x6 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game6x6.place(x=300, y=310)
    buttons.append(button_game6x6)
    row6.append(button_game6x6)

    button_game6x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x7.place(x=300, y=352)
    buttons.append(button_game6x7)
    row7.append(button_game6x7)

    button_game6x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game6x8.place(x=300, y=394)
    buttons.append(button_game6x8)
    row8.append(button_game6x8)

    button_game6x9 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game6x9.place(x=300, y=436)
    buttons.append(button_game6x9)
    row9.append(button_game6x9)

    button_game6x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game6x10.place(x=300, y=478)
    buttons.append(button_game6x10)
    row10.append(button_game6x10)

    # endregion

    # region COLUMNA 7

    button_game7x1 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x1.place(x=340, y=100)
    buttons.append(button_game7x1)
    row1.append(button_game7x1)

    button_game7x2 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game7x2.place(x=340, y=142)
    buttons.append(button_game7x2)
    row2.append(button_game7x2)

    button_game7x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x3.place(x=340, y=184)
    buttons.append(button_game7x3)
    row3.append(button_game7x3)

    button_game7x4 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x4.place(x=340, y=226)
    buttons.append(button_game7x4)
    row4.append(button_game7x4)

    button_game7x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x5.place(x=340, y=268)
    buttons.append(button_game7x5)
    row5.append(button_game7x5)

    button_game7x6 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game7x6.place(x=340, y=310)
    buttons.append(button_game7x6)
    row6.append(button_game7x6)

    button_game7x7 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game7x7.place(x=340, y=352)
    buttons.append(button_game7x7)
    row7.append(button_game7x7)

    button_game7x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x8.place(x=340, y=394)
    buttons.append(button_game7x8)
    row8.append(button_game7x8)

    button_game7x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game7x9.place(x=340, y=436)
    buttons.append(button_game7x9)
    row9.append(button_game7x9)

    button_game7x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game7x10.place(x=340, y=478)
    buttons.append(button_game7x10)
    row10.append(button_game7x10)

    # endregion

    # region COLUMNA 8

    button_game8x1 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game8x1.place(x=380, y=100)
    buttons.append(button_game8x1)
    row1.append(button_game8x1)

    button_game8x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x2.place(x=380, y=142)
    buttons.append(button_game8x2)
    row2.append(button_game8x2)

    button_game8x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x3.place(x=380, y=184)
    buttons.append(button_game8x3)
    row3.append(button_game8x3)

    button_game8x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game8x4.place(x=380, y=226)
    buttons.append(button_game8x4)
    row4.append(button_game8x4)

    button_game8x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x5.place(x=380, y=268)
    buttons.append(button_game8x5)
    row5.append(button_game8x5)

    button_game8x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x6.place(x=380, y=310)
    buttons.append(button_game8x6)
    row6.append(button_game8x6)

    button_game8x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x7.place(x=380, y=352)
    buttons.append(button_game8x7)
    row7.append(button_game8x7)

    button_game8x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x8.place(x=380, y=394)
    buttons.append(button_game8x8)
    row8.append(button_game8x8)

    button_game8x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game8x9.place(x=380, y=436)
    buttons.append(button_game8x9)
    row9.append(button_game8x9)

    button_game8x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game8x10.place(x=380, y=478)
    buttons.append(button_game8x10)
    row10.append(button_game8x10)

    # endregion

    # region COLUMNA 9
    button_game9x1 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game9x1.place(x=420, y=100)
    buttons.append(button_game9x1)
    row1.append(button_game9x1)

    button_game9x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x2.place(x=420, y=142)
    buttons.append(button_game9x2)
    row2.append(button_game9x2)

    button_game9x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x3.place(x=420, y=184)
    buttons.append(button_game9x3)
    row3.append(button_game9x3)

    button_game9x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game9x4.place(x=420, y=226)
    buttons.append(button_game9x4)
    row4.append(button_game9x4)

    button_game9x5 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x5.place(x=420, y=268)
    buttons.append(button_game9x5)
    row5.append(button_game9x5)

    button_game9x6 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x6.place(x=420, y=310)
    buttons.append(button_game9x6)
    row6.append(button_game9x6)

    button_game9x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x7.place(x=420, y=352)
    buttons.append(button_game9x7)
    row7.append(button_game9x7)

    button_game9x8 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x8.place(x=420, y=394)
    buttons.append(button_game9x8)
    row8.append(button_game9x8)

    button_game9x9 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game9x9.place(x=420, y=436)
    buttons.append(button_game9x9)
    row9.append(button_game9x9)

    button_game9x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game9x10.place(x=420, y=478)
    buttons.append(button_game9x10)
    row10.append(button_game9x10)

    # endregion

    # region COLUMNA 10

    button_game10x1 = Button(window, width=4, bg="black", state="disabled", height=2, text="")
    button_game10x1.place(x=460, y=100)
    buttons.append(button_game10x1)
    row1.append(button_game10x1)

    button_game10x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game10x2.place(x=460, y=142)
    buttons.append(button_game10x2)
    row2.append(button_game10x2)

    button_game10x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game10x3.place(x=460, y=184)
    buttons.append(button_game10x3)
    row3.append(button_game10x3)

    button_game10x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x4.place(x=460, y=226)
    buttons.append(button_game10x4)
    row4.append(button_game10x4)

    button_game10x5 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x5.place(x=460, y=268)
    buttons.append(button_game10x5)
    row5.append(button_game10x5)

    button_game10x6 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x6.place(x=460, y=310)
    buttons.append(button_game10x6)
    row6.append(button_game10x6)

    button_game10x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game10x7.place(x=460, y=352)
    buttons.append(button_game10x7)
    row7.append(button_game10x7)

    button_game10x8 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x8.place(x=460, y=394)
    buttons.append(button_game10x8)
    row8.append(button_game10x8)

    button_game10x9 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x9.place(x=460, y=436)
    buttons.append(button_game10x9)
    row9.append(button_game10x9)

    button_game10x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game10x10.place(x=460, y=478)
    buttons.append(button_game10x10)
    row10.append(button_game10x10)

    # endregion

    # region COLUMNA 11

    button_game11x1 = Button(window, width=4, bg="black", state="disabled", height=2, text="")
    button_game11x1.place(x=500, y=100)
    buttons.append(button_game11x1)
    row1.append(button_game11x1)

    button_game11x2 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game11x2.place(x=500, y=142)
    buttons.append(button_game11x2)
    row2.append(button_game11x2)

    button_game11x3 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game11x3.place(x=500, y=184)
    buttons.append(button_game11x3)
    row3.append(button_game11x3)

    button_game11x4 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x4.place(x=500, y=226)
    buttons.append(button_game11x4)
    row4.append(button_game11x4)

    button_game11x5 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x5.place(x=500, y=268)
    buttons.append(button_game11x5)
    row5.append(button_game11x5)

    button_game11x6 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x6.place(x=500, y=310)
    buttons.append(button_game11x6)
    row6.append(button_game11x6)

    button_game11x7 = Button(window, width=4, height=2, bg="black", state="disabled")
    button_game11x7.place(x=500, y=352)
    buttons.append(button_game11x7)
    row7.append(button_game11x7)

    button_game11x8 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x8.place(x=500, y=394)
    buttons.append(button_game11x8)
    row8.append(button_game11x8)

    button_game11x9 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x9.place(x=500, y=436)
    buttons.append(button_game11x9)
    row9.append(button_game11x9)

    button_game11x10 = Button(window, width=4, height=2, bg="black", state="disabled", text="", fg="white")
    button_game11x10.place(x=500, y=478)
    buttons.append(button_game11x10)
    row10.append(button_game11x10)

    # endregion

    # endregion

    #region creating matrix
    generalList = []
    generalList.append(row1)
    generalList.append(row2)
    generalList.append(row3)
    generalList.append(row4)
    generalList.append(row5)
    generalList.append(row6)
    generalList.append(row7)
    generalList.append(row8)
    generalList.append(row9)
    generalList.append(row10)
    #endregion

    #region main buttons & labels
    timeLabel = Button(window, width=45, height=1, text='Tiempo de Ejecución ->', font="Courier", fg="black",state="disabled")
    timeLabel.place(x=25, y=700)

    solutionLabel = Button(window, width=19, height=1, text='Solución', font="Courier", fg="black",state="disabled")
    solutionLabel.place(x=200, y=775)

    solutionNumbers = Button(window, width=57, height=1, font="Courier", fg="black",state="disabled")
    solutionNumbers.place(x=25, y=825)

    spin = Spinbox(window, from_=0, to=9, width=5, font="arial")
    spin.place(x=290, y=575)

    button0 = Button(window, width=12, height=4, bg='red', text='Fuerza \nBruta', font="Courier", fg="white",activebackground='red3', command=lambda: paint_matrix_gui(generalList, int(spin.get()),0,timeLabel, solutionNumbers))
    button0.place(x=100, y=550)

    button1 = Button(window, width=12, height=4, bg='red', text='Backtracking', font="Courier", fg="white",activebackground='red4', command=lambda: paint_matrix_gui(generalList, int(spin.get()),1,timeLabel,solutionNumbers))
    button1.place(x=408, y=550)

    #endregion

    window.mainloop()



main_window()
