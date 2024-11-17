CHOICES: set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def solveSudoku(matrix: list[list[int]]) -> list[list[int]]:
    rowList, columnList, cellList = populateRowCol(matrix)
    return sudokuHelper(matrix, rowList, columnList, cellList, 0, 0)

def populateRowCol(matrix: list[list[int]]) -> tuple[list[set], list[set], list[list[set[int]]]]:
    rowList: list[set[int]] = [CHOICES.copy() for _ in range(9)]
    columnList: list[set[int]] = [CHOICES.copy() for _ in range(9)]
    cellList: list[list[set[int]]] = [[CHOICES.copy() for _ in range(3)] for _ in range(3)]
                
    for x in range(9):
        for y in range(9):
            if matrix[x][y] == 0: continue
            cellX = int(x/3)
            cellY = int(y/3)
            current: int = int(matrix[x][y]) # without int() wrapping matrix, its a str.
            if current in rowList[x] and current in columnList[y] and current in cellList[cellX][cellY]:
                rowList[x].remove(current)
                columnList[y].remove(current)
                cellList[cellX][cellY].remove(current)
            else:
                raise Exception(f"Invalid board configuration! x = {x} y = {y}")
    return rowList, columnList, cellList


def sudokuHelper(matrix: list[list[int]], rowList: list[set], columnList: list[set], cellList: list[list[set[int]]],
                  x: int, y: int) -> list[list[int]]:
    if y == 9: return matrix
    nextX = x + 1 if x < 8 else 0 
    nextY = y if x < 8 else y + 1
    if matrix[x][y] != 0: return sudokuHelper(matrix, rowList, columnList, cellList, nextX, nextY)
    for choice in CHOICES:
        cellX = int(x/3)
        cellY = int(y/3)
        if choice in rowList[x] and choice in columnList[y] and choice in cellList[cellX][cellY]:
            rowList[x].remove(choice)
            columnList[y].remove(choice)
            cellList[cellX][cellY].remove(choice)
            matrix[x][y] = choice
            temp = sudokuHelper(matrix, rowList, columnList, cellList, nextX, nextY)
            if temp is not None: return temp
            rowList[x].add(choice)
            columnList[y].add(choice)
            cellList[cellX][cellY].add(choice)
            matrix[x][y] = 0                
    return None