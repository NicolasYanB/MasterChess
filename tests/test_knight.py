import unittest
from source import Knight, Board


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight1 = Knight("white", (3, 4))
        self.board = Board()
        self.board.add(self.knight1)

    def test_get_possible_moves(self):
        # When all moves are possible
        k1moves = self.knight1.get_possible_moves(self.board)
        self.assertEqual(k1moves, [(2, 2), (4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])
        # When knight is on the corner
        self.board.move(self.knight1, (0, 0))
        k1moves = self.knight1.get_possible_moves(self.board)
        self.assertEqual(k1moves, [(1, 2), (2, 1)])
        # Capture
        self.board.move(self.knight1, (3, 4))
        bknight = Knight("black", (2, 2))
        self.board.add(bknight)
        k1moves = self.knight1.get_possible_moves(self.board)
        self.assertEqual(k1moves, [(2, 2), (4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])
        self.board.remove(bknight)
        # Ally piece blocking the way
        wknight = Knight("white", (2, 2))
        self.board.add(wknight)
        k1moves = self.knight1.get_possible_moves(self.board)
        self.assertEqual(k1moves, [(4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])


if __name__ == '__main__':
    unittest.main()
