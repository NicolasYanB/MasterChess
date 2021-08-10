import unittest
from source import Game


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


if __name__ == '__main__':
    unittest.main()
