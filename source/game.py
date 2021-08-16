from multipledispatch import dispatch
from source import Pawn, Knight, Rook, Bishop, Queen, King


class TurnError(Exception):
    pass


class InvalidMoveException(Exception):
    pass


class Game:
    def __init__(self):
        self.__board = Board()
        self.__selected_piece = None
        self.__captured_pieces = []
        self.__turn = "white"

    @property
    def board(self):
        return self.__board

    @property
    def selected_piece(self):
        return self.__selected_piece

    @property
    def captured_pieces(self):
        return self.__captured_pieces

    def load_board(self):
        piece_types = [Pawn, Knight, Rook, Bishop, Queen, King]
        for color in ("white", "black"):
            for type in piece_types:
                for position in type.initial_positions[color]:
                    piece = type(color, position)
                    self.__board.add(piece)

    def select_piece(self, column, line):
        if self.__board.is_empty(column, line):
            raise ValueError("There's not a piece in this position")
        piece = self.__board.get(column, line)
        if piece.color != self.__turn:
            raise TurnError("Can't select an opponent piece")
        self.__selected_piece = piece

    def unselect(self):
        self.__selected_piece = None

    def get_selected_piece_moves(self):
        return self.__selected_piece.get_possible_moves(self.__board)

    def move_selected_piece(self, destination):
        selected_piece_possible_moves = self.__selected_piece.get_possible_moves(self.__board)
        if destination not in selected_piece_possible_moves:
            raise InvalidMoveException("This piece can't be moved to this position")
        self.__board.move(self.__selected_piece, destination)
        self.__selected_piece.moved = True


class Board:
    def __init__(self):
        self.__board = [[None for column in range(8)] for line in range(8)]

    def __iter__(self):
        for line in range(8):
            for column in range(8):
                if self.is_empty(column, line):
                    continue
                piece = self.__board[column][line]
                yield piece

    def get(self, column, line):
        return self.__board[column][line]

    def is_empty(self, column, line):
        return self.__board[column][line] is None

    def add(self, piece):
        column, line = piece.position
        if not self.is_empty(column, line):
            raise IndexError("There is already an object in this position")
        self.__board[column][line] = piece

    def get_all_of(self, color):
        pieces = []
        for piece in self:
            if piece.color == color:
                pieces.append(piece)
        return pieces

    def get_all(self, piece_type, color=None):
        pieces = []
        for piece in self:
            if color is not None and piece.color != color:
                continue
            if piece.type == piece_type:
                pieces.append(piece)
        return pieces

    def get_all_pieces(self):
        return [piece for piece in self]

    def move(self, piece, destination):
        if piece.position == destination:
            raise ValueError("destination can't be the current piece position")
        piece_column, piece_line = piece.position
        self.remove(piece_column, piece_line)
        piece.position = destination
        self.add(piece)
        piece.moved = True

    @dispatch(int, int)
    def remove(self, column, line):
        if self.is_empty(column, line):
            raise IndexError("Can't remove from an empty position")
        self.__board[column][line] = None

    @dispatch(object)
    def remove(self, piece):
        column, line = piece.position
        if self.is_empty(column, line):
            raise ValueError("piece not in board")
        self.__board[column][line] = None
