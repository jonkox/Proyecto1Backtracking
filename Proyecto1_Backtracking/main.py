def makeMatrix(n):
    matrix = []

    for i in range(n+1):
        matrix.append([0])

        for j in range(n+1):
            matrix[i].append(0)

    return matrix


def printMatrix(matrix):
    for i in matrix:
        for j in i:
            print("\t", j, end=" ")
        print()

def getNumberOfTokens(matrix):
    rows = len(matrix)
    colums = len(matrix[0])

    return int((rows*colums)/2)

matrix = makeMatrix(2)
print(matrix)
printMatrix(matrix)
print(getNumberOfTokens(matrix))
