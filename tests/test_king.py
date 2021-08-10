import unittest
from source import King, Board


class TestKing(unittest.TestCase):
    def setUp(self):
        self.king = King("white", (3, 4))
        self.board = Board()
        self.board.add(self.king)

    def test_get_possible_moves(self):
        # All moves possible
        kmoves = self.king.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)])
        # When the piece is on one corner
        self.board.move(self.king, (0, 0))
        kmoves = self.king.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(0, 1), (1, 0), (1, 1)])
        self.board.move(self.king, (3, 4))
        # Capture
        king2 = King("black", (2, 3))
        self.board.add(king2)
        kmoves = self.king.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)])
        self.board.remove(king2)
        # Ally piece blocking the way
        king3 = King("white", (2, 4))
        self.board.add(king3)
        kmoves = self.king.get_possible_moves(self.board)
        self.assertEqual(kmoves, [(2, 3), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)])


if __name__ == '__main__':
    unittest.main()
