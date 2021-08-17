import unittest
from source import Game, TurnError, InvalidMoveException


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_load_board(self):
        print("test_load_board")
        self.game.load_board()
        pieces = {
            "white": {
                "pawn": [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)],
                "rook": [(0, 7), (7, 7)],
                "knight": [(1, 7), (6, 7)],
                "bishop": [(2, 7), (5, 7)],
                "queen": [(3, 7)],
                "king": [(4, 7)]
                },
            "black": {
                "pawn": [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                "rook": [(0, 0), (7, 0)],
                "knight": [(1, 0), (6, 0)],
                "bishop": [(2, 0), (5, 0)],
                "queen": [(3, 0)],
                "king": [(4, 0)]
                }
            }
        for color in pieces:
            for piece in pieces[color]:
                for position in pieces[color][piece]:
                    self.assertFalse(self.game.board.is_empty(*position))
                    p = self.game.board.get(*position)
                    self.assertEqual(p.color, color)
                    self.assertEqual(p.type, piece)

    def test_select_piece(self):
        print("test_select_piece")
        self.game.load_board()
        self.game.select_piece(0, 6)
        self.assertEqual(self.game.selected_piece, self.game.board.get(0, 6))
        self.assertRaises(ValueError, self.game.select_piece, 0, 5)
        self.assertRaises(TurnError, self.game.select_piece, 0, 1)

    def test_unselect(self):
        print("test_unselect")
        self.game.load_board()
        self.game.select_piece(0, 6)
        self.game.unselect()
        self.assertIsNone(self.game.selected_piece)

    def test_get_selected_piece_moves(self):
        print("test_get_selected_piece_moves")
        self.game.load_board()
        self.game.select_piece(0, 6)
        self.assertEqual(self.game.get_selected_piece_moves(), [(0, 5), (0, 4)])
        self.game.unselect()
        self.game.select_piece(0, 7)
        self.assertEqual(self.game.get_selected_piece_moves(), [])

    def test_move_selected_piece(self):
        print("test_move_selected_piece")
        self.game.load_board()
        piece = self.game.board.get(0, 6)
        self.game.select_piece(0, 6)
        self.assertRaises(InvalidMoveException, self.game.move_selected_piece, (1, 5))
        self.game.move_selected_piece((0, 5))
        self.assertEqual(self.game.selected_piece, piece)


if __name__ == '__main__':
    unittest.main()
