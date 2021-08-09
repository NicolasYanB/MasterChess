import unittest
from source import Knight, Board


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight = Knight("white", (3, 4))
        self.board = Board()
        self.board.add(self.knight)

    def test_get_possible_moves(self):
        # When all moves are possible
        kmoves = self.knight.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(2, 2), (4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])
        # When knight is on the corner
        self.board.move(self.knight, (0, 0))
        kmoves = self.knight.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(1, 2), (2, 1)])
        # Capture
        self.board.move(self.knight, (3, 4))
        bknight = Knight("black", (2, 2))
        self.board.add(bknight)
        kmoves = self.knight.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(2, 2), (4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])
        self.board.remove(bknight)
        # Ally piece blocking the way
        wknight = Knight("white", (2, 2))
        self.board.add(wknight)
        kmoves = self.knight.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(4, 2), (2, 6), (4, 6), (1, 3), (1, 5), (5, 3), (5, 5)])


if __name__ == '__main__':
    unittest.main()
