import numpy as np
import math
import random
from CHESS import chess
import chess_list_functions 
from numpy import sign
import constants
import pieces
import Legal_checker
import copy
import time

# TODO fix winning move check currently allows checkmates less moves
# TODO repitiion stalemates
# TODO insufficiant material stalemates


def highlight_white(text):
    return f"\033[47;30m{text}\033[m"  # White background, black text


# Function to check if a player has a winning move on the board.
def winning_move(game, board, turn):
    if game.inCheck(turn + 1, board):
        return True
    return False


# Function to score the position of a game board for a given player.
def score_position(game, turn):
    player = "W" if turn % 2 == 1 else "B"
    player_score = 0
    opponent_score = 0
    #'''
    for piece in game.White_pieces + game.Black_pieces:
            row = piece.y
            column = piece.x
            piece_score = 0
            #'''
            match piece.code:
                case constants.PAWN_CODE:
                    piece_score += [[ 0,  0,  0,  0,  0,  0,  0,  0,],
                                    [ 5, 10, 10,-25,-25, 10, 10,  5,],
                                    [ 5, -5,-10,  0,  0,-10, -5,  5,],
                                    [ 0,  0,  0, 25, 25,  0,  0,  0,],
                                    [ 0,  0,  0, 25, 25,  0,  0,  0,],
                                    [ 5, -5,-10,  0,  0,-10, -5,  5,],
                                    [ 5, 10, 10,-25,-25, 10, 10,  5,],
                                    [ 0,  0,  0,  0,  0,  0,  0,  0,],
                                    ][row][column]
                case constants.KNIGHT_CODE:
                    piece_score += [[-50,-40,-20,-30,-30,-20,-40,-50,],
                                    [-40,-20,  0,  5,  5,  0,-20,-40,],
                                    [-30,  5, 10, 15, 15, 10,  5,-30,],
                                    [-30,  0, 15, 20, 20, 15,  0,-30,],
                                    [-30,  0, 15, 20, 20, 15,  0,-30,],
                                    [-30,  5, 10, 15, 15, 10,  5,-30,],
                                    [-40,-20,  0,  5,  5,  0,-20,-40,],
                                    [-50,-40,-20,-30,-30,-20,-40,-50,],
                                    ][row][column]
                case constants.BISHOP_CODE:
                    piece_score += [[-20,-10,-40,-10,-10,-40,-10,-20,],
                                    [-10,  5,  0,  0,  0,  0,  5,-10,],
                                    [-10, 10, 10, 10, 10, 10, 10,-10,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-10, 10, 10, 10, 10, 10, 10,-10,],
                                    [-10,  5,  0,  0,  0,  0,  5,-10,],
                                    [-20,-10,-40,-10,-10,-40,-10,-20,],
                                    ][row][column]
                case constants.ROOK_CODE:
                    piece_score += [[-10,-20, 10, 20, 20, 10,-20,-10,],
                                    [-20,  0,  0,  0,  0,  0,  0,-20,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-10,  0, 10, 20, 20, 10,  0,-10,],
                                    [-10,  0, 10, 20, 20, 10,  0,-10,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-20,  0,  0,  0,  0,  0,  0,-20,],
                                    [-10,-20, 10, 20, 20, 10,-20,-10,],
                                    ][row][column]
                case constants.QUEEN_CODE:
                    piece_score += [[-10,-10, 10, 20, 20, 10,-10,-10,],
                                    [-10,  0,  0,  0,  0,  0,  0,-10,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-10,  0, 10, 20, 20, 10,  0,-10,],
                                    [-10,  0, 10, 20, 20, 10,  0,-10,],
                                    [-10,  0, 10, 10, 10, 10,  0,-10,],
                                    [-10,  0,  0,  0,  0,  0,  0,-10,],
                                    [-10,-10, 10, 20, 20, 10,-10,-10,],
                                    ][row][column]
                case constants.KING_CODE:
                    if len(game.White_pieces + game.Black_pieces) > 10:
                        piece_score += [[ 20,  30,  10,   0,   0,  10,  30,  20,],
                                        [  5,   5,   0,   0,   0,   0,   5,   5,],
                                        [-10, -20, -20, -20, -20, -20, -20, -10,],
                                        [-20, -30, -30, -40, -40, -30, -30, -20,],
                                        [-20, -30, -30, -40, -40, -30, -30, -20,],
                                        [-10, -20, -20, -20, -20, -20, -20, -10,],
                                        [  5,   5,   0,   0,   0,   0,   5,   5,],
                                        [ 20,  30,  10,   0,   0,  10,  30,  20,],
                                        ][row][column]
                    else:
                        piece_score += [[-50,-30,-30,-30,-30,-30,-30,-50,],
                                        [-30,-30,  0,  0,  0,  0,-30,-30,],
                                        [-30,-10, 20, 30, 30, 20,-10,-30,],
                                        [-30,-10, 30, 40, 40, 30,-10,-30,],
                                        [-30,-10, 30, 40, 40, 30,-10,-30,],
                                        [-30,-10, 20, 30, 30, 20,-10,-30,],
                                        [-30,-30,  0,  0,  0,  0,-30,-30,],
                                        [-50,-30,-30,-30,-30,-30,-30,-50,],
                                        ][row][column]
            piece_score /= 100
            if piece.code != constants.KING_CODE:
                piece_score += piece.value * 10
            if piece.player == player:
                player_score += piece_score
            else:
                opponent_score += piece_score
    score = 0
    score = player_score - opponent_score
    return score


# Function to check if a game board is a terminal node (end of the game).
def is_terminal_node(game, moves, turn):
    total_pieces = game.White_pieces + game.Black_pieces
    state = str(game)
    if len(total_pieces) == 2 or\
        game.mandatory_move_delay >= 50 or\
        len(total_pieces) == 3 and ("N" in [piece.code for piece in total_pieces] or "B" in [piece.code for piece in total_pieces]) or\
        len(total_pieces) == 4 and ("B", 1, "W") in [(piece.code, (piece.x + piece.y) % 2, piece.player) for piece in total_pieces] and ("B", 0, "B") in [(piece.code, (piece.x + piece.y) % 2, piece.player) for piece in total_pieces] or\
        (state in game.boards and game.boards[state] == 2):# check for stalemate
        return True
    for mv in moves:
        if not mv[0] == "0":
            piece = game.board[mv[2][0]][mv[2][1]]
            opposing_piece = game.board[mv[1][0]][mv[1][1]]
            taking = opposing_piece.symbol != constants.EMPTY_CELL or (piece.player != opposing_piece.player and opposing_piece.code == constants.SHADOW_PAWN_CODE and piece.code == constants.PAWN_CODE)
            game.movePiece(mv[1][0], mv[1][1], mv[2][0], mv[2][1], turn, promotion=mv[7], taking=taking, saveHistory=True) # never causes a delay
            if not game.inCheck(turn, game.board):# one second delay depth 3
                game.undoMove(game.board[mv[1][0]][mv[1][1]])
                return False
            else:
                game.undoMove(game.board[mv[1][0]][mv[1][1]])
        else:
            return False
    return True


# Minimax algorithm with Alpha-Beta Pruning for finding the best move on the game board.
def minimax(game, turn, depth, alpha, beta, maximizingPlayer):

    valid_locations = game.listLegalMoves(Check = False)

    terminal = is_terminal_node(game, valid_locations, turn)

    # Stop if the depth is zero or game over, the return the current board's score.
    if depth == 0 or terminal:
        if terminal: # game has ended
            if winning_move(game, game.board, turn + 1):# checkmate
                return (None, (constants.LARGE_NUM + depth) * (-1 if maximizingPlayer else 1))
            else: # Draw
                return (None, 0)
        else: # Depth is zero, so score the board
            return (None, score_position(game, turn) * np.random.normal(1, 0.1) * (1 if maximizingPlayer else -1))# some times causes a delay


    # Maximize the score if it's the maximizing player's turn
    if maximizingPlayer:
        value = False
        move = False
        for mv in valid_locations:
            new_score = -math.inf
            if not mv[0] == "0":
                piece = game.board[mv[2][0]][mv[2][1]]
                opposing_piece = game.board[mv[1][0]][mv[1][1]]
                taking = opposing_piece.symbol != constants.EMPTY_CELL or (piece.player != opposing_piece.player and opposing_piece.code == constants.SHADOW_PAWN_CODE and piece.code == constants.PAWN_CODE)
                game.movePiece(mv[1][0], mv[1][1], mv[2][0], mv[2][1], turn, promotion=mv[7], taking=taking, saveHistory=True) # never causes a delay
                if not game.inCheck(turn, game.board):# one second delay depth 3
                    if game.inCheck(turn + 1, game.board):
                        if len(game.listLegalMoves(Check=True)) == 0:# check if the check is mate
                            mv[4] = True
                            #game.undoMove(game.board[mv[1][0]][mv[1][1]])
                            #return (mv, math.inf)
                        else:
                            mv[3] = True
                    total_pieces = game.White_pieces + game.Black_pieces
                    state = str(game)
                    if len(total_pieces) == 2 or\
                        game.mandatory_move_delay >= 50 or\
                        len(total_pieces) == 3 and ("N" in [piece.code for piece in total_pieces] or "B" in [piece.code for piece in total_pieces]) or\
                        len(total_pieces) == 4 and ("B", 1) in [(piece.code, (piece.x + piece.y) % 2) for piece in total_pieces] and ("B", 0) in [(piece.code, (piece.x + piece.y) % 2) for piece in total_pieces] or\
                        (state in game.boards and game.boards[state] == 2):# check for stalemate
                        mv[5] = True
                        #game.undoMove(game.board[mv[1][0]][mv[1][1]])
                        #return (mv, 0)
                    # quintessentence search
                    #new_score = minimax(game, turn + 1, (1 if  depth == 1 and game.checkCheck(opposing_piece.y, opposing_piece.x, opposing_player = opposing_piece.player, board = game.board) else depth - 1), alpha, beta, False)[1]

                    new_score = minimax(game, turn + 1, depth - 1, alpha, beta, False)[1]

                    if not value or new_score > value: # Update the best move and alpha value.
                        value = new_score
                        move = mv
                game.undoMove(game.board[mv[1][0]][mv[1][1]])
            else:
                mv = game.decode_checks(mv)
                game.decode_castle(mv, save_history=True)
                new_score = minimax(game, turn + 1, depth-1, alpha, beta, False)[1]
                if game.inCheck(turn + 1, game.board):
                    if len(game.listLegalMoves(Check=True)) == 0:# check if the check is mate
                        mv += "#"
                    else:
                        mv += "+"
                if game.decode_checks(mv) == "0-0":
                    game.undoShortCastle()
                else:
                    game.undoLongCastle()

                if not value or new_score > value:# Update the best move and alpha value.
                    value = new_score
                    move = mv

            alpha = max(alpha, value)

            # Prune the search if the alpha value is greater than or equal to beta.
            if alpha >= beta:
                break
        #if not move:
        #    if winning_move(game, game.board, turn + 1):# checkmate
        #        return (None, math.inf * (-1 if maximizingPlayer else 1))
        #    else: # Draw
        #        return (None, 0)
        return move, value

    else: # Minimize the score if it's the minimizing player's turn.
        value = False
        move = False
        for mv in valid_locations:
            new_score = math.inf
            if not mv[0] == "0":
                piece = game.board[mv[2][0]][mv[2][1]]
                opposing_piece = game.board[mv[1][0]][mv[1][1]]
                taking = opposing_piece.symbol != constants.EMPTY_CELL or (opposing_piece.player != piece.player and opposing_piece.code == constants.SHADOW_PAWN_CODE and piece.code == constants.PAWN_CODE)
                game.movePiece(mv[1][0], mv[1][1], mv[2][0], mv[2][1], turn, promotion=mv[7], taking=taking, saveHistory=True)# almost never causes a delay 10^-4
                if not game.inCheck(turn, game.board):# one second delay depth 3
                    if game.inCheck(turn + 1, game.board):
                        if len(game.listLegalMoves(Check=True)) == 0:# check if the check is mate
                            mv[4] = True
                            #game.undoMove(game.board[mv[1][0]][mv[1][1]])
                            #return (mv, -math.inf)
                        else:
                            mv[3] = True
                    total_pieces = game.White_pieces + game.Black_pieces
                    state = str(game)
                    if len(total_pieces) == 2 or\
                        game.mandatory_move_delay >= 50 or\
                        len(total_pieces) == 3 and ("N" in [piece.code for piece in total_pieces] or "B" in [piece.code for piece in total_pieces]) or\
                        len(total_pieces) == 4 and ("B", 1) in [(piece.code, (piece.x + piece.y) % 2) for piece in total_pieces] and ("B", 0) in [(piece.code, (piece.x + piece.y) % 2) for piece in total_pieces] or\
                        (state in game.boards and game.boards[state] == 2):# check for stalemate
                        mv[5] = True
                        #game.undoMove(game.board[mv[1][0]][mv[1][1]])
                        #return (mv, 0)
                    
                    # quitenicence search
                    #new_score = minimax(game, turn + 1, (1 if  depth == 1 and game.checkCheck(opposing_piece.y, opposing_piece.x, opposing_player = opposing_piece.player, board = game.board) else depth - 1), alpha, beta, True)[1]

                    new_score = minimax(game, turn + 1, depth - 1, alpha, beta, True)[1]

                    if not value or new_score < value: # Update the best move and alpha value.
                        value = new_score
                        move = mv
                game.undoMove(game.board[mv[1][0]][mv[1][1]])
            else:
                mv = game.decode_checks(mv)
                game.decode_castle(mv, save_history=True)
                new_score = minimax(game, turn + 1, depth-1, alpha, beta, True)[1]
                if game.inCheck(turn + 1, game.board):
                    if len(game.listLegalMoves(Check=True)) == 0:# check if the check is mate
                        mv += "#"
                    else:
                        mv += "+"
                if game.decode_checks(mv) == "0-0":
                    game.undoShortCastle()
                else:
                    game.undoLongCastle()
                
                if not value or new_score < value: # Update the best move and alpha value.
                    value = new_score
                    move = mv
            beta = min(beta, value)

            # Prune the search if the alpha value is greater than or equal to beta
            if alpha >= beta:
                break
        #if not move:
        #    if winning_move(game, game.board, turn + 1):# checkmate
        #        return (None, math.inf * (-1 if maximizingPlayer else 1))
        #    else: # Draw
        #        return (None, 0)
        return move, value
   

def play_game(depth, show = False):
    # set up the class
    board = chess()

    # Initialize game state variables.
    game_over = False
    turn = 0


    # moves used index 0 end pos index 1 start pos
    moves_used = []

    # codes for the moves to be displayed at the top of the screen
    move_codes = []

    # locations of all of the taken pieces
    taken_pieces = []

    # promotions that occurred during the game
    promotions = []

    boards = [copy.deepcopy(board.board)]

    # temp board sync stuff
    temp_board = [["  "] * 8 for _ in range(8)]
    blacknames = ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR", "BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"]
    whitenames = ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR", "WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"]
    for i in range(16):
        temp_board[i//8][i%8] = blacknames[i]
        temp_board[7 - i//8][i%8] = whitenames[i]


    # Main game loop
    while not game_over:
        if show:
            board.display(board.board)
        legal = False
        board.conversion_moves = [[i, board.encode(i)] if not i[0] == "0" else [i, i] for i in board.listLegalMoves()]
        board.legal_moves = [i[1] if not i[0] == "0" else i for i in board.conversion_moves]
        board.conversion_moves = filter(lambda x: not x[0][0] == "0", board.conversion_moves)
        if show:
            print(board.legal_moves)
        while legal == False:
            if show:
                tick = time.time()
            try:
                encoded_code, minimax_score = minimax(board, board.turn, depth, -math.inf, math.inf, True,)
            except RecursionError:
                print("problem")
                input()
            if show:
                print(time.time()- tick)
            if not encoded_code[0] == "0": 
                for move, move_code in board.conversion_moves:
                    if move[0] == encoded_code[0] and move[1] == encoded_code[1] and move[2] == encoded_code[2] and move[7] == encoded_code[7]:
                        code = move_code
                        break
                #code = board.encode(encoded_code)
                #if encoded_code[11] or encoded_code[10]:# if there is disambiguation needed
                #    print("disambiguation move:", code)
                #    print("encoded move:", encoded_code)
                    #input()
            else:
                code = encoded_code
            if code in board.legal_moves:
                legal = True
                if show:
                    print(code, minimax_score)
                    print(board.mandatory_move_delay)
            else:
                print("illegal move attempted:", code)
                print("legal moves are:", board.legal_moves)
                board.legal_moves = [board.encode(i) if not i[0] == "0" else i for i in board.listLegalMoves()]
                print(board.legal_moves, "\n",board.White_pieces, "\n", board.Black_pieces, "\n", board.shadow_pawns, "\n", board.turn)
                print(code, minimax_score)
                raise Exception("illegal move")
        game_over = board.playStep(code)
        
        # add the board to the list of boards for history
        boards.append(copy.deepcopy(board.board))

        # add the used moves the list of moves
        move_codes.append(code)

        # add taken pieces
        taken_pieces.append(encoded_code[12] if not encoded_code[0] == "0" else None)

        # add if a piece promoted
        promotions.append(encoded_code[7] if not encoded_code[0] == "0" else None)

        if encoded_code[0] != "0":
            moves_used.append(encoded_code[1:3])
        else:
            encoded_code = board.decode_checks(encoded_code)
            if board.turn % 2 == 0:# if it is whites turn
                moves_used.append([[[7, 6], [7, 4]], [[7,5], [7,7]]] if encoded_code == "0-0" else [[[7, 2], [7, 4]], [[7, 3], [7, 0]]])
            else:
                moves_used.append([[[0, 6], [0, 4]], [[0,5], [0,7]]] if encoded_code == "0-0" else [[[0, 2], [0, 4]], [[0, 3], [0, 0]]])

        turn = (turn + 1) % 2
        if board.turn > 1000:
            input("draw?")
            game_over = True
    if show:
        board.display(board.board)
        print(f"Game Over {'White' if board.turn % 2 == 0 else 'Black'} wins")
        print(moves_used)
    return moves_used, boards, move_codes, taken_pieces, promotions

if __name__ == "__main__":
    while True:
        play_game(1, show=True)
