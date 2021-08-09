import unittest
from source import Rook, Board


class TestRook(unittest.TestCase):
    def setUp(self):
        self.rook = Rook("white", (3, 4))
        self.board = Board()
        self.board.add(self.rook)

    def test_get_possible_moves(self):
        # All moves available
        rmoves = self.rook.get_possible_moves(self.board)
        rout = [(3, 3), (3, 2), (3, 1), (3, 0), (3, 5), (3, 6), (3, 7), (2, 4), (1, 4), (0, 4),
                (4, 4), (5, 4), (6, 4), (7, 4)]
        self.assertEqual(rmoves, rout)
        # Piece on a corner
        self.board.move(self.rook, (0, 0))
        rmoves = self.rook.get_possible_moves(self.board)
        rout = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0),
                (4, 0), (5, 0), (6, 0), (7, 0)]
        self.assertEqual(rmoves, rout)
        self.board.move(self.rook, (3, 4))
        # Capture
        rook2 = Rook("black", (3, 2))
        self.board.add(rook2)
        rmoves = self.rook.get_possible_moves(self.board)
        rout = [(3, 3), (3, 2), (3, 5), (3, 6), (3, 7), (2, 4), (1, 4), (0, 4),
                (4, 4), (5, 4), (6, 4), (7, 4)]
        self.assertEqual(rmoves, rout)
        self.board.remove(rook2)
        # Ally piece blocking the way
        rook3 = Rook("white", (4, 4))
        self.board.add(rook3)
        rmoves = self.rook.get_possible_moves(self.board)
        rout = [(3, 3), (3, 2), (3, 1), (3, 0), (3, 5), (3, 6), (3, 7), (2, 4), (1, 4), (0, 4)]
        self.assertEqual(rmoves, rout)


if __name__ == '__main__':
    unittest.main()
