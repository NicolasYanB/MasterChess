import unittest
from source import Knight


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight1 = Knight("white", (3, 4))
        self.knight2 = Knight("black", (4, 3))

    def test_get_possible_moves(self):
        # When all moves are possible
        k1moves = self.knight1.get_possible_moves()
        k2moves = self.knight2.get_possible_moves()
        self.assertEqual(k1moves, [(2, 2), (4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])
        self.assertEqual(k2moves, [(3, 1), (5, 1), (3, 5), (5, 5), (2, 2), (2, 4), (6, 2), (6, 4)])
        # When knight is on the corner
        self.knight1.move_to((0, 0))
        self.knight2.move_to((7, 7))
        k1moves = self.knight1.get_possible_moves()
        k2moves = self.knight2.get_possible_moves()
        self.assertEqual(k1moves, [(1, 2), (2, 1)])
        self.assertEqual(k2moves, [(6, 5), (5, 6)])


if __name__ == '__main__':
    unittest.main()
