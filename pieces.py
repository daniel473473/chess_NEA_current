import constants
import Legal_checker
import chess_list_functions
import math
import helper_functions

class Piece:# the class used to create pieces
    
    def __init__(self, x, y, symbol, code, value, player, legal, listmoves, moved = False):
        self.x = x# the x coordinate of the piece on the board
        self.y = y# the coordinates of the piece on the board
        self.symbol = symbol# the symbol for the piece
        self.code = code# the code of the piece for moves
        self.value = value
        self.player = player# the player this piece belongs to 
        self.legal = legal# the function checking if the move was legal
        self.list_moves = listmoves# the function that returns a list of legal moves for the piece
        self.moved = moved# has the piece moved
        self.taken_history = helper_functions.Stack([])# the history of taken pieces
        self.position_history = helper_functions.Stack([])# the history of positions of the piece
        self.moved_history = helper_functions.Stack([])# the history of whether the piece has moved
 

    def move(self, x, y):# move the piece to a new position
        self.x = x
        self.y = y
        self.moved = True


    def undo_move(self):# undo the move of the piece
        self.x, self.y = self.position_history.pop()# get the last position
        self.moved = self.moved_history.pop()# get the last moved state
        last_taken = self.taken_history.pop()# get the last taken piece
        return self.x, self.y, last_taken


    def update_history(self, piece):# update the history of the piece
        # update histories
        self.set_next_taken(piece)
        self.position_history.push((self.x, self.y))
        self.moved_history.push(self.moved)


    def set_next_taken(self, piece):
         self.taken_history.push(piece)


    def get_next_taken(self):
         return self.taken_history.pop()


    def clone(self):
        return Piece(self.x, self.y, self.symbol, self.code, self.value, self.player, self.legal, self.list_moves, moved = self.moved)
    

    def __lt__(self, other):
         return self.value + self.x/10 + self.y/100 < other.value + other.x/10 + other.y/100
    

    def __gt__(self, other):
         return self.value + self.x/10 + self.y/100 > other.value + other.x/10 + other.y/100


    def __repr__(self):
        return self.code + " " + str(self.y) + " " + str(self.x)+ " " + self.player + " " + str(self.moved)
    

class Shadow_Pawn(Piece):# the class of the shadow pawn used for enpassant
        def __init__(self,
                        y,
                        x,
                        pawnrow,
                        pawncolumn,
                        player,
                        symbol = constants.EMPTY_CELL,
                        code = constants.SHADOW_PAWN_CODE,
                        legal = Legal_checker.legalEmptyMove,
                        listmoves = chess_list_functions.list_empty_moves,
                        moved=False,
                        created=True,
                        value=0):
                super().__init__(x, y, symbol, code, value, player, legal, listmoves, moved)
                self.pawn_row = pawnrow# the row of the pawn this links to
                self.pawn_column = pawncolumn# the column of the pawn this links to
                self.created = created# whether the piece has just been created


        def clone(self):
                return Shadow_Pawn(self.x, self.y, self.pawn_row, self.pawn_column, self.player, self.symbol, self.code, self.value, self.legal, moved=self.moved, created=self.created)


        def __repr__(self):
             return "shadow pawn "+ str(self.created) + " " + self.player + " " + str(self.y) + " " + str(self.x) + " " + str(self.pawn_row) + " " + str(self.pawn_column)


class Empty_Cell(Piece):# class of the empty cell
    def __init__(self,
                y,
                x,
                symbol = constants.EMPTY_CELL,
                code = constants.EMPTY_CODE,
                value = 0,
                player = "",
                legal = Legal_checker.legalEmptyMove,
                listmoves = chess_list_functions.list_empty_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class Pawn(Piece):# class of the white pawn
    def __init__(self, 
                y,
                x,
                player,
                symbol = constants.PAWN,
                code = constants.PAWN_CODE,
                value = 1,
                legal = Legal_checker.legalPawnMove,
                listmoves = chess_list_functions.list_pawn_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class Rook(Piece):# class of the white rook
    def __init__(self,
                y,
                x,
                player,
                symbol = constants.ROOK,
                code = constants.ROOK_CODE,
                value = 5,
                legal = Legal_checker.legalRookMove,
                listmoves = chess_list_functions.list_rook_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class Knight(Piece):# class of the white knight
    def __init__(self,
                y,
                x,
                player,
                symbol = constants.KNIGHT,
                code = constants.KNIGHT_CODE,
                value = 3,
                legal = Legal_checker.legalKnightMove,
                listmoves = chess_list_functions.list_knight_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class Bishop(Piece):# class of the white bishop
    def __init__(self,
                y,
                x,
                player,
                symbol = constants.BISHOP,
                code = constants.BISHOP_CODE,
                value = 3,
                legal = Legal_checker.legalBishopMove,
                listmoves = chess_list_functions.list_bishop_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class King(Piece):# class of the white king
    def __init__(self,
                y,
                x,
                player,
                symbol = constants.KING,
                code = constants.KING_CODE,
                value = 100000,
                legal = Legal_checker.legalKingMove,
                listmoves = chess_list_functions.list_king_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)


class Queen(Piece):# class of the white queen
    def __init__(self,
                y,
                x,
                player,
                symbol = constants.QUEEN,
                code = constants.QUEEN_CODE,
                value = 9,
                legal = Legal_checker.legalQueenMove,
                listmoves = chess_list_functions.list_queen_moves,
                moved=False):
        super().__init__(x, y, symbol, code, value, player, legal, listmoves,  moved)
