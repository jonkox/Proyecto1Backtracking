
#IMPORTACIONES----------------------------------------------------------------------------------------------------------
from tkinter import messagebox
from tkinter import Tk, Label, Button, Spinbox
from random import randint

import main
from main import create_puzzle
#-----------------------------------------------------------------------------------------------------------------------
function = 0


"""Funcion cambio button: esta funcion tiene como tarea hacer que el button seleccionado para asiganarle un valor para hacer una jugada se cambie, si se le asigna un valor vacio se retorna un error."""
def cambio_button(button, jugada):
    global texto, lista_jugadas, button_actual, borrar, jugadas_de_partida

    # Con esta condicional se valida si lo que se quiere hacer es borrar una casilla o no
    if borrar == True:
        if validar_texto(button) == False:
            messagebox.showerror(title="ERROR", message="LA CASILLA NO SE PUEDE ELIMINAR")
            borrar = False

        else:
            button.configure(text="")
            borrar = False
        return




    jugada = []
    jugada.append(button)
    jugada.append(button["text"])
    jugada.append(texto)
    if jugada not in lista_jugadas:
        lista_jugadas.append(jugada)




    #Valida que se haya seleccionado un button del panel antes de configurar el button
    if texto == '':
        ''' MessageBox
        -showinfo(), showerror(), showwarning(), askquestion(), askcancel(), askyesno(), askretrycancel()'''
        messagebox.showerror(message='Debe seleccionar un button del panel de seleccion')
    else:
        button.configure(text=texto)
        button_actual.insert(0,button)

    #validar_sumas(jugadas_de_partida)


"""Funcion validar texto: esta funcion valida el un button contiene texto o no y retorna un valor booleano para entender"""
def validar_texto(button):
    if button["text"] == "":
        return False
    return True


def changeColors(buttonsList,solution):

    colorList = ["white", "red", "yellow","blue","green"]
    row = 0
    column = 0

    totalRows = 10
    totalColumns = 11

    for i in solution:
        myColor = randint(0,4)

        if i == "0":
            for j in range(2):
                if not validar_texto(buttonsList[row][column]):
                    buttonsList[row][column].configure(bg=colorList[myColor],text="0")
                    column += 1
                    if column >= 11:
                        column = 0


        if i == "1":
            for j in range(2):
                if not validar_texto(buttonsList[row][column]):
                    buttonsList[row][column].configure(bg=colorList[myColor],text="1")
                    row += 1

            row -= 1

def calculate_centered_start(length):
    i = (7 - length) // 2

    # i = j
    # i = 10 - length = 11-1 - length = 11 - length - 1 = 11 - (length +1)
    # If you think it the vertical relationship has to be always kept, example (0, 0)

    return i, i

def paint_matrix_gui(buttons, n,function):
    colorList = ["white", "red", "yellow", "blue", "green","CadetBlue1","DarkGoldenrod4", "DarkOrchid4", "DeepPink2","brown2",
                 "LightPink1", "SteelBlue4", "cornsilk2", "dark slate gray", "indian red", "violet red", "medium sea green"]

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
        possible_solution = main.brute_strength_solution(num_matrix)
        randomSolution = randint(0, len(possible_solution)-1)
        possible_solution = possible_solution[randomSolution]

        #Set horizontal and vertical values
        horizontal_length = len(num_matrix[0])
        vertical_length = len(num_matrix)


    if function == 1:

        matrix = False
        while matrix == False:
            num_matrix = create_puzzle(n)
            if num_matrix != False:
                matrix = True

        possible_solution = main.backtracking_solution(num_matrix)
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

"""Funcion ventana de game: esta funcion es la funcion mas importante del programa puesto que es la funcion que crea el tablero y demas cosas importantes que se deben mostrar
para poder jugar al game"""
def ventana_de_game():

    #region creacion y configuracion de la ventana
    ventana = Tk()

    # titulo
    ventana.title("DOMINOSA")

    # se le da tamaño a la ventana principal
    ventana.geometry("600x800")
    # color a la ventana principal
    ventana.configure(bg="gray1")

    etiqueta = Label(ventana, text="DOMINOSA", bg="red",fg= "white", padx=88, pady=5, font="Helvetica 25",relief="solid").place(x=150, y=5)

    ventana.resizable(False, False)

    #endregion

    # region FILAS
    buttos = []
    fila1 = []
    fila2 = []
    fila3 = []
    fila4 = []
    fila5 = []
    fila6 = []
    fila7 = []
    fila8 = []
    fila9 = []
    fila10 = []

    # endregion

    #region columnas
    # region COLUMNA 1

    button_game1x1 = Button(ventana, width=4, bg="black", state="disabled", height=2, text="",command=lambda: cambio_button(button_game1x1, texto))
    button_game1x1.place(x=100, y=100)
    buttos.append(button_game1x1)
    fila1.append(button_game1x1)

    button_game1x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",command=lambda: cambio_button(button_game1x2, texto))
    button_game1x2.place(x=100, y=142)
    buttos.append(button_game1x2)
    fila2.append(button_game1x2)

    button_game1x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",command=lambda: cambio_button(button_game1x3, texto))
    button_game1x3.place(x=100, y=184)
    buttos.append(button_game1x3)
    fila3.append(button_game1x3)

    button_game1x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            command=lambda: cambio_button(button_game1x4, texto))
    button_game1x4.place(x=100, y=226)
    buttos.append(button_game1x4)
    fila4.append(button_game1x4)

    button_game1x5 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            command=lambda: cambio_button(button_game1x5, texto))
    button_game1x5.place(x=100, y=268)
    buttos.append(button_game1x5)
    fila5.append(button_game1x5)

    button_game1x6 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            command=lambda: cambio_button(button_game1x6, texto))
    button_game1x6.place(x=100, y=310)
    buttos.append(button_game1x6)
    fila6.append(button_game1x6)

    button_game1x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game1x7, texto))
    button_game1x7.place(x=100, y=352)
    buttos.append(button_game1x7)
    fila7.append(button_game1x7)

    button_game1x8 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            command=lambda: cambio_button(button_game1x8, texto))
    button_game1x8.place(x=100, y=394)
    buttos.append(button_game1x8)
    fila8.append(button_game1x8)

    button_game1x9 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            command=lambda: cambio_button(button_game1x9, texto))
    button_game1x9.place(x=100, y=436)
    buttos.append(button_game1x9)
    fila9.append(button_game1x9)

    button_game1x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game1x10.place(x=100, y=478)
    buttos.append(button_game1x10)
    fila10.append(button_game1x10)

    # endregion

    # region COLUMNA 2
    button_game2x1 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x1, texto))
    button_game2x1.place(x=140, y=100)
    buttos.append(button_game2x1)
    fila1.append(button_game2x1)

    button_game2x2 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game2x2, texto))
    button_game2x2.place(x=140, y=142)
    buttos.append(button_game2x2)
    fila2.append(button_game2x2)

    button_game2x3 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game2x3, texto))
    button_game2x3.place(x=140, y=184)
    buttos.append(button_game2x3)
    fila3.append(button_game2x3)

    button_game2x4 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x4, texto))
    button_game2x4.place(x=140, y=226)
    buttos.append(button_game2x4)
    fila4.append(button_game2x4)

    button_game2x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x5, texto))
    button_game2x5.place(x=140, y=268)
    buttos.append(button_game2x5)
    fila5.append(button_game2x5)

    button_game2x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x6, texto))
    button_game2x6.place(x=140, y=310)
    buttos.append(button_game2x6)
    fila6.append(button_game2x6)

    button_game2x7 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game2x7, texto))
    button_game2x7.place(x=140, y=352)
    buttos.append(button_game2x7)
    fila7.append(button_game2x7)

    button_game2x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x8, texto))
    button_game2x8.place(x=140, y=394)
    buttos.append(button_game2x8)
    fila8.append(button_game2x8)

    button_game2x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game2x9, texto))
    button_game2x9.place(x=140, y=436)
    buttos.append(button_game2x9)
    fila9.append(button_game2x9)

    button_game2x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game2x10.place(x=140, y=478)
    buttos.append(button_game2x10)
    fila10.append(button_game2x10)

    # endregion

    # region COLUMNA 3
    button_game3x1 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game3x1, texto))
    button_game3x1.place(x=180, y=100)
    buttos.append(button_game3x1)
    fila1.append(button_game3x1)

    button_game3x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x2, texto))
    button_game3x2.place(x=180, y=142)
    buttos.append(button_game3x2)
    fila2.append(button_game3x2)

    button_game3x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x3, texto))
    button_game3x3.place(x=180, y=184)
    buttos.append(button_game3x3)
    fila3.append(button_game3x3)

    button_game3x4 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x4, texto))
    button_game3x4.place(x=180, y=226)
    buttos.append(button_game3x4)
    fila4.append(button_game3x4)

    button_game3x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x5, texto))
    button_game3x5.place(x=180, y=268)
    buttos.append(button_game3x5)
    fila5.append(button_game3x5)

    button_game3x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x6, texto))
    button_game3x6.place(x=180, y=310)
    buttos.append(button_game3x6)
    fila6.append(button_game3x6)

    button_game3x7 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game3x7, texto))
    button_game3x7.place(x=180, y=352)
    buttos.append(button_game3x7)
    fila7.append(button_game3x7)

    button_game3x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x8, texto))
    button_game3x8.place(x=180, y=394)
    buttos.append(button_game3x8)
    fila8.append(button_game3x8)

    button_game3x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game3x9, texto))
    button_game3x9.place(x=180, y=436)
    buttos.append(button_game3x9)
    fila9.append(button_game3x9)

    button_game3x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game3x10.place(x=180, y=478)
    buttos.append(button_game3x10)
    fila10.append(button_game3x10)

    # endregion

    # region COLUMNA 4
    button_game4x1 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game4x1, texto))
    button_game4x1.place(x=220, y=100)
    buttos.append(button_game4x1)
    fila1.append(button_game4x1)

    button_game4x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x2, texto))
    button_game4x2.place(x=220, y=142)
    buttos.append(button_game4x2)
    fila2.append(button_game4x2)

    button_game4x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x3, texto))
    button_game4x3.place(x=220, y=184)
    buttos.append(button_game4x3)
    fila3.append(button_game4x3)

    button_game4x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game4x4, texto))
    button_game4x4.place(x=220, y=226)
    buttos.append(button_game4x4)
    fila4.append(button_game4x4)

    button_game4x5 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game4x5, texto))
    button_game4x5.place(x=220, y=268)
    buttos.append(button_game4x5)
    fila5.append(button_game4x5)

    button_game4x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x6, texto))
    button_game4x6.place(x=220, y=310)
    buttos.append(button_game4x6)
    fila6.append(button_game4x6)

    button_game4x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x7, texto))
    button_game4x7.place(x=220, y=352)
    buttos.append(button_game4x7)
    fila7.append(button_game4x7)

    button_game4x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x8, texto))
    button_game4x8.place(x=220, y=394)
    buttos.append(button_game4x8)
    fila8.append(button_game4x8)

    button_game4x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game4x9, texto))
    button_game4x9.place(x=220, y=436)
    buttos.append(button_game4x9)
    fila9.append(button_game4x9)

    button_game4x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game4x10.place(x=220, y=478)
    buttos.append(button_game4x10)
    fila10.append(button_game4x10)

    # endregion

    # region COLUMNA 5
    button_game5x1 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x1, texto))
    button_game5x1.place(x=260, y=100)
    buttos.append(button_game5x1)
    fila1.append(button_game5x1)

    button_game5x2 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game5x2, texto))
    button_game5x2.place(x=260, y=142)
    buttos.append(button_game5x2)
    fila2.append(button_game5x2)

    button_game5x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x3, texto))
    button_game5x3.place(x=260, y=184)
    buttos.append(button_game5x3)
    fila3.append(button_game5x3)

    button_game5x4 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x4, texto))
    button_game5x4.place(x=260, y=226)
    buttos.append(button_game5x4)
    fila4.append(button_game5x4)

    button_game5x5 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game5x5, texto))
    button_game5x5.place(x=260, y=268)
    buttos.append(button_game5x5)
    fila5.append(button_game5x5)

    button_game5x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x6, texto))
    button_game5x6.place(x=260, y=310)
    buttos.append(button_game5x6)
    fila6.append(button_game5x6)

    button_game5x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x7, texto))
    button_game5x7.place(x=260, y=352)
    buttos.append(button_game5x7)
    fila7.append(button_game5x7)

    button_game5x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x8, texto))
    button_game5x8.place(x=260, y=394)
    buttos.append(button_game5x8)
    fila8.append(button_game5x8)

    button_game5x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game5x9, texto))
    button_game5x9.place(x=260, y=436)
    buttos.append(button_game5x9)
    fila9.append(button_game5x9)

    button_game5x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game5x10.place(x=260, y=478)
    buttos.append(button_game5x10)
    fila10.append(button_game5x10)

    # endregion

    # region COLUMNA 6

    button_game6x1 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x1, texto))
    button_game6x1.place(x=300, y=100)
    buttos.append(button_game6x1)
    fila1.append(button_game6x1)

    button_game6x2 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game6x2, texto))
    button_game6x2.place(x=300, y=142)
    buttos.append(button_game6x2)
    fila2.append(button_game6x2)

    button_game6x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x3, texto))
    button_game6x3.place(x=300, y=184)
    buttos.append(button_game6x3)
    fila3.append(button_game6x3)

    button_game6x4 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x4, texto))
    button_game6x4.place(x=300, y=226)
    buttos.append(button_game6x4)
    fila4.append(button_game6x4)

    button_game6x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x5, texto))
    button_game6x5.place(x=300, y=268)
    buttos.append(button_game6x5)
    fila5.append(button_game6x5)

    button_game6x6 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game6x6, texto))
    button_game6x6.place(x=300, y=310)
    buttos.append(button_game6x6)
    fila6.append(button_game6x6)

    button_game6x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x7, texto))
    button_game6x7.place(x=300, y=352)
    buttos.append(button_game6x7)
    fila7.append(button_game6x7)

    button_game6x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game6x8, texto))
    button_game6x8.place(x=300, y=394)
    buttos.append(button_game6x8)
    fila8.append(button_game6x8)

    button_game6x9 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game6x9, texto))
    button_game6x9.place(x=300, y=436)
    buttos.append(button_game6x9)
    fila9.append(button_game6x9)

    button_game6x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game6x10.place(x=300, y=478)
    buttos.append(button_game6x10)
    fila10.append(button_game6x10)

    # endregion

    # region COLUMNA 7

    button_game7x1 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x1, texto))
    button_game7x1.place(x=340, y=100)
    buttos.append(button_game7x1)
    fila1.append(button_game7x1)

    button_game7x2 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game7x2, texto))
    button_game7x2.place(x=340, y=142)
    buttos.append(button_game7x2)
    fila2.append(button_game7x2)

    button_game7x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x3, texto))
    button_game7x3.place(x=340, y=184)
    buttos.append(button_game7x3)
    fila3.append(button_game7x3)

    button_game7x4 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x4, texto))
    button_game7x4.place(x=340, y=226)
    buttos.append(button_game7x4)
    fila4.append(button_game7x4)

    button_game7x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x5, texto))
    button_game7x5.place(x=340, y=268)
    buttos.append(button_game7x5)
    fila5.append(button_game7x5)

    button_game7x6 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game7x6, texto))
    button_game7x6.place(x=340, y=310)
    buttos.append(button_game7x6)
    fila6.append(button_game7x6)

    button_game7x7 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game7x7, texto))
    button_game7x7.place(x=340, y=352)
    buttos.append(button_game7x7)
    fila7.append(button_game7x7)

    button_game7x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x8, texto))
    button_game7x8.place(x=340, y=394)
    buttos.append(button_game7x8)
    fila8.append(button_game7x8)

    button_game7x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game7x9, texto))
    button_game7x9.place(x=340, y=436)
    buttos.append(button_game7x9)
    fila9.append(button_game7x9)

    button_game7x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game7x10.place(x=340, y=478)
    buttos.append(button_game7x10)
    fila10.append(button_game7x10)

    # endregion

    # region COLUMNA 8

    button_game8x1 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game8x1, texto))
    button_game8x1.place(x=380, y=100)
    buttos.append(button_game8x1)
    fila1.append(button_game8x1)

    button_game8x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x2, texto))
    button_game8x2.place(x=380, y=142)
    buttos.append(button_game8x2)
    fila2.append(button_game8x2)

    button_game8x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x3, texto))
    button_game8x3.place(x=380, y=184)
    buttos.append(button_game8x3)
    fila3.append(button_game8x3)

    button_game8x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game8x4, texto))
    button_game8x4.place(x=380, y=226)
    buttos.append(button_game8x4)
    fila4.append(button_game8x4)

    button_game8x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x5, texto))
    button_game8x5.place(x=380, y=268)
    buttos.append(button_game8x5)
    fila5.append(button_game8x5)

    button_game8x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x6, texto))
    button_game8x6.place(x=380, y=310)
    buttos.append(button_game8x6)
    fila6.append(button_game8x6)

    button_game8x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x7, texto))
    button_game8x7.place(x=380, y=352)
    buttos.append(button_game8x7)
    fila7.append(button_game8x7)

    button_game8x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x8, texto))
    button_game8x8.place(x=380, y=394)
    buttos.append(button_game8x8)
    fila8.append(button_game8x8)

    button_game8x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game8x9, texto))
    button_game8x9.place(x=380, y=436)
    buttos.append(button_game8x9)
    fila9.append(button_game8x9)

    button_game8x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game8x10.place(x=380, y=478)
    buttos.append(button_game8x10)
    fila10.append(button_game8x10)

    # endregion

    # region COLUMNA 9
    button_game9x1 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game9x1, texto))
    button_game9x1.place(x=420, y=100)
    buttos.append(button_game9x1)
    fila1.append(button_game9x1)

    button_game9x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x2, texto))
    button_game9x2.place(x=420, y=142)
    buttos.append(button_game9x2)
    fila2.append(button_game9x2)

    button_game9x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x3, texto))
    button_game9x3.place(x=420, y=184)
    buttos.append(button_game9x3)
    fila3.append(button_game9x3)

    button_game9x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                            justify="right", command=lambda: cambio_button(button_game9x4, texto))
    button_game9x4.place(x=420, y=226)
    buttos.append(button_game9x4)
    fila4.append(button_game9x4)

    button_game9x5 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x5, texto))
    button_game9x5.place(x=420, y=268)
    buttos.append(button_game9x5)
    fila5.append(button_game9x5)

    button_game9x6 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x6, texto))
    button_game9x6.place(x=420, y=310)
    buttos.append(button_game9x6)
    fila6.append(button_game9x6)

    button_game9x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x7, texto))
    button_game9x7.place(x=420, y=352)
    buttos.append(button_game9x7)
    fila7.append(button_game9x7)

    button_game9x8 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x8, texto))
    button_game9x8.place(x=420, y=394)
    buttos.append(button_game9x8)
    fila8.append(button_game9x8)

    button_game9x9 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                            command=lambda: cambio_button(button_game9x9, texto))
    button_game9x9.place(x=420, y=436)
    buttos.append(button_game9x9)
    fila9.append(button_game9x9)

    button_game9x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game9x10.place(x=420, y=478)
    buttos.append(button_game9x10)
    fila10.append(button_game9x10)

    # endregion

    # region COLUMNA 10

    button_game10x1 = Button(ventana, width=4, bg="black", state="disabled", height=2, text="",
                             command=lambda: cambio_button(button_game1x1, texto))
    button_game10x1.place(x=460, y=100)
    buttos.append(button_game10x1)
    fila1.append(button_game10x1)

    button_game10x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game1x2, texto))
    button_game10x2.place(x=460, y=142)
    buttos.append(button_game10x2)
    fila2.append(button_game10x2)

    button_game10x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game1x3, texto))
    button_game10x3.place(x=460, y=184)
    buttos.append(button_game10x3)
    fila3.append(button_game10x3)

    button_game10x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game1x4, texto))
    button_game10x4.place(x=460, y=226)
    buttos.append(button_game10x4)
    fila4.append(button_game10x4)

    button_game10x5 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game1x5, texto))
    button_game10x5.place(x=460, y=268)
    buttos.append(button_game10x5)
    fila5.append(button_game10x5)

    button_game10x6 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game1x6, texto))
    button_game10x6.place(x=460, y=310)
    buttos.append(button_game10x6)
    fila6.append(button_game10x6)

    button_game10x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game1x7, texto))
    button_game10x7.place(x=460, y=352)
    buttos.append(button_game10x7)
    fila7.append(button_game10x7)

    button_game10x8 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game1x8, texto))
    button_game10x8.place(x=460, y=394)
    buttos.append(button_game10x8)
    fila8.append(button_game10x8)

    button_game10x9 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game1x9, texto))
    button_game10x9.place(x=460, y=436)
    buttos.append(button_game10x9)
    fila9.append(button_game10x9)

    button_game10x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                              command=lambda: cambio_button(button_game11x9, texto))
    button_game10x10.place(x=460, y=478)
    buttos.append(button_game10x10)
    fila10.append(button_game10x10)

    # endregion

    # region COLUMNA 11

    button_game11x1 = Button(ventana, width=4, bg="black", state="disabled", height=2, text="",
                             command=lambda: cambio_button(button_game11x1, texto))
    button_game11x1.place(x=500, y=100)
    buttos.append(button_game11x1)
    fila1.append(button_game11x1)

    button_game11x2 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game11x2, texto))
    button_game11x2.place(x=500, y=142)
    buttos.append(button_game11x2)
    fila2.append(button_game11x2)

    button_game11x3 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game11x3, texto))
    button_game11x3.place(x=500, y=184)
    buttos.append(button_game11x3)
    fila3.append(button_game11x3)

    button_game11x4 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x4, texto))
    button_game11x4.place(x=500, y=226)
    buttos.append(button_game11x4)
    fila4.append(button_game11x4)

    button_game11x5 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x5, texto))
    button_game11x5.place(x=500, y=268)
    buttos.append(button_game11x5)
    fila5.append(button_game11x5)

    button_game11x6 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x6, texto))
    button_game11x6.place(x=500, y=310)
    buttos.append(button_game11x6)
    fila6.append(button_game11x6)

    button_game11x7 = Button(ventana, width=4, height=2, bg="black", state="disabled",
                             command=lambda: cambio_button(button_game11x7, texto))
    button_game11x7.place(x=500, y=352)
    buttos.append(button_game11x7)
    fila7.append(button_game11x7)

    button_game11x8 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x8, texto))
    button_game11x8.place(x=500, y=394)
    buttos.append(button_game11x8)
    fila8.append(button_game11x8)

    button_game11x9 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                             command=lambda: cambio_button(button_game11x9, texto))
    button_game11x9.place(x=500, y=436)
    buttos.append(button_game11x9)
    fila9.append(button_game11x9)

    button_game11x10 = Button(ventana, width=4, height=2, bg="black", state="disabled", text="", fg="white",
                              command=lambda: cambio_button(button_game11x9, texto))
    button_game11x10.place(x=500, y=478)
    buttos.append(button_game11x10)
    fila10.append(button_game11x10)

    # endregion

    # endregion

    generalList = []
    generalList.append(fila1)
    generalList.append(fila2)
    generalList.append(fila3)
    generalList.append(fila4)
    generalList.append(fila5)
    generalList.append(fila6)
    generalList.append(fila7)
    generalList.append(fila8)
    generalList.append(fila9)
    generalList.append(fila10)

    spin = Spinbox(ventana, from_=1, to=9, width=5, font="arial")
    spin.place(x=275, y=600)

    button0 = Button(ventana, width=12, height=4, bg='red', text='Fuerza \nBruta', font="Courier", fg="white",activebackground='red3', command=lambda: paint_matrix_gui(generalList, int(spin.get()),0))
    button0.place(x=100, y=600)

    button1 = Button(ventana, width=12, height=4, bg='red', text='Backtracking', font="Courier", fg="white",activebackground='red4', command=lambda: paint_matrix_gui(generalList, int(spin.get()),1))
    button1.place(x=375, y=600)



    ventana.mainloop()



ventana_de_game()
