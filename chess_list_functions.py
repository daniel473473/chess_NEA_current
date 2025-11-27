import constants

def list_empty_moves(row, column):
    return []


def list_pawn_moves(board, row, column, player):
    moves = []
    if player == "W":# if it is whites turn set the direction to be up 
        direction = -1
    else:# if it is blacks turn set the direction to be down
        direction = 1
    if board[row + direction][column].symbol == constants.EMPTY_CELL:
        moves.append([row + direction, column])# one square forward
        if row + 2 * direction >=0 and row + 2 * direction < 8  and board[row + 2 * direction][column].symbol == constants.EMPTY_CELL:
            moves.append([row + 2 * direction, column])# two squares forward
    moves.append([row + direction, column + 1])# takes right
    moves.append([row + direction, column - 1])# takes left
    return moves


def list_rook_moves(row, column):
    moves = []
    for i in range(-8, 9):
        moves.append([row + i, column])# list all of the possible rook row moves
        moves.append([row, column + i])# list all of the possible rook column moves
    return moves


def list_knight_moves(row, column):
    moves = []
    moves.append([row + 2, column + 1])# all possible knight moves
    moves.append([row + 2, column - 1])
    moves.append([row - 2, column + 1])
    moves.append([row - 2, column - 1])
    moves.append([row + 1, column + 2])
    moves.append([row + 1, column - 2])
    moves.append([row - 1, column + 2])
    moves.append([row - 1, column - 2])
    return moves


def list_bishop_moves(row, column):
    moves = []
    for i in range(-8, 9):# loop through all possible bishop moves
        moves.append([row + i, column + i])# one diagonal
        moves.append([row - i, column + i])# the other
    return moves


def list_king_moves(row, column):
    moves = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            moves.append([row + i, column + j])# one move or less in every direction
    return moves


def list_queen_moves(row, column):
    moves = []
    moves.extend(list_rook_moves(row, column))
    moves.extend(list_bishop_moves(row, column))
    return moves
    
        
