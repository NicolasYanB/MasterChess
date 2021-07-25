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

    def move(self, new_position):
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
