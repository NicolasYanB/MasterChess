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
        self.__en_passant_pawn = 0
        self.__history = []
        self.__fifty_moves_counter = 0

    @property
    def board(self):
        return self.__board

    @property
    def selected_piece(self):
        return self.__selected_piece

    @property
    def captured_pieces(self):
        return self.__captured_pieces

    @property
    def turn(self):
        return self.__turn

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
        return self.__get_valid_moves(self.__selected_piece)

    def __get_valid_moves(self, piece):
        piece_possible_moves = piece.get_possible_moves(self.__board)
        piece_valid_moves = []
        for move in piece_possible_moves:
            if not self.__let_king_vulnerable(piece, move):
                piece_valid_moves.append(move)
        en_passant = self.__get_pawn_en_passant()
        castling = self.__get_king_castling()
        if en_passant:
            piece_valid_moves.append(en_passant)
        if castling:
            piece_valid_moves += castling
        return piece_valid_moves

    def __get_pawn_en_passant(self):
        if self.__selected_piece.type != "pawn":
            return False
        column, line = self.__selected_piece.position
        for delta in (1, -1):
            verified_column = column + delta
            if verified_column < 0 or verified_column > 7:
                continue
            if not self.__board.is_empty(verified_column, line):
                piece = self.__board.get(verified_column, line)
                if piece == self.__en_passant_pawn:
                    vertical_direction = self.__selected_piece.direction
                    en_passant_move = verified_column, line + vertical_direction
                    if self.__let_king_vulnerable(self.__selected_piece, en_passant_move):
                        return False
                    return en_passant_move
        return False

    def __get_king_castling(self):
        if self.__selected_piece.type != "king" or self.__selected_piece.moved:
            return False
        if self.__selected_piece.in_check:
            return False
        king = self.__selected_piece
        castling_moves = []
        column, line = self.__selected_piece.position
        for delta in (1, -1):
            current_column = column
            while True:
                current_column += delta
                if current_column == 0 or current_column == 7:
                    castling_column = column + 2 * delta
                    if self.__let_king_vulnerable(king, (castling_column - 1 * delta, line)):
                        break
                    if self.__let_king_vulnerable(king, (castling_column, line)):
                        break
                    if self.__board.is_empty(current_column, line):
                        break
                    piece = self.__board.get(current_column, line)
                    if piece.color != king.color or piece.type != "rook" or piece.moved:
                        break
                    castling_moves.append((castling_column, line))
                    break
                if not self.__board.is_empty(current_column, line):
                    break
        return castling_moves

    def __let_king_vulnerable(self, piece, move):
        from copy import deepcopy
        board_copy = deepcopy(self.__board)
        column, line = piece.position
        piece_copy = board_copy.get(column, line)
        if piece_copy.type == "pawn" and self.__en_passant_pawn != 0:
            if move[1] == self.__en_passant_pawn.position[1] + piece_copy.direction:
                board_copy.remove(self.__en_passant_pawn)
        board_copy.remove(*move)
        board_copy.move(piece_copy, move)
        ally_king = board_copy.get_all("king", piece_copy.color)[0]
        return self.__is_in_check(ally_king, board_copy)

    def move_selected_piece(self, destination):
        self.__fifty_moves_counter += 0.5
        selected_piece_possible_moves = self.get_selected_piece_moves()
        if destination not in selected_piece_possible_moves:
            raise InvalidMoveException("This piece can't be moved to this position")
        if not self.__board.is_empty(*destination):
            self.__fifty_moves_counter = 0
            self.__history = []
            self.__capture_movement(destination)
        if self.__selected_piece.type == "pawn":
            self.__fifty_moves_counter = 0
            self.__history = []
            if self.__en_passant_pawn != 0:
                self.__en_passant_movement(destination)
        if self.__selected_piece.type == "king":
            self.__castling_movement(destination)
        if self.__is_susceptible_to_en_passant(self.__selected_piece, destination):
            self.__en_passant_pawn = self.__selected_piece
        else:
            self.__en_passant_pawn = 0
        self.__board.move(self.__selected_piece, destination)
        self.__selected_piece.moved = True
        self.__turn = "black" if self.__turn == "white" else "white"

    def post_movement_actions(self):
        kings = self.__board.get_all("king")
        for king in kings:
            if self.__is_in_check(king, self.__board):
                king.in_check = True
                continue
            king.in_check = False
        game_status = self.__get_board_status()
        self.__history.append(game_status)
        return self.__get_game_status()

    def __get_game_status(self):
        if self.__is_checkmate():
            return 1
        if self.__is_stalemate():
            return 2
        if self.__is_threefold_repetition():
            return 3
        if self.__fifty_moves_counter == 50:
            return 4
        return 0

    def __is_checkmate(self):
        pieces = self.__board.get_all_of(self.__turn)
        king = self.__board.get_all("king", self.__turn)[0]
        for piece in pieces:
            if len(self.__get_valid_moves(piece)) > 0:
                return False
        return self.__is_in_check(king, self.__board)

    def __is_stalemate(self):
        pieces = self.__board.get_all_of(self.__turn)
        for piece in pieces:
            if len(self.__get_valid_moves(piece)) > 0:
                return False
        return True

    def __is_threefold_repetition(self):
        if len(self.__history) < 3:
            return False
        actual_status = self.__history[-1]
        repetitions = 0
        for game_status in self.__history[:-1]:
            if game_status == actual_status:
                repetitions += 1
            if repetitions == 2:
                return True
        return False

    def __capture_movement(self, move_position):
        captured_piece = self.__board.get(*move_position)
        self.__captured_pieces.append(captured_piece)
        self.__board.remove(*move_position)

    def __en_passant_movement(self, move_position):
        pawn_direction = self.__selected_piece.direction
        if move_position[1] == self.__en_passant_pawn.position[1] + pawn_direction:
            self.__captured_pieces.append(self.__en_passant_pawn)
            self.__board.remove(self.__en_passant_pawn)
            self.__en_passant_pawn = 0

    def __castling_movement(self, move_position):
        move_delta = self.__selected_piece.position[0] - move_position[0]
        if abs(move_delta) == 2:
            castling_rook = self.__find_castling_rook(move_position)
            direction = move_delta//abs(move_delta)
            rook_movement = move_position[0] + direction, move_position[1]
            self.__board.move(castling_rook, rook_movement)

    def __find_castling_rook(self, king_destination):
        column, line = king_destination
        if column == 2:
            rook_column = 0
        if column == 6:
            rook_column = 7
        rook = self.__board.get(rook_column, line)
        return rook

    def __is_susceptible_to_en_passant(self, piece, move):
        if piece.type != "pawn":
            return False
        if piece.moved:
            return False
        piece_line = piece.position[1]
        move_line = move[1]
        return abs(piece_line - move_line) == 2

    def __is_in_check(self, king, board):
        enemy_color = "black" if king.color == "white" else "white"
        enemy_pieces = board.get_all_of(enemy_color)
        for piece in enemy_pieces:
            if king.position in piece.get_possible_moves(board):
                return True
        return False

    def get_king_in_check(self):
        kings = self.__board.get_all("king")
        for king in kings:
            if king.in_check:
                return king
        return 0

    def __get_board_status(self):
        pieces = self.__board.get_all_pieces()
        game_status = []
        for piece in pieces:
            line = f"{piece.color} {piece.type} {len(self.__get_valid_moves(piece))}"
            game_status.append(line)
        return ' '.join(game_status)


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
        self.__board[column][line] = None

    @dispatch(object)
    def remove(self, piece):
        column, line = piece.position
        if self.is_empty(column, line):
            raise ValueError("piece not in board")
        self.__board[column][line] = None
