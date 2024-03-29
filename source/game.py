from multipledispatch import dispatch

from source import Pawn, Knight, Rook, Bishop, Queen, King


class TurnError(Exception):
    pass


class InvalidMoveException(Exception):
    pass


class Game:
    """
    Class that handle the game logic

    Responsible for things like move validation, test whether a pawn can make an en passant,
    check if any king is in check, and more.

    Attributes:
        board (game.Board): object that handle the pieces positions on the board
        selected_piece (piece.Piece): piece selected by the user
        captured_pieces (Dict[str, List[piece.Piece]]): pieces that was captured sorted by color
        turn (str): player that makes the next move
        en_passant_pawn (piece.Piece): pawn that can suffer en passant on the next turn
        history (List[str]): stores board states that are relevant to check whether threefold
            repetition occurred or not
        fifty_moves_counter (int): count how much moves occurred without a pawn movement or a
            capture
    """
    def __init__(self):
        self.__board = Board()
        self.__selected_piece = None
        self.__captured_pieces = {"white": [], "black": []}
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

    def init_new_game_board(self):
        """Initialize a board with all pieces in their initial positions"""
        piece_classes = [Pawn, Knight, Rook, Bishop, Queen, King]
        for color in ("white", "black"):
            for piece_class in piece_classes:
                for position in piece_class.initial_positions[color]:
                    piece = piece_class(color, position)
                    self.__board.add(piece)

    def load_saved_game_board(self, game_state):
        """
        Initialize a board of a game that didn't end

        Args:
            game_state (List[object]): list of pieces of information about the game
        """
        piece_classes = {"pawn": Pawn, "knight": Knight, "rook": Rook,
                         "bishop": Bishop, "queen": Queen, "king": King}
        turn = game_state[-3]
        captured_pieces = game_state[-1]
        self.__captured_pieces = captured_pieces
        self.__turn = turn
        # Adding pieces to the board
        pieces = game_state[:-3]
        for piece_data in pieces:
            piece_info = piece_data.split()
            color, piece_type = piece_info[:2]
            position = int(piece_info[2]), int(piece_info[3])
            moved = eval(piece_info[-1])
            piece_class = piece_classes[piece_type]
            piece = piece_class(color, position)
            piece.moved = moved
            self.__board.add(piece)
        # Check if there's a pawn that can suffer an en passant
        en_passant = game_state[-2]
        if en_passant != 0:
            column, line = en_passant
            en_passant_pawn = self.__board.get(column, line)
            self.__en_passant_pawn = en_passant_pawn
        # Check if one of the kings is in check
        kings = self.__board.get_all("king")
        for king in kings:
            if self.__is_in_check(king):
                king.in_check = True
                break

    def select_piece(self, column, line):
        """
        Put a piece in given column and line as the selected pieces

        Args:
            column (int): column which the piece is positioned
            line (int): line which the piece is positioned
        """
        if self.__board.is_empty(column, line):
            raise ValueError("There's not a piece in this position")
        piece = self.__board.get(column, line)
        if piece.color != self.__turn:
            raise TurnError("Can't select an opponent piece")
        self.__selected_piece = piece

    def unselect(self):
        self.__selected_piece = None

    def get_selected_piece_moves(self):
        """
        Returns a list of int tuples of 2 elements. The first element is the column, the second is
        the line of the square that the piece can move to
        """
        return self.__get_valid_moves(self.__selected_piece)

    def __get_valid_moves(self, piece):
        """
        Get all the valid moves that a given piece can make

        Args:
            piece (piece.Piece)

        Returns:
            list of int tuples of 2 elements. The first element is the column, the second is the
            line of the square that the piece can move to. For example:

            [(1, 1), (1, 2), (2, 1)]
        """
        # Remove moves that would let king in check from get_possible_moves
        # and add castling or en passant if is necessary
        piece_possible_moves = piece.get_possible_moves(self.__board)
        piece_valid_moves = []
        for move in piece_possible_moves:
            if not self.__let_king_vulnerable(piece, move):
                piece_valid_moves.append(move)
        en_passant = self.__get_en_passant(piece)
        castling = self.__get_castling(piece)
        if en_passant:
            piece_valid_moves.append(en_passant)
        if castling:
            piece_valid_moves += castling
        return piece_valid_moves

    def __get_en_passant(self, piece):
        """
        Returns True if the piece can make an en passant on the next move. And returns false if
        the piece cannot or isn't a pawn

        Args:
            piece (piece.Piece)
        """
        if piece.type != "pawn":
            return False
        column, line = piece.position
        for delta in (1, -1):
            verified_column = column + delta
            if verified_column < 0 or verified_column > 7:
                continue
            if not self.__board.is_empty(verified_column, line):
                adjacent_piece = self.__board.get(verified_column, line)
                if adjacent_piece == self.__en_passant_pawn:
                    vertical_delta = piece.direction
                    en_passant_move = verified_column, line + vertical_delta
                    if self.__let_king_vulnerable(piece, en_passant_move):
                        return False
                    return en_passant_move
        return False

    def __get_castling(self, piece):
        """
        Returns True if the piece can make a castle. Returns False if the piece cannot or isn't
        the king

        Args:
            piece (piece.Piece)
        """
        if piece.type != "king" or piece.moved:
            return False
        if piece.in_check:
            return False
        king = piece
        castling_moves = []
        column, line = piece.position
        for delta in (1, -1):
            current_column = column
            while True:
                current_column += delta
                if current_column == 0 or current_column == 7:
                    castling_column = column + 2 * delta
                    castling_steps = (castling_column - 1 * delta, line), (castling_column, line)
                    # Check if the king would pass through an attacked square while castling
                    if any(self.__let_king_vulnerable(king, step) for step in castling_steps):
                        break
                    if self.__board.is_empty(current_column, line):
                        break
                    piece = self.__board.get(current_column, line)
                    if piece.color != king.color or piece.type != "rook" or piece.moved:
                        break
                    castling_moves.append((castling_column, line))
                    break
                # Check if there's any piece before the last/first column
                if not self.__board.is_empty(current_column, line):
                    break
        return castling_moves

    def __let_king_vulnerable(self, piece, move):
        """
        Check if the king would de in check if piece make a given move

        Args:
            piece (Piece.piece)
            move (Tuple[int, int]): position of the move that would be performed by piece

        Returns:
            A boolean value that represents whether the king would be in check after this move
        """
        # Create a copy of the board to simulate the move and check if the king would be
        # in check after it
        from copy import deepcopy
        board_copy = deepcopy(self.__board)
        column, line = piece.position
        piece_copy = board_copy.get(column, line)
        if piece_copy.type == "pawn" and self.__en_passant_pawn != 0:
            # If the move is an en passant, remove en passant pawn
            if move[1] == self.__en_passant_pawn.position[1] + piece_copy.direction:
                board_copy.remove(self.__en_passant_pawn)
        move_column, move_line = move
        board_copy.remove(move_column, move_line)
        board_copy.move(piece_copy, move)
        ally_king = board_copy.get_all("king", color=piece_copy.color)[0]
        return self.__is_in_check(ally_king, board=board_copy)

    def move_selected_piece(self, destination):
        """
        Perform the movement of the selected piece to a given destination

        Args:
            destination (Tuple[int, int]): square that the selected piece will move to
        """
        self.__fifty_moves_counter += 0.5
        selected_piece_valid_moves = self.__get_valid_moves(self.__selected_piece)
        if destination not in selected_piece_valid_moves:
            raise InvalidMoveException("This piece can't be moved to this position")
        dest_column, dest_line = destination
        if not self.__board.is_empty(dest_column, dest_line):
            self.__fifty_moves_counter = 0
            self.__history = []  # After a capture any state before it can't be repeated
            self.__capture(destination)
        if self.__selected_piece.type == "pawn":
            self.__fifty_moves_counter = 0
            self.__history = []  # After a pawn move any state before it can't be repeated
            if self.__en_passant_pawn != 0:
                self.__en_passant(destination)
        if self.__selected_piece.type == "king" and not self.__selected_piece.moved:
            self.__castling(destination)
        if self.__is_susceptible_to_en_passant(self.__selected_piece, destination):
            self.__en_passant_pawn = self.__selected_piece
        else:
            self.__en_passant_pawn = 0
        self.__board.move(self.__selected_piece, destination)
        self.__selected_piece.moved = True
        self.__turn = "black" if self.__turn == "white" else "white"

    def __capture(self, move_position):
        """
        Remove the piece on the given position and add it to the captured_pieces list

        Args:
            move_position (Tuple[int, int]): position of the deleted piece
        """
        column, line = move_position
        captured_piece = self.__board.get(column, line)
        self.__captured_pieces[captured_piece.color].append(captured_piece.type)
        self.__board.remove(column, line)

    def __en_passant(self, move_position):
        """
        Check if the movement performed is an en passant. If it is, remove en_passant_pawn and
        append it to the captured pieces list

        Args:
            move_position (Tuple[int, int]): position that selected_piece will move to
        """
        pawn_column, pawn_line = self.__selected_piece.position
        en_passant_pawn = self.__en_passant_pawn
        en_passant_pawn_column, en_passant_pawn_line = en_passant_pawn.position
        is_adjacent = abs(pawn_column - en_passant_pawn_column) == 1
        pawn_direction = self.__selected_piece.direction
        move_is_above_en_passant_pawn = en_passant_pawn_line + pawn_direction == move_position[1]
        if pawn_line == en_passant_pawn_line and is_adjacent and move_is_above_en_passant_pawn:
            self.__captured_pieces[self.__en_passant_pawn.color].append(self.__en_passant_pawn.type)
            self.__board.remove(self.__en_passant_pawn)
            self.__en_passant_pawn = 0

    def __castling(self, move_position):
        """
        Check if the movement performed is a castle. If it is, move the castle rook to it's
        correspondent position

        Args:
            move_position (Tuple[int, int]): position that selected_piece will move to
        """
        # Do the castling if the distance between the king and the point to move is 2
        move_delta = self.__selected_piece.position[0] - move_position[0]
        distance = abs(self.__selected_piece.position[0] - move_position[0])
        if distance == 2:
            # Once this move was validated by the __get_valid_moves method we already know
            # that all conditions have been met
            castling_rook = self.__find_castling_rook(move_position)
            direction = move_delta//abs(move_delta)
            rook_movement = move_position[0] + direction, move_position[1]
            self.__board.move(castling_rook, rook_movement)

    def post_movement_actions(self):
        """
        Game processes that occurs after the move:
            - Check if any king is in check
            - store the current game board state
            - check if the game ended

        Returns:
            True if the game has ended (in draw or with one player winning), otherwise,
            return False
        """
        kings = self.__board.get_all("king")
        for king in kings:
            if self.__is_in_check(king):
                king.in_check = True
                continue
            king.in_check = False
        game_status = self.__get_board_state()
        self.__history.append(game_status)
        return self.__get_game_status()

    def __get_game_status(self):
        """
        Return 0 if the game didn't end, otherwise, return other number between 1 and 5
        depending on how the game ended
        """
        if self.__is_checkmate():
            return 1
        if self.__is_stalemate():
            return 2
        if self.__is_threefold_repetition():
            return 3
        if self.__fifty_moves_counter == 50:
            return 4
        if self.__is_insufficient_material():
            return 5
        return 0

    def __is_checkmate(self):
        """Return True if any king suffered a check mate"""
        pieces = self.__board.get_all_where(color=self.__turn)
        king = self.__board.get_all("king", color=self.__turn)[0]
        for piece in pieces:
            if len(self.__get_valid_moves(piece)) > 0:
                return False
        if self.__is_in_check(king):
            return True
        return False

    def __is_stalemate(self):
        """Return True if any king suffered a stealmete"""
        pieces = self.__board.get_all_where(color=self.__turn)
        for piece in pieces:
            if len(self.__get_valid_moves(piece)) > 0:
                return False
        return True

    def __is_threefold_repetition(self):
        """Return true if the current board state occurred twice before"""
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

    def __is_insufficient_material(self):
        """Return True if any player don't have pieces enough to make a checkmate"""
        white_pieces = self.__board.get_all_where(color="white")
        black_pieces = self.__board.get_all_where(color="black")
        all_pieces = white_pieces + black_pieces
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            # Only king in both sides
            return True
        if len(white_pieces) == 2 and len(black_pieces) == 1:
            if any([piece.type == "knight" for piece in white_pieces]):
                # White player have a king and a knight, black player only have a king
                return True
        if len(black_pieces) == 2 and len(white_pieces) == 1:
            if any([piece.type == "knight" for piece in black_pieces]):
                # Black player have a king and a knight, white player only have a king
                return True
        bishops = [piece for piece in all_pieces if piece.type == "bishop"]
        if len(bishops) != len(all_pieces)-2:
            # Return false if there's any piece other than bishops, besides the kings
            return False
        get_bishop_square_color = lambda c, l: "white" if c % 2 == l % 2 else "black"
        square_colors = [get_bishop_square_color(*bishop.position) for bishop in bishops]
        if len(set(square_colors)) == 1:
            # All bishops are in the same square color
            return True
        return False

    def __find_castling_rook(self, king_destination):
        """
        Return the rook that will be moved on castle given the king final destination.

        Args:
            king_destination (Tuple[int, int]): king position after the castle

        Returns:
            a rook object (pieces.Rook)
        """
        column, line = king_destination
        if column == 2:
            rook_column = 0
        if column == 6:
            rook_column = 7
        rook = self.__board.get(rook_column, line)
        return rook

    def __is_susceptible_to_en_passant(self, piece, move):
        """
        Return True if a given piece is a pawn and can suffer an en passant during the next
        opponent turn.

        Args:
            piece (pieces.Piece): piece that will be moved
            move (Tuple[int, int]): movement that the piece will make
        """
        if piece.type != "pawn":
            return False
        if piece.moved:
            return False
        piece_line = piece.position[1]
        move_line = move[1]
        distance_travelled = abs(piece_line - move_line)
        return distance_travelled == 2

    def __is_in_check(self, king, board=None):
        """
        Return True the given king is in check.

        Args:
            king (pieces.King): king that maybe is in check
            board (game.Board): board object that contains the king. Defaults to None
        """
        if board is None:
            board = self.__board
        enemy_color = "black" if king.color == "white" else "white"
        enemy_pieces = board.get_all_where(color=enemy_color)
        for piece in enemy_pieces:
            if king.position in piece.get_possible_moves(board):
                return True
        return False

    def get_king_in_check(self):
        """
        Return the king in check or 0 if there isn't any.
        """
        kings = self.__board.get_all("king")
        for king in kings:
            if king.in_check:
                return king
        return 0

    def get_game_data(self):
        """
        Returns a list with all the information necessary to save the game. And it have
        the following structure:
            [all pieces in the board (color, type, column, line, number of valid moves, moved),
            turn player, en passant pawn, captured pieces]
        """
        game = self.__get_board_state()
        turn_player = self.__turn
        en_passant = 0
        if self.__en_passant_pawn != 0:
            en_passant_column, en_passant_line = self.__en_passant_pawn.position
            en_passant = en_passant_column, en_passant_line
        game.append(turn_player)
        game.append(en_passant)
        game.append(self.__captured_pieces)
        return str(game)

    def __get_board_state(self):
        pieces = self.__board.get_all_pieces()
        game_status = []
        for piece in pieces:
            column, line = piece.position
            amount_of_moves = len(self.__get_valid_moves(piece))
            line = f"{piece.color} {piece.type} {column} {line} {amount_of_moves} {piece.moved}"
            game_status.append(line)
        return game_status

    def promote(self, promoted_piece, new_piece):
        self.__board.remove(promoted_piece)
        self.__board.add(new_piece)
        self.__history = []


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

    def get_all_where(self, color):
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
