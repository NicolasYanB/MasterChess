import unittest
from source import Rook


class TestRook(unittest.TestCase):
    def setUp(self):
        self.rook1 = Rook("white", (3, 4))
        self.rook2 = Rook("black", (4, 3))

    def test_get_possible_moves(self):
        # All moves available
        r1moves = self.rook1.get_possible_moves()
        r2moves = self.rook2.get_possible_moves()
        r1out = [(3, 3), (3, 2), (3, 1), (3, 0), (3, 5), (3, 6), (3, 7), (2, 4), (1, 4), (0, 4),
                 (4, 4), (5, 4), (6, 4), (7, 4)]
        r2out = [(4, 2), (4, 1), (4, 0), (4, 4), (4, 5), (4, 6), (4, 7), (3, 3), (2, 3), (1, 3),
                 (0, 3), (5, 3), (6, 3), (7, 3)]
        self.assertEqual(r1moves, r1out)
        self.assertEqual(r2moves, r2out)
        # Piece on a corner
        self.rook1.move_to((0, 0))
        self.rook2.move_to((7, 7))
        r1moves = self.rook1.get_possible_moves()
        r2moves = self.rook2.get_possible_moves()
        r1out = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0),
                 (4, 0), (5, 0), (6, 0), (7, 0)]
        r2out = [(7, 6), (7, 5), (7, 4), (7, 3),  (7, 2), (7, 1), (7, 0), (6, 7), (5, 7), (4, 7),
                 (3, 7), (2, 7), (1, 7), (0, 7)]
        self.assertEqual(r1moves, r1out)
        self.assertEqual(r2moves, r2out)


if __name__ == '__main__':
    unittest.main()
