import unittest
from source import King


class TestKing(unittest.TestCase):
    def setUp(self):
        self.king1 = King("white", (3, 4))
        self.king2 = King("black", (4, 3))

    def test_get_possible_moves(self):
        # All moves possible
        k1moves = self.king1.get_possible_moves()
        k2moves = self.king2.get_possible_moves()
        self.assertEqual(k1moves, [(2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)])
        self.assertEqual(k2moves, [(3, 2), (3, 3), (3, 4), (4, 2), (4, 4), (5, 2), (5, 3), (5, 4)])
        # When the piece is on one corner
        self.king1.move_to((0, 0))
        self.king2.move_to((7, 7))
        k1moves = self.king1.get_possible_moves()
        k2moves = self.king2.get_possible_moves()
        self.assertEqual(k1moves, [(0, 1), (1, 0), (1, 1)])
        self.assertEqual(k2moves, [(6, 6), (6, 7), (7, 6)])


if __name__ == '__main__':
    unittest.main()
