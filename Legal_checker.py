import constants
from numpy import sign

# TODO fix legal castle checks

def legalRangeMove(board, x, y):# check if the move is in range
    return False if x not in range(len(board)) or y not in range(len(board)) else True


def legalTaking(board, turn, x, y, pawn = False):
    opposing_player = "B" if turn % 2 == 1 else "W"
    return True if board[y][x].player == opposing_player and (board[y][x].code != constants.SHADOW_PAWN_CODE or pawn) else False

    if turn % 2 == 1:# check if white's turn
        return True if (board[y][x].player == "B" and not(not(pawn) and board[y][x].code == "BSP")) else False
    else:
        return True if (board[y][x].player == "W" and not(not(pawn) and board[y][x].code == "WSP"))  else False


def legalEmptyMove(board):
    return False


def legalPawnMove(board, row, column, spacesMovedX, spacesMovedY, player, moved,):
    AspacesMoveX = abs(spacesMovedX)
    AspacesMoveY = abs(spacesMovedY)

    if player == "W" and AspacesMoveY == spacesMovedY:# if the pawn moves in the wrong direction
        return False
    if player == "B" and AspacesMoveY != spacesMovedY:# if the pawn moves in the wrong direction
        return False

    if board[row + spacesMovedY][column + spacesMovedX].player == player and board[row + spacesMovedY][column + spacesMovedX].symbol != constants.EMPTY_CELL:# check if the pawn is taking a piece on its side
        return False

    if board[row + spacesMovedY][column + spacesMovedX].symbol != constants.EMPTY_CELL or (board[row + spacesMovedY][column + spacesMovedX].player != player and board[row + spacesMovedY][column + spacesMovedX].code == constants.SHADOW_PAWN_CODE):# check if the pawn is taking a piece on its front
        if AspacesMoveX != 1 or AspacesMoveY != 1:# if it doesn't take diagonally
            return False
    else:
        if spacesMovedX != 0:# if it moves sideways without taking
            return False

    if moved:
        if AspacesMoveY!=1:# if it moves to far after being moved
            return False
    else:
        if not(AspacesMoveY in range(1,3)):# if it moves too far for its first move
            return False
        elif AspacesMoveY == 2 and board[row + sign(spacesMovedY)][column].symbol != constants.EMPTY_CELL:# if it jumps a piece on its first move
            return False
        #if AspacesMoveY == 2 and  board[row + sign(spacesMovedY)][column].symbol != constants.EMPTY_CELL:
        #    return False


    return True


def legalRookMove(board, row, column, spacesMovedX, spacesMovedY, player, moved):
    if spacesMovedX * spacesMovedY != 0:# check it moves orthometrically
        return False
    if spacesMovedX == 0:
        for row2 in range(row + sign(spacesMovedY), row + spacesMovedY , sign(spacesMovedY)):
            if board[row2][column].symbol != constants.EMPTY_CELL:
                return False
    else:
        for column2 in range(column + sign(spacesMovedX), column + spacesMovedX, sign(spacesMovedX)):
            if board[row][column2].symbol != constants.EMPTY_CELL:
                return False
    return True


def legalKnightMove(board, row, column, spacesMovedX, spacesMovedY, player, moved):
    trueX = abs(spacesMovedX)
    trueY = abs(spacesMovedY)
    if not(trueX in range(1,3)) or not(trueY in range(1,3)):# check if the move forms the rough correct shape
        return False
    if trueX + trueY != 3:# check the knight moves 3 places
        return False
    return True


def legalBishopMove(board, row, column, spacesMovedX, spacesMovedY, player, moved):
    trueX = abs(spacesMovedX)
    trueY = abs(spacesMovedY)
    if trueX != trueY:# check it is travelling diagonally
        return False
    for spaces in range(1, trueY):
        row2 = spaces * sign(spacesMovedY)
        column2 = spaces * sign(spacesMovedX)
        if board[row + row2][column + column2].symbol != constants.EMPTY_CELL:# check if the bishop would jump a piece
            return False
    return True


def legalKingMove(board, row, column, spacesMovedX, spacesMovedY, player, moved):
    trueX = abs(spacesMovedX)
    trueY = abs(spacesMovedY)
    if not(trueX in range(0,2)) or not(trueY in range(0,2)):# ensure the king only moves 1 space
        return False
    return True


def legalQueenMove(board, row, column, spacesMovedX, spacesMovedY, player, moved):
    if abs(spacesMovedX) == abs(spacesMovedY):# check if the queen is moving like a bishop
        return legalBishopMove(board, row, column, spacesMovedX, spacesMovedY, player, moved)
    elif spacesMovedX * spacesMovedY == 0:# check if the queen is moving like a rook
        return legalRookMove(board, row, column, spacesMovedX, spacesMovedY, player, moved)
    else:
        return False



def legalShortCastle(board, turn):
    kingFound = False
    rookFound = False

    if turn % 2 == 1:# if it is whites turn
        for column in range(8):
            if kingFound and board[-1][column].symbol == constants.ROOK and board[-1][column].moved == False and board[-1][column].player == "W":# check if the rook has moved
                return True
            elif kingFound and board[-1][column].symbol != constants.EMPTY_CELL:# check if a piece is in the way
                return False
            if board[-1][column].symbol == constants.KING and board[-1][column].moved == False and board[-1][column].player == "W":# check if the king has moved
                kingFound = True
    else:
        for column in range(8):
            if kingFound and board[0][column].symbol == constants.ROOK and board[0][column].moved == False and board[0][column].player == "B":# check if the rook has moved
                return True
            elif kingFound and board[0][column].symbol != constants.EMPTY_CELL:# check if a piece is in the way
                return False
            if board[0][column].symbol == constants.KING and board[0][column].moved == False and board[0][column].player == "B":# check if the king has moved
                kingFound = True
    return False
def legalLongCastle(board, turn):
    kingFound = False
    rookFound = False

    if turn % 2 == 1:# if it is whites turn
        for column in range(8):
            if rookFound and board[-1][column].symbol == constants.KING and board[-1][column].moved == False and board[-1][column].player == "W":# check if the king has moved
                return True
            elif rookFound and board[-1][column].symbol != constants.EMPTY_CELL:# check if a piece is in the way
                return False
            if board[-1][column].symbol == constants.ROOK and board[-1][column].moved == False and board[-1][column].player == "W":# check if the rook has moved
                rookFound = True
    else:
        for column in range(8):
            if rookFound and board[0][column].symbol == constants.KING and board[0][column].moved == False and board[0][column].player == "B":# check if the king has moved
                return True
            elif rookFound and board[0][column].symbol != constants.EMPTY_CELL:# check if a piece is in the way
                return False
            if board[0][column].symbol == constants.ROOK and board[0][column].moved == False and board[0][column].player == "B":# check if the rook has moved
                rookFound = True
    return False