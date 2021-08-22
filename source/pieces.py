class Piece:
    def __init__(self, type, color, position):
        self._type = type
        self._color = color
        self._position = position
        self._image = f"images/pieces/{color}/{type}.png"
        self.moved = False

    @property
    def type(self):
        return self._type

    @property
    def color(self):
        return self._color

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def image(self):
        return self._image

    def get_possible_moves(self):
        # Get all moves that a piece can make in its actual position
        # without considering other pieces that are on the board
        pass

    def _is_possible(self, move):
        move_column, move_line = move
        column, line = self._position
        if move_column > 7 or move_column < 0:
            return False
        if move_line > 7 or move_line < 0:
            return False
        if (move_column, move_line) == (column, line):
            return False
        return True


class Pawn(Piece):
    initial_positions = {"white": [(i, 6) for i in range(8)],
                         "black": [(i, 1) for i in range(8)]}

    def __init__(self, color, position):
        type = "pawn"
        super().__init__(type, color, position)
        self.__direction = -1 if color == "white" else 1

    @property
    def direction(self):
        return self.__direction

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        normal_move = column, line + self.__direction
        if self._is_possible(normal_move) and board.is_empty(*normal_move):
            moves.append(normal_move)
            double_move = column, line + self.__direction * 2
            if not self.moved and self._is_possible(double_move) and board.is_empty(*double_move):
                moves.append(double_move)
        for x in (1, -1):
            capture_move = column + x, line + self.__direction
            if self._is_possible(capture_move) and not board.is_empty(*capture_move):
                piece = board.get(*capture_move)
                if piece.color != self._color:
                    moves.append(capture_move)
        return moves


class Knight(Piece):
    initial_positions = {"white": [(1, 7), (6, 7)],
                         "black": [(1, 0), (6, 0)]}

    def __init__(self, color, position):
        type = "knight"
        super().__init__(type, color, position)

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        deltas = [(-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
        for x, y in deltas:
            move = column + x, line + y
            if not self._is_possible(move):
                continue
            if not board.is_empty(*move):
                piece = board.get(*move)
                if piece.color == self._color:
                    continue
            moves.append(move)
        return moves


class Rook(Piece):
    initial_positions = {"white": [(0, 7), (7, 7)],
                         "black": [(0, 0), (7, 0)]}

    def __init__(self, color, position):
        type = "rook"
        super().__init__(type, color, position)

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for x, y in directions:
            current_column, current_line = column, line
            while True:
                current_column += x
                current_line += y
                move = current_column, current_line
                if not self._is_possible(move):
                    break
                if not board.is_empty(*move):
                    piece = board.get(*move)
                    if piece.color != self._color:
                        moves.append(move)
                    break
                moves.append(move)
        return moves


class Bishop(Piece):
    initial_positions = {"white": [(2, 7), (5, 7)],
                         "black": [(2, 0), (5, 0)]}

    def __init__(self, color, position):
        type = "bishop"
        super().__init__(type, color, position)

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for x, y in directions:
            current_column, current_line = column, line
            while True:
                current_column += x
                current_line += y
                move = current_column, current_line
                if not self._is_possible(move):
                    break
                if not board.is_empty(*move):
                    piece = board.get(*move)
                    if piece.color != self._color:
                        moves.append(move)
                    break
                moves.append(move)
        return moves


class Queen(Piece):
    initial_positions = {"white": [(3, 7)],
                         "black": [(3, 0)]}

    def __init__(self, color, position):
        type = "queen"
        super().__init__(type, color, position)

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for x, y in directions:
            current_column, current_line = column, line
            while True:
                current_column += x
                current_line += y
                move = current_column, current_line
                if not self._is_possible(move):
                    break
                if not board.is_empty(*move):
                    piece = board.get(*move)
                    if piece.color != self._color:
                        moves.append(move)
                    break
                moves.append(move)
        return moves


class King(Piece):
    initial_positions = {"white": [(4, 7)],
                         "black": [(4, 0)]}

    def __init__(self, color, position):
        type = "king"
        super().__init__(type, color, position)
        self.in_check = False

    def get_possible_moves(self, board):
        column, line = self._position
        moves = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                move = column + x, line + y
                if not self._is_possible(move):
                    continue
                if not board.is_empty(*move):
                    piece = board.get(*move)
                    if piece.color == self._color:
                        continue
                moves.append(move)
        return moves
