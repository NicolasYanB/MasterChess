import unittest
from source import Queen


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.queen1 = Queen("white", (3, 4))
        self.queen2 = Queen("black", (4, 4))

    def test_get_possible_moves(self):
        # All moves available
        q1moves = self.queen1.get_possible_moves()
        q2moves = self.queen2.get_possible_moves()
        q1out = [(3, 3), (3, 2), (3, 1), (3, 0), (4, 3), (5, 2), (6, 1), (7, 0), (4, 4), (5, 4),
                 (6, 4), (7, 4), (4, 5), (5, 6), (6, 7), (3, 5), (3, 6), (3, 7), (2, 5), (1, 6),
                 (0, 7), (2, 4), (1, 4), (0, 4), (2, 3), (1, 2), (0, 1)]
        q2out = [(4, 3), (4, 2), (4, 1), (4, 0), (5, 3), (6, 2), (7, 1), (5, 4), (6, 4), (7, 4),
                 (5, 5), (6, 6), (7, 7), (4, 5), (4, 6), (4, 7), (3, 5), (2, 6), (1, 7), (3, 4),
                 (2, 4), (1, 4), (0, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
        self.assertEqual(q1moves, q1out)
        self.assertEqual(q2moves, q2out)
        # When this piece is on a corner
        self.queen1.move_to((0, 0))
        self.queen2.move_to((7, 7))
        q1moves = self.queen1.get_possible_moves()
        q2moves = self.queen2.get_possible_moves()
        q1out = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 1), (2, 2), (3, 3),
                 (4, 4), (5, 5), (6, 6), (7, 7), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                 (0, 7)]
        q2out = [(7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (7, 0), (6, 7), (5, 7), (4, 7),
                 (3, 7), (2, 7), (1, 7), (0, 7), (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1),
                 (0, 0)]
        self.assertEqual(q1moves, q1out)
        self.assertEqual(q2moves,  q2out)


if __name__ == '__main__':
    unittest.main()
