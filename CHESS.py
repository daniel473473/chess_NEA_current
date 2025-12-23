import chess_list_functions 
import constants
import pieces
import Legal_checker
import copy
import time
import math




# TODO 50 move rule
# TODO repetition
# TODO stop casting in check

def underline(text):
    return f"\033[4m{text}\033[0m"# under line the text
def highlight_white(text):
    return f"\033[47;30m{text}\033[m"  # White background, black text


class chess:# the whole game class


    def __init__(self):
        # set up the variables for decode
        self.reset()


    def reset(self):# set the board back to the start position

        self.moves_used = []

        # first board Position

        self.board = [
            [pieces.Rook(0, 0, "B"), pieces.Knight(0, 1, "B"), pieces.Bishop(0, 2, "B"), pieces.Queen(0, 3, "B"), pieces.King(0, 4, "B"), pieces.Bishop(0, 5, "B"), pieces.Knight(0, 6, "B"), pieces.Rook(0, 7, "B")],
            [pieces.Pawn(1, 0, "B"), pieces.Pawn(1, 1, "B"), pieces.Pawn(1, 2, "B"), pieces.Pawn(1, 3, "B"), pieces.Pawn(1, 4, "B"), pieces.Pawn(1, 5, "B"), pieces.Pawn(1, 6, "B"), pieces.Pawn(1, 7, "B")],
            [pieces.Empty_Cell(2, 0), pieces.Empty_Cell(2, 1), pieces.Empty_Cell(2, 2), pieces.Empty_Cell(2, 3), pieces.Empty_Cell(2, 4), pieces.Empty_Cell(2, 5), pieces.Empty_Cell(2, 6), pieces.Empty_Cell(2, 7)],
            [pieces.Empty_Cell(3, 0), pieces.Empty_Cell(3, 1), pieces.Empty_Cell(3, 2), pieces.Empty_Cell(3, 3), pieces.Empty_Cell(3, 4), pieces.Empty_Cell(3, 5), pieces.Empty_Cell(3, 6), pieces.Empty_Cell(3, 7)],
            [pieces.Empty_Cell(4, 0), pieces.Empty_Cell(4, 1), pieces.Empty_Cell(4, 2), pieces.Empty_Cell(4, 3), pieces.Empty_Cell(4, 4), pieces.Empty_Cell(4, 5), pieces.Empty_Cell(4, 6), pieces.Empty_Cell(4, 7)],
            [pieces.Empty_Cell(5, 0), pieces.Empty_Cell(5, 1), pieces.Empty_Cell(5, 2), pieces.Empty_Cell(5, 3), pieces.Empty_Cell(5, 4), pieces.Empty_Cell(5, 5), pieces.Empty_Cell(5, 6), pieces.Empty_Cell(5, 7)],
            [pieces.Pawn(6, 0, "W"), pieces.Pawn(6, 1, "W"), pieces.Pawn(6, 2, "W"), pieces.Pawn(6, 3, "W"), pieces.Pawn(6, 4, "W"), pieces.Pawn(6, 5, "W"), pieces.Pawn(6, 6, "W"), pieces.Pawn(6, 7, "W")],
            [pieces.Rook(7, 0, "W"), pieces.Knight(7, 1, "W"), pieces.Bishop(7, 2, "W"), pieces.Queen(7, 3, "W"), pieces.King(7, 4, "W"), pieces.Bishop(7, 5, "W"), pieces.Knight(7, 6, "W"), pieces.Rook(7, 7, "W")],
        ]
        '''
        self.board = [[pieces.Empty_Cell(0,0),pieces.Empty_Cell(0,1),pieces.Empty_Cell(0,2),pieces.Empty_Cell(0,3),pieces.King(0,4,"B"),pieces.Empty_Cell(0,5),pieces.Empty_Cell(0,6),pieces.Empty_Cell(0,7)],[pieces.Empty_Cell(1,0),pieces.Empty_Cell(1,1),pieces.Empty_Cell(1,2),pieces.Empty_Cell(1,3),pieces.Empty_Cell(1,4),pieces.Empty_Cell(1,5),pieces.Empty_Cell(1,6),pieces.Empty_Cell(1,7)],[pieces.Rook(2,0,"W"),pieces.Empty_Cell(2,1),pieces.Empty_Cell(2,2),pieces.Empty_Cell(2,3),pieces.Empty_Cell(2,4),pieces.Empty_Cell(2,5),pieces.Empty_Cell(2,6),pieces.Empty_Cell(2,7)],[pieces.Empty_Cell(3,0),pieces.Empty_Cell(3,1),pieces.Empty_Cell(3,2),pieces.Empty_Cell(3,3),pieces.Empty_Cell(3,4),pieces.Empty_Cell(3,5),pieces.Empty_Cell(3,6),pieces.Empty_Cell(3,7)],[pieces.Empty_Cell(4,0),pieces.Empty_Cell(4,1),pieces.Empty_Cell(4,2),pieces.Empty_Cell(4,3),pieces.Empty_Cell(4,4),pieces.Empty_Cell(4,5),pieces.Empty_Cell(4,6),pieces.Empty_Cell(4,7)],[pieces.Empty_Cell(5,0),pieces.Empty_Cell(5,1),pieces.Empty_Cell(5,2),pieces.Empty_Cell(5,3),pieces.Empty_Cell(5,4),pieces.Empty_Cell(5,5),pieces.Empty_Cell(5,6),pieces.Empty_Cell(5,7)],[pieces.Empty_Cell(6,0),pieces.Empty_Cell(6,1),pieces.Empty_Cell(6,2),pieces.Empty_Cell(6,3),pieces.Empty_Cell(6,4),pieces.Empty_Cell(6,5),pieces.Empty_Cell(6,6),pieces.Empty_Cell(6,7)],[pieces.Rook(7,0,"W"),pieces.Empty_Cell(7,1),pieces.Empty_Cell(7,2),pieces.Empty_Cell(7,3),pieces.King(7,4,"W"),pieces.Empty_Cell(7,5),pieces.Empty_Cell(7,6),pieces.Empty_Cell(7,7)]]

        #'''
        # set the first turn to be 0

        self.turn = 1

        # set the winner and draw varibles

        self.winner = None
        self.drawn = False

        self.White_pieces, self.Black_pieces = self.storePieces(self.board)# list of pieces for each player

        self.shadow_pawn_history = []# list of shadow pawns that have been created

        self.shadow_pawns = []

        # history of the mandatory move delays
        self.mandatory_move_delay_history = []

        # time since last pawn/taking move
        self.mandatory_move_delay = 0


        self.move_time = 0


    def storePieces(self, board):
        White_pieces = []
        Black_pieces = []
        for row in board:
            for piece in row:
                if piece.symbol != constants.EMPTY_CELL:
                    if piece.player == "W":
                        White_pieces.append(piece)
                    else:
                        Black_pieces.append(piece)
        White_pieces.sort()
        Black_pieces.sort()
        return White_pieces, Black_pieces


    def getPieces(self, turn):
        if turn % 2 == 1:
            self.White_pieces.sort()
            return self.White_pieces
        else:
            self.Black_pieces.sort()
            return self.Black_pieces


    def display(self, board):
        print(underline(f"  | a | b | c | d | e | f | g | h |"))
        for row in range(8):
            print(underline(f"{8-row} |"),end="")
            for column in range(8):
                if board[row][column].code == constants.SHADOW_PAWN_CODE:
                    print(highlight_white("S") if board[row][column].created else "S", end="")
                if board[row][column].symbol == constants.EMPTY_CELL: print(highlight_white(f" {constants.EMPTY_CELL} ") if (row + column) % 2 == 0 else f" {constants.EMPTY_CELL} ", end="")
                else: print(highlight_white(f' {board[row][column].player + board[row][column].symbol} ') if (row + column) % 2 == 0 else f' {board[row][column].player + board[row][column].symbol} ',end="")
            print()
        print(underline(f"  | a | b | c | d | e | f | g | h |"))


    def encodeString(self, x, y):
        X = chr(x + ord("a"))
        Y = str(8 - y)
        return X+Y


    def encode(self, move):# 0 --> the piece code, 1 --> the end position, 2 --> the start position, 3 --> check, 4 --> checkmate, 5 --> stalemate, 6 --> castled, 7 --> promotion
        code = str(move[0])
        if move[8]:
            if move[0] == constants.PAWN_CODE:
                code += chr(move[2][1] + ord("a"))
            code += "x"
        if move[10] and move[0]:# disambiguate in y direction
            code += str(8 - move[2][0])
        if move[11] and move[0]:# disambiguate in x direction
            code += chr(move[2][1] + ord("a"))
        code += self.encodeString(move[1][1], move[1][0])
        if not move[7] is None:
            code += "="+move[7]
        if move[3]:
            code += "+"
        elif move[4]:
            code += "#"
        if move[5]:
            code += "-"
        return code


    def decodeString(self, x, y):
        X = ord(x) - ord("a")
        Y = 8 - int(y)
        return X, Y


    def decode_checks(self, code):
        if code[-1] == "-":# check for stalemate
            self.drawn = True
            code = code[:-1]
        if code[-1] == "+":# check for check
            code = code[:-1]
        elif code[-1] == "#":# check for checkmate
            self.winner = "W" if self.turn % 2 == 1 else "B"
            code = code[:-1]
        return code


    def decode_castle(self, code, save_history = False):
        castled = False
        if code == "0-0":
                castled = True
                self.shortCastle(save_history=save_history)
        elif code == "0-0-0":
                castled = True
                self.longCastle(save_history=save_history)
        return castled


    def decode(self, code, board, turn):# decode the chess abrivations

        # reset the variables

        piece = ""
        endXCoor = -1
        endYCoor = -1
        startXCoor = -1
        startYCoor = -1
        taking = False
        check = False
        checkmate = False 
        promotion = False
        knownX = -1
        knownY = -1 

        if code[-1].isupper():# if it is pawn promotion
            if code[-2] == "=":
                promotion = code[-1:]
                code = code[:-2]

        # find end positions

        endXCoor, endYCoor = self.decodeString(code[-2], code[-1])

        # check if the move will take a piece

        if (code[1] == "x"):
            if code != code.lower():# if a non pawn piece took
                if Legal_checker.legalTaking(board, turn, endXCoor, endYCoor):# if it will take a piece legally
                    taking = True
                    code = code[0] + code[2:]
            else:
                if Legal_checker.legalTaking(board, turn, endXCoor, endYCoor, pawn=True):# if it will take a piece legally
                    taking = True
                    code = code[0] + code[2:]

        if code.lower() == code:# pawn move
            piece = constants.PAWN
            #print(code, len(code), code[0].isalpha())
            if len(code) >= 3:# check for disambiguation
                if code[0].isalpha():# check for correct character
                    knownX = ord(code[0]) - ord("a")
                    #print(knownX, knownY)
        else:# non pawn move
            if len(code) in range(4,6):# is there disambiguation
                    if code[-3].isnumeric():# is there disambiguation in the y direction
                        knownY = 8 - int(code[-3])
                        if len(code) == 4:# is there disambiguation in both directions
                            if code[-4].islower():# is there disambiguation in the x direction lower as first letter will be uppercase alphabetic
                                knownX = ord(code[-4]) - ord("a")
                    elif code[-3].islower():# is there disambiguation in the x direction
                        knownX = ord(code[-3]) - ord("a")
                    #print(knownX, knownY)
            if code[0] == "B":# bishop move
                piece = constants.BISHOP
            elif code[0] == "N":# knight move
                piece = constants.KNIGHT
            elif code[0] == "R":# rook move
                piece = constants.ROOK
            elif code[0] == "Q":# queen move
                piece = constants.QUEEN
            elif code[0] == "K":# king move
                piece = constants.KING
        startXCoor, startYCoor = self.findPiece(piece, endXCoor, endYCoor, knownX, knownY, turn)# find the piece that moved
        return endXCoor, endYCoor, startXCoor, startYCoor, promotion, taking


    def checkCheck(self, row, column, opposing_player = None, board = None, turn = 0):# checks if a square is in check
        for attacking_row, attacking_column, in [(row + 1, column + 2,),# return in check from knights
                                                    (row - 1, column + 2,),
                                                    (row + 1, column - 2,),
                                                    (row - 1, column - 2,),
                                                    (row + 2, column + 1,),
                                                    (row - 2, column + 1,),
                                                    (row + 2, column - 1,),
                                                    (row - 2, column - 1,),
                                                    ]:
            if attacking_column in range(8) and attacking_row in range(8) and board[attacking_row][attacking_column].code == constants.KNIGHT_CODE and board[attacking_row][attacking_column].player == opposing_player:
                return True
        distance = 1
        while row - distance >= 0:# return check from rooks and queens in the same column up
            code = board[row - distance][column].code
            if board[row - distance][column].player == opposing_player:
                if code in [constants.ROOK_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1
        
        distance = 1
        while row + distance < 8:# return check from rooks and queens in the same column down
            code = board[row + distance][column].code
            if board[row + distance][column].player == opposing_player:
                if code in [constants.ROOK_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1

        distance = 1
        while column - distance >= 0:# return check from rooks and queens in the same row left
            code = board[row][column - distance].code
            if board[row][column - distance].player == opposing_player:
                if code in [constants.ROOK_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1
        
        distance = 1
        while column + distance < 8:# return check from rooks and queens in the same row right
            code = board[row][column + distance].code
            if board[row][column + distance].player == opposing_player:
                if code in [constants.ROOK_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1

        distance = 1
        while row - distance >= 0 and column - distance >= 0:# return in bishops and queens in the diagonal up and left
            code = board[row - distance][column - distance].code
            if board[row - distance][column - distance].player == opposing_player:
                if code in [constants.BISHOP_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1

        #self.display(board)
        distance = 1
        while row + distance < 8 and column + distance < 8:# return in bishops and queens in the diagonal down and right
            code = board[row + distance][column + distance].code
            if board[row + distance][column + distance].player == opposing_player:
                if code in [constants.BISHOP_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1

        distance = 1
        while row - distance >= 0 and column + distance < 8:# return in bishops and queens in the diagonal up and right
            code = board[row - distance][column + distance].code
            if board[row - distance][column + distance].player == opposing_player:
                if code in [constants.BISHOP_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1

        distance = 1
        while row + distance < 8 and column - distance >= 0:# return in bishops and queens in the diagonal down and left
            code = board[row + distance][column - distance].code
            if board[row + distance][column - distance].player == opposing_player:
                if code in [constants.BISHOP_CODE, constants.QUEEN_CODE]:
                    return True
            if code != constants.EMPTY_CODE and code != constants.SHADOW_PAWN_CODE:
                break
            distance += 1
        # single space checks
        for pos in [
            [row + 1, column + 1],
            [row + 1, column],
            [row + 1, column - 1],
            [row, column + 1],
            [row, column - 1],
            [row - 1, column + 1],
            [row - 1, column],
            [row - 1, column - 1],
            
        ]:
            if pos[0] >=0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8:
                if board[pos[0]][pos[1]].player == opposing_player:
                    if board[pos[0]][pos[1]].code == constants.KING_CODE:
                        return True
                    if board[pos[0]][pos[1]].code == constants.PAWN_CODE and pos[1] != column and ((opposing_player == "W" and pos[0] == row + 1) or (opposing_player == "B" and pos[0] == row - 1)):
                        return True
        return False


    def findPiece(self, piece, endXCoor, endYCoor, knownX, knownY, turn):
        pieces = self.getPieces(turn)# get the pieces of the player whose turn it is
        XCoor = -1
        YCoor = -1
        for player_piece in pieces:# loop through all the pieces to find the one that moved
            if player_piece.symbol == piece and (knownX == -1 or player_piece.x == knownX) and (knownY == -1 or player_piece.y == knownY):
                if player_piece.legal(
                    self.board,
                    player_piece.y,
                    player_piece.x,
                    endXCoor - player_piece.x,
                    endYCoor - player_piece.y,
                    player_piece.player,
                    player_piece.moved):
                    YCoor, XCoor = player_piece.y, player_piece.x
        return XCoor, YCoor


    def movePiece(self, endYCoor, endXCoor, startYCoor, startXCoor, turn, promotion = False, taking = False, saveHistory = False):

        self.turn += 1


        # save the delay
        if saveHistory:
            self.mandatory_move_delay_history.append(self.mandatory_move_delay)


        # increment the mandatory move delay
        self.mandatory_move_delay += 1

        self.removeShadows(saveHistory)# remove the shadow pawns


        # reset the move delay if a pawn was moved
        if self.board[startYCoor][startXCoor].code == constants.PAWN_CODE:
            self.mandatory_move_delay = 0

        if promotion:
            player = "W" if turn % 2 == 1 else "B"
            match promotion:
                case "B":# bishop move
                    promotion = pieces.Bishop(endYCoor, endXCoor,player)
                case "N":# knight move
                    promotion = pieces.Knight(endYCoor, endXCoor,player)
                case "R":# rook move
                    promotion = pieces.Rook(endYCoor, endXCoor,player)
                case "Q":# queen move
                    promotion = pieces.Queen(endYCoor, endXCoor,player)
            if saveHistory:# add history to the promoted piece so that undo works
                promotion.update_history(self.board[endYCoor][endXCoor])
            if player == "W":# change the list of pieces
                self.White_pieces.append(promotion)
            else:
                self.Black_pieces.append(promotion)
        
        if taking:
                # reset the move delay
                self.mandatory_move_delay = 0

                if self.board[endYCoor][endXCoor].code == constants.SHADOW_PAWN_CODE and self.board[startYCoor][startXCoor].code == constants.PAWN_CODE:
                    x = self.board[endYCoor][endXCoor]# temporary variable for coors
                    if x.player == "W":# if it is a white pawn
                        self.White_pieces.remove(self.board[x.pawn_row][x.pawn_column])# remove the pawn from the list of pieces
                    else:# if it is a black pawn
                        self.Black_pieces.remove(self.board[x.pawn_row][x.pawn_column])# remove the pawn from the list of pieces
                    if saveHistory:
                        self.board[startYCoor][startXCoor].set_next_taken(self.board[x.pawn_row][x.pawn_column])# save the taken piece
                    self.shadow_pawns.remove(self.board[endYCoor][endXCoor])# remove the shadow pawn from the list of shadow pawns
                    self.board[x.pawn_row][x.pawn_column] = pieces.Empty_Cell(x.pawn_row, x.pawn_column)
                else:
                    if self.board[endYCoor][endXCoor].player == "W":# remove the piece from the list of pieces
                        self.White_pieces.remove(self.board[endYCoor][endXCoor])
                    elif self.board[endYCoor][endXCoor].player == "B":
                        self.Black_pieces.remove(self.board[endYCoor][endXCoor])
                    else:
                        self.display(self.board)
                        print("ERROR")
                        print(self.encode((self.board[startYCoor][startXCoor].code, (endYCoor, endXCoor), (startYCoor, startXCoor), False, False, False, False, promotion.symbol[-1] if promotion else None, taking)))
                        print(self.White_pieces, "\n", self.Black_pieces)
                        raise Exception("ERROR")
                
        else:
            if self.board[startYCoor][startXCoor].code == constants.PAWN_CODE and abs(startYCoor - endYCoor) > 1:# shadow pawn for enpassant
                direction = -1 if turn % 2 == 1 else 1# direction of the pawn
                self.board[endYCoor - direction][endXCoor] = pieces.Shadow_Pawn(endYCoor - direction, endXCoor, endYCoor, endXCoor, self.board[startYCoor][startXCoor].player)
                self.shadow_pawns.append(self.board[endYCoor - direction][endXCoor])# add the shadow pawn to the list of shadow pawns
            if self.board[endYCoor][endXCoor].code == constants.SHADOW_PAWN_CODE:# if a shadown pawn is "taken"
                self.shadow_pawns.remove(self.board[endYCoor][endXCoor])# remove the shadow pawn from the list of shadow pawns
        if promotion:

            # update the history differently for promotion
            if saveHistory:
                promotion.update_history(self.board[startYCoor][startXCoor])

            # remove the piece that promoted
            if self.board[startYCoor][startXCoor].player == "W":# remove the piece from the list of pieces
                self.White_pieces.remove(self.board[startYCoor][startXCoor])
            elif self.board[startYCoor][startXCoor].player == "B":
                self.Black_pieces.remove(self.board[startYCoor][startXCoor])
        else:
            if saveHistory:
                self.board[startYCoor][startXCoor].update_history(self.board[endYCoor][endXCoor])
        
        if not promotion:
            self.board[startYCoor][startXCoor].move(endXCoor, endYCoor,)# update the variables of the piece
        self.board[endYCoor][endXCoor] = promotion if promotion else self.board[startYCoor][startXCoor]# move piece to new position
        self.board[startYCoor][startXCoor] = pieces.Empty_Cell(startYCoor, startXCoor)# empty old position

        # ensure the order of the lists are constant
        self.White_pieces.sort()
        self.Black_pieces.sort()


    def undoMove(self, piece):
        
        # undo the mandatory move delay changes
        self.mandatory_move_delay = self.mandatory_move_delay_history.pop()

        x, y = piece.x, piece.y# get the current position of the piece
        old_X, old_Y, old_piece = piece.undo_move()# get the old position of the piece
        if (x, y) == (old_X, old_Y):
            _, _, first_piece = piece.undo_move()# the piece that was taken during promotion
            first_x, first_y, = first_piece.x, first_piece.y
            self.board[first_y][first_x] = first_piece
            if first_piece.player == "W":# add the piece back to the list of pieces
                self.White_pieces.append(first_piece)
            elif first_piece.player == "B":
                self.Black_pieces.append(first_piece)
            
            if piece.player == "W":# remove the other piece from the list of pieces
                self.White_pieces.remove(piece)
            elif piece.player == "B":
                self.Black_pieces.remove(piece)

            self.board[old_piece.y][old_piece.x] = old_piece# do its own values as saved ones are off
        else:
            self.board[old_Y][old_X] = piece
            self.board[y][x] = old_piece

        if self.board[y][x].code == constants.SHADOW_PAWN_CODE:
            self.shadow_pawns.append(self.board[y][x])# add the shadow pawn back to the list of shadow pawns if it was taken
            if piece.code == constants.PAWN_CODE:# if the piece is a shadow pawn
                second_old_piece = piece.get_next_taken()# get the piece that was taken with the shadow pawn
                self.board[second_old_piece.y][second_old_piece.x] = second_old_piece# set the piece that was taken with the shadow pawn back to its old position
                if second_old_piece.player == "W":# add the piece back to the list of pieces
                    self.White_pieces.append(second_old_piece)
                elif second_old_piece.player == "B":
                    self.Black_pieces.append(second_old_piece)
                else:
                    self.display(self.board)
                    print("ERROR")
                    input(second_old_piece)
                    raise Exception("ERROR")

        elif old_piece.player == "W":# add the piece back to the list of pieces
            self.White_pieces.append(old_piece)
        elif old_piece.player == "B":
            self.Black_pieces.append(old_piece)
        piece.x, piece.y = old_X, old_Y# set the piece to the old position
        self.undoShadowPawns()
        self.turn -= 1

        # ensure the order of the lists are constant
        self.White_pieces.sort()
        self.Black_pieces.sort()

        #self.moves_used.pop()# remove the last move from the list of moves used


    def check_pieces(self, strng):
        current_white, current_black = self.storePieces(self.board)
        if not (current_white == self.White_pieces and current_black == self.Black_pieces):
            print(strng)
            print("ERROR: Desync between board and piece lists")
            print("White pieces on board:", current_white)
            print("White pieces in list:", self.White_pieces)
            print("Black pieces on board:", current_black)
            print("Black pieces in list:", self.Black_pieces)
            self.display(self.board)
            raise Exception("Desync between board and piece lists")


    def undoShadowPawns(self):
        for i in range(len(self.shadow_pawns)-1, -1, -1):
            shadow_pawn = self.shadow_pawns[i]
            if shadow_pawn.created:
                self.board[shadow_pawn.y][shadow_pawn.x] = pieces.Empty_Cell(shadow_pawn.y, shadow_pawn.x)# set the shadow pawn to be empty
                self.shadow_pawns.remove(shadow_pawn)# remove the shadow pawn from the board
            else:
                self.board[shadow_pawn.y][shadow_pawn.x].created = True
        shadow_pawn = self.shadow_pawn_history.pop()
        if not shadow_pawn is None:
            shadow_pawn.created = False# set the shadow pawn to be created
            self.board[shadow_pawn.y][shadow_pawn.x] = shadow_pawn# restore the shadow pawn
            self.shadow_pawns.append(shadow_pawn)# add the shadow pawn back to the list of shadow pawns


    def undoShortCastle(self):

        self.undoShadowPawns()

        self.turn -= 1
        if self.turn % 2 == 1:# if it is white's turn
            self.board[7][4] = self.board[7][6]# move the king back
            self.board[7][4].y, self.board[7][4].x = 7, 4
            self.board[7][4].moved = False
            self.board[7][7] = self.board[7][5]# move the rook back
            self.board[7][7].y, self.board[7][7].x = 7, 7
            self.board[7][7].moved = False
            self.board[7][6] = pieces.Empty_Cell(7, 6)# reset the empty cells
            self.board[7][5] = pieces.Empty_Cell(7, 5)# reset the empty cells
        else:
            self.board[0][4] = self.board[0][6]# move the king
            self.board[0][4].y, self.board[0][4].x = 0, 4
            self.board[0][4].moved = False
            self.board[0][7] = self.board[0][5]# move the rook
            self.board[0][7].y, self.board[0][7].x = 0, 7
            self.board[0][7].moved = False
            self.board[0][6] = pieces.Empty_Cell(0, 6)# reset the empty cells
            self.board[0][5] = pieces.Empty_Cell(0, 5)# reset the empty cells


    def undoLongCastle(self):
        self.undoShadowPawns()

        self.turn -= 1
        if self.turn % 2 == 1:# if it is white's turn
            self.board[7][4] = self.board[7][2]# move the king
            self.board[7][4].y, self.board[7][4].x = 7, 4
            self.board[7][4].moved = False
            self.board[7][0] = self.board[7][3]# move the rook
            self.board[7][0].y, self.board[7][0].x = 7, 0
            self.board[7][0].moved = False
            self.board[7][2] = pieces.Empty_Cell(7, 2)# reset the empty cells
            self.board[7][3] = pieces.Empty_Cell(7, 3)# reset the empty cells
        else:
            self.board[0][4] = self.board[0][2]# move the king
            self.board[0][4].y, self.board[0][4].x = 0, 4
            self.board[0][4].moved = False
            self.board[0][0] = self.board[0][3]# move the rook
            self.board[0][0].y, self.board[0][0].x = 0, 0
            self.board[0][0].moved = False
            self.board[0][2] = pieces.Empty_Cell(0, 2)# reset the empty cells
            self.board[0][3] = pieces.Empty_Cell(0, 3)# reset the empty cells


    def shortCastle(self, save_history = False):
        if self.turn % 2 == 1:# if it is white's turn
            self.board[7][6] = self.board[7][4]# move the king
            self.board[7][6].y, self.board[7][6].x = 7, 6
            self.board[7][6].moved = True
            self.board[7][5] = self.board[7][7]# move the rook
            self.board[7][5].y, self.board[7][5].x = 7, 5
            self.board[7][6].moved = True
            self.board[7][4] = pieces.Empty_Cell(7, 4)# reset the empty cells
            self.board[7][7] = pieces.Empty_Cell(7, 7)# reset the empty cells
        else:
            self.board[0][6] = self.board[0][4]# move the king
            self.board[0][6].y, self.board[0][6].x = 0, 6
            self.board[0][6].moved = True
            self.board[0][5] = self.board[0][7]# move the rook
            self.board[0][5].y, self.board[0][5].x = 0, 5
            self.board[0][6].moved = True
            self.board[0][4] = pieces.Empty_Cell(0, 4)# reset the empty cells
            self.board[0][7] = pieces.Empty_Cell(0, 7)# reset the empty cells
        self.turn += 1

        self.removeShadows(save_history = save_history)


    def longCastle(self, save_history = False):
        if self.turn % 2 == 1:# if it is white's turn
            self.board[7][2] = self.board[7][4]# move the king
            self.board[7][2].y, self.board[7][2].x = 7, 2
            self.board[7][2].moved = True
            self.board[7][3] = self.board[7][0]# move the rook
            self.board[7][3].y, self.board[7][3].x = 7, 3
            self.board[7][3].moved = True
            self.board[7][4] = pieces.Empty_Cell(7, 4)# reset the empty cells
            self.board[7][0] = pieces.Empty_Cell(7, 0)# reset the empty cells
            self.board[7][1] = pieces.Empty_Cell(7, 1)# reset the empty cells
        else:
            self.board[0][2] = self.board[0][4]# move the king
            self.board[0][2].y, self.board[0][2].x = 0, 2
            self.board[0][2].moved = True
            self.board[0][3] = self.board[0][0]# move the rook
            self.board[0][3].y, self.board[0][3].x = 0, 3
            self.board[0][3].moved = True
            self.board[0][4] = pieces.Empty_Cell(0, 4)# reset the empty cells
            self.board[0][0] = pieces.Empty_Cell(0, 0)# reset the empty cells
            self.board[0][1] = pieces.Empty_Cell(0, 1)# reset the empty cells
        self.turn += 1

        self.removeShadows(save_history = save_history)


    def removeShadows(self, save_history):# remove the shadow pawns after a turn
        if save_history:
            updated = False
        for i in range(len(self.shadow_pawns)-1, -1, -1):
            shadow_pawn = self.shadow_pawns[i]# get the shadow pawn
            if shadow_pawn.created:
                self.board[shadow_pawn.y][shadow_pawn.x].created = False# leave a turn to be taken
            else:
                if save_history:
                    self.shadow_pawn_history.append(shadow_pawn)
                    updated = True
                self.board[shadow_pawn.y][shadow_pawn.x] = pieces.Empty_Cell(shadow_pawn.y, shadow_pawn.x)
                self.shadow_pawns.remove(shadow_pawn)
        if save_history and not updated:# if no shadow pawns were removed
            self.shadow_pawn_history.append(None)


    def moveInput(self, move = None):
        if move is None:
            print(f"Turn : {(self.turn+1)//2}\n{'Whites Move' if self.turn % 2 == 1 else 'Blacks Move'}")
            return input("Enter your move : ")
        return move


    def isDisambiguated(self, move):
        pass


    def listLegalMoves(self, Check = True):
        
        if self.inCheck(self.turn + 1, self.board):
            print(f"illegal board : turn {'white' if self.turn % 2 == 1 else 'black'}")
            self.display(self.board)
            raise Exception("Illegal board given")
        
        legal_moves = []

        current_pieces = self.getPieces(self.turn)
        for i, piece in enumerate(current_pieces):
                    row, column = piece.y, piece.x
                    moves = []# list of all the possible moves a piece can make
                    pawn = False# was it a pawn that moves
                    if self.board[row][column].code == constants.PAWN_CODE:# sets pawn to be true that it is a piece checked
                        pawn = True
                        moves = self.board[row][column].list_moves(self.board, row, column, self.board[row][column].player)
                    else:
                        moves = self.board[row][column].list_moves(row, column)
                    for move in moves:
                        spacesMovedX = move[1] - column
                        spacesMovedY = move[0] - row
                        if not(spacesMovedX == spacesMovedY and spacesMovedY == 0) and Legal_checker.legalRangeMove(self.board, move[1], move[0]) and piece.legal(self.board, row, column, spacesMovedX, spacesMovedY, piece.player, piece.moved):# check if the move is legal
                            if self.board[move[0]][move[1]].symbol == constants.EMPTY_CELL or Legal_checker.legalTaking(self.board, self.turn, move[1], move[0], pawn=pawn):# if it would take a piece is it legal
                                if pawn and ((self.turn % 2 == 1 and move[0] == 0) or (self.turn % 2 == 0 and move[0] == 7)):
                                        for promoted_piece in ["R", "N", "B", "Q"]:
                                            legal, temp_move = self.add_new_move(piece, self.turn, move, row, column, Check, promotion=promoted_piece)
                                            if legal:
                                                legal_moves.append(temp_move)  
                                else:   
                                    legal, temp_move = self.add_new_move(piece, self.turn, move, row, column, Check)
                                    if legal:
                                        legal_moves.append(temp_move)
        # all the moves that have been seen so far
        seen_moves = []
        for i in range(len(legal_moves)):# loop through all the legal moves
            key_data = legal_moves[i][0:2] + [legal_moves[i][7]]# get the data that is shown for the move
            for j in range(0, i):# loop through the previous moves to find the duplicates
                if seen_moves[j] == key_data:
                    prev_move = legal_moves[j]
                    if not (prev_move[2][0] == legal_moves[i][2][0]):# if the y coordinates are different
                        legal_moves[j][10] = True# disambiguate Y
                        legal_moves[i][10] = True
                    elif not (prev_move[2][1] == legal_moves[i][2][1]):# if the x coordinates are different
                        legal_moves[j][11] = True# disambiguate X
                        legal_moves[i][11] = True
                    else:
                        print(seen_moves)
                        print(legal_moves)
                        print("Conflict move:", legal_moves[i], prev_move)
                        raise Exception("Duplicate move found that cannot be disambiguated")
            seen_moves.append(key_data)


        # sort the moves by score for minimax
        legal_moves.sort(key=lambda x: x[9], reverse=True)
        # add castling moves after so sorting works
        if Legal_checker.legalShortCastle(self.board, self.turn):# check if you can short castle
            self.shortCastle(save_history=True)
            if not self.inCheck(self.turn + 1, self.board):
                legal_moves.insert(0, "0-0")
                if self.inCheck(self.turn + 2, self.board):
                    if len(self.listLegalMoves(Check=True)) == 0:# check if the check is mate
                        legal_moves[0] += "#"
                    else:
                        legal_moves[0] += "+"
                #elif len(self.listLegalMoves(Check=True)) == 0:# check for stalemate
                #    legal_moves[0] += "-"
            self.undoShortCastle()
        if Legal_checker.legalLongCastle(self.board, self.turn):# check if you can long castle
            self.longCastle(save_history=True)
            if not self.inCheck(self.turn + 1, self.board):
                legal_moves.insert(0, "0-0-0")
                if self.inCheck(self.turn + 2, self.board):
                    if len(self.listLegalMoves(Check=True)) == 0:# check if the check is mate
                        legal_moves[0] += "#"
                    else:
                        legal_moves[0] += "+"
                #elif len(self.listLegalMoves(Check=True)) == 0:# check for stalemate
                #    legal_moves[0] += "-"
            self.undoLongCastle()
        return legal_moves


    def add_new_move(self, piece, turn, move, row, column, check, promotion = None):
        is_check = False
        is_checkmate = False
        is_stalemate = False
        disambiguateX = False
        disambiguateY = False
        legal = True
        attacked_piece = self.board[move[0]][move[1]]
        taking = (piece.code == constants.PAWN_CODE and attacked_piece.code == constants.SHADOW_PAWN_CODE and attacked_piece.player != piece.player) or attacked_piece.symbol != constants.EMPTY_CELL
        if check:
            self.movePiece(move[0], move[1], row, column, turn, promotion=promotion, taking=taking, saveHistory=True)# one second delay depth 3
            if self.inCheck(turn, self.board):# one second delay depth 3
                legal = False
            elif self.inCheck(turn + 1, self.board):
                    if len(self.listLegalMoves(Check=True)) == 0:# check if the check is mate
                        is_checkmate = True
                    else:
                        is_check = True
            if (len(self.White_pieces) == 1 and len(self.Black_pieces) == 1) or self.mandatory_move_delay >= 50:# check for stalemate
                is_stalemate = True
            self.undoMove(self.board[move[0]][move[1]])# one second delay depth 3

        # score the move for sorting so minimax is more efficient
        score = 0
        if is_checkmate:
            score = math.inf
        elif is_check:
            score = 100
        elif is_stalemate:
            score = 50
        else:
            if taking:
                score += attacked_piece.value / piece.value
            if promotion:
                score += 10
        return legal, [piece.code, move, [row, column], is_check, is_checkmate, is_stalemate, False, promotion, taking, score, disambiguateY, disambiguateX]


    def playStep(self, code):
        self.move_time = 0
        code = self.decode_checks(code)
        castled = self.decode_castle(code)
        if not(castled):
            endXCoor, endYCoor, startXCoor, startYCoor, promotion, taking = self.decode(code, self.board, self.turn)
            self.movePiece(endYCoor, endXCoor, startYCoor, startXCoor, self.turn, promotion=promotion, taking=taking)
        done = self.gameEnd(self.board, self.turn)# whether the game is over

        return done


    def play(self):
        done = False
        while not done:
            self.display(self.board)
            legal = False
            self.legal_moves = [self.encode(i) if not  i[0] == "0" else i for i in self.listLegalMoves()]
            print(self.legal_moves)
            
            while legal == False:
                code = self.moveInput()
                if code in self.legal_moves:
                    legal = True
            done = self.playStep(code)
        self.display(self.board)


    def inCheck(self, turn, board):
        pieces = self.getPieces(turn)
        x, y = -1, -1
        for piece in pieces:# loop through all the pieces to find the king
            if piece.code == constants.KING_CODE:
                y, x = piece.y, piece.x
        
        if x == -1 or y == -1:
            self.display(self.board)
            raise Exception("king not found")

        return self.checkCheck(y, x, opposing_player="B" if turn % 2 == 1 else "W", board=board, turn=turn)


    def gameEnd(self, board, turn):
        if self.winner is not None or self.drawn:# if the game is over
            return True
        return False


    def copy_board(self, board):
        return [[cell.clone() for cell in row] for row in board]# often causes a delay 10^-4
    
    def __str__(self):
        return "".join(j.code if j.code else "p" for i in self.board for j in i)

if __name__ == "__main__":
    game = chess()
    print(str(game))
    game.play()
