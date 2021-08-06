from multipledispatch import dispatch


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
            raise IndexError("There is already an object in this index")
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

    def move(self, piece, destination):
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
