class Piece:
    def __init__(self, type, color, position):
        self._type = type
        self._color = color
        self._position = position
        self._image = f"images/pieces/{color}/{type}"
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

    @property
    def image(self):
        return self._image

    def move_to(self, new_position):
        self._position = new_position

    def get_possible_moves(self):
        pass

    def _is_possible(self, move):
        move_column, move_line = move
        column, line = self._position
        if move_column > 7 or move_column < 0:
            return False
        if move_line > 7 or move_line < 0:
            return False
        if move_column == column and move_line == line:
            return False
        return True


class Pawn(Piece):
    initial_positions = {"white": [(i, 6) for i in range(8)],
                         "black": [(i, 1) for i in range(8)]}

    def __init__(self, color, position):
        type = "pawn"
        super().__init__(type, color, position)
        self.__direction = -1 if color == "white" else 1

    def get_possible_moves(self):
        column, line = self._position
        moves = []
        normal_move = column, line + self.__direction
        double_square_move = column, line + self.__direction * 2
        captures = [(column + i, line + self.__direction) for i in (1, -1)]
        moves += [capture for capture in captures if self._is_possible(capture)]
        moves.append(normal_move) if self._is_possible(normal_move) else 0
        if not self.moved:
            moves.append(double_square_move) if self._is_possible(double_square_move) else 0
        return moves


class Knight(Piece):
    initial_positions = {"white": [(1, 7), (6, 7)],
                         "black": [(1, 0), (6, 0)]}

    def __init__(self, color, position):
        type = "knight"
        super().__init__(type, color, position)

    def get_possible_moves(self):
        column, line = self._position
        moves = []
        deltas = [(-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
        for x, y in deltas:
            move = column + x, line + y
            moves.append(move) if self._is_possible(move) else 0
        return moves


class Rook(Piece):
    initial_positions = {"white": [(0, 7), (7, 7)],
                         "black": [(0, 0), (7, 0)]}

    def __init__(self, color, position):
        type = "rook"
        super().__init__(type, color, position)

    def get_possible_moves(self):
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
                moves.append(move)
        return moves


class Bishop(Piece):
    initial_positions = {"white": [(2, 7), (5, 7)],
                         "black": [(2, 0), (5, 0)]}

    def __init__(self, color, position):
        type = "bishop"
        super().__init__(type, color, position)

    def get_possible_moves(self):
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
                moves.append(move)
        return moves


class Queen(Piece):
    initial_position = {"white": (3, 7),
                        "black": (3, 0)}

    def __init__(self, color, position):
        type = "queen"
        super().__init__(type, color, position)

    def get_possible_moves(self):
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
                moves.append(move)
        return moves
