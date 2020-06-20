# Side Project – Just for fun.

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def empty(board):
    for a in range(len(board)):
        for b in range(len(board[0])):
            if board[a][b] == 0:
                return (a, b)

def game_board(board):
    for a in range(len(board)):
        if a % 3 == 0 and a != 0:
            print("===============================")
        for b in range(len(board[0])):
            if b % 3 == 0:
                print(" || ", end="")

            if b == 8:
                print(board[a][b], end="\n")
            else:
                print(str(board[a][b]) + "  ", end="")

def validity(board, number, position):
    for a in range(len(board[0])):
        if board[position[0]][a] == number and position[1] != a:
            return False

    for a in range(len(board)):
        if board[a][position[1]] == number and position[1] != a:
            return False

    x_coordinate = position[1] // 3
    y_coordinate = position[0] // 3

    for i in range(x_coordinate * 3, x_coordinate * 3 + 3):
        for j in range(y_coordinate * 3, y_coordinate * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True

def solve_board(board):

    look_for_board = empty(board)

    if not look_for_board:
        return True
    else :
        row, column = look_for_board

    for a in range(1, 10):
        if validity(board, a, (row, column)):
            board[row][column] = a

            if solve_board(board):
                return True

            board[row][column] = 0
    return False



game_board(board)
solve_board(board)
print("==============================")
game_board(board)