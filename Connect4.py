from copy import deepcopy
import time

def printBoard(board):
    for i in range(7):
        print(i,end=' ')
    print()
    for row in board:
        for i in row:
            print(i,end=' ')
        print()

xends = {-1 : -1, 1 : 7}
yends = {-1 : -1, 1 : 6}


def isWin(board, x, y, player):
    directionPairs = [(1,0),(0,1),(1,1),(-1,1)]
    for dx,dy in directionPairs:
        firstDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x + dx, xends[dx], dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y + dy, yends[dy], dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                firstDirection+=1
            else:
                break
        secondDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x - dx, xends[-dx], -dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y - dy, yends[-dy], -dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                secondDirection+=1
            else:
                break
        if secondDirection+firstDirection >= 3:
            return 1
    return 0

def distanceFromBottom(board, column):
    d = 0
    for i in range(5, -1, -1):
        if board[i][column] != '-':
            d += 1
        else:
            break
    return d

def rateBoard(board):
    numberOfWinsX = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == '-':
                d = distanceFromBottom(board, column)
                numberOfWinsX += isWin(board, column, row, 'X') * (0.8 ** (5 - row - d))
    numberOfWinsO = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == '-':
                d = distanceFromBottom(board, column)
                numberOfWinsO += isWin(board, column, row, 'O') * 4 * (0.8 ** (5 - row - d))
    return numberOfWinsX - numberOfWinsO

def recursivelyPickAiSpot(board, iterations, turn):
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
    if iterations <= 0:
        return rateBoard(board)
    avg = 0
    for column in range(7):
        boardCopy = deepcopy(board)
        r,c = 5 - distanceFromBottom(board, column),column
        if turn == 'O' and isWin(boardCopy, c, r, 'O'):
            return -4
        elif turn == 'X' and isWin(boardCopy, c, r, 'X'):
            return 1
        boardCopy[r][c] = turn
        avg += recursivelyPickAiSpot(boardCopy, iterations - 1, turn)
    avg /= 7
    return avg

def pickAiSpot(board, iterations):
    for column in range(7):
        r,c = 5 - distanceFromBottom(board, column),column
        if board[r][c] == '-' and isWin(board, c, r, 'X'):
            return column
    for column in range(7):
        r,c = 5 - distanceFromBottom(board,column),column
        if board[r][c] == '-' and isWin(board, c, r, 'O'):
            return column
    plays = [0 for i in range(7)]
    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r < 0:
            plays[column] = -100000
        else:
            boardCopy[r][c] = 'X'
            plays[column] =  recursivelyPickAiSpot(boardCopy, iterations - 1, 'O')

    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r > 0:
            boardCopy[r][c] = 'X'
            if isWin(boardCopy, c, r - 1, 'O'):
                plays[column] = -10000

    p = plays.copy()
    p.sort()
    return plays.index(p[-1])


def main():
    board = [['-' for i in range(7)] for j in range(6)]
    winner = None
    while winner == None:
        printBoard(board)
        print('> ',end="")
        i = input()
        column = int(i[0])
        r,c = 5 - distanceFromBottom(board, column),column
        if isWin(board,c,r,'O'):
            winner = "O"
        board[5 - distanceFromBottom(board, column)][column] = 'O'
        if winner != None:
            break
        column = pickAiSpot(board[:], 5)
        r,c = 5 - distanceFromBottom(board, column),column
        if isWin(board,c,r,'X'):
            winner = "X"
        board[r][c] = 'X'

    printBoard(board)
    print('Winner is %s' % str(winner))

if __name__ == '__main__':
    main()
