import unittest
from source import Bishop


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.bishop1 = Bishop("white", (3, 4))
        self.bishop2 = Bishop("black", (4, 4))

    def test_get_possible_moves(self):
        # All moves available
        b1moves = self.bishop1.get_possible_moves()
        b2moves = self.bishop2.get_possible_moves()
        b1out = [(2, 3), (1, 2), (0, 1), (4, 3), (5, 2), (6, 1), (7, 0), (4, 5), (5, 6), (6, 7),
                 (2, 5), (1, 6), (0, 7)]
        b2out = [(3, 3), (2, 2), (1, 1), (0, 0), (5, 3), (6, 2), (7, 1), (5, 5), (6, 6), (7, 7),
                 (3, 5), (2, 6), (1, 7)]
        self.assertEqual(b1moves, b1out)
        self.assertEqual(b2moves, b2out)
        # Moves when the piece is on a corner
        self.bishop1.move_to((0, 0))
        self.bishop2.move_to((7, 0))
        b1moves = self.bishop1.get_possible_moves()
        b2moves = self.bishop2.get_possible_moves()
        b1out = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        b2out = [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)]
        self.assertEqual(b1moves, b1out)
        self.assertEqual(b2moves, b2out)


if __name__ == '__main__':
    unittest.main()
