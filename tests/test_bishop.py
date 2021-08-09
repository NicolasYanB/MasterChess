import unittest
from source import Bishop, Board


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.bishop = Bishop("white", (3, 4))
        self.board = Board()
        self.board.add(self.bishop)

    def test_get_possible_moves(self):
        # All moves available
        bmoves = self.bishop.get_possible_moves(self.board)
        bout = [(2, 3), (1, 2), (0, 1), (4, 3), (5, 2), (6, 1), (7, 0), (4, 5), (5, 6), (6, 7),
                (2, 5), (1, 6), (0, 7)]
        self.assertEqual(bmoves, bout)
        # Moves when the piece is on a corner
        self.board.move(self.bishop, (0, 0))
        bmoves = self.bishop.get_possible_moves(self.board)
        bout = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        self.assertEqual(bmoves, bout)
        self.board.move(self.bishop, (3, 4))
        # Capture
        bishop2 = Bishop("black", (2, 3))
        self.board.add(bishop2)
        bmoves = self.bishop.get_possible_moves(self.board)
        bout = [(2, 3), (4, 3), (5, 2), (6, 1), (7, 0), (4, 5), (5, 6), (6, 7),
                (2, 5), (1, 6), (0, 7)]
        self.assertEqual(bmoves, bout)
        self.board.remove(bishop2)
        # Ally piece blocking the way
        bishop2 = Bishop("white", (5, 2))
        self.board.add(bishop2)
        bmoves = self.bishop.get_possible_moves(self.board)
        bout = [(2, 3), (1, 2), (0, 1), (4, 3), (4, 5), (5, 6), (6, 7),
                (2, 5), (1, 6), (0, 7)]
        self.assertEqual(bmoves, bout)


if __name__ == '__main__':
    unittest.main()
