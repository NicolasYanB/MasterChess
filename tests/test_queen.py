import unittest
from source import Queen, Board


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.queen = Queen("white", (3, 4))
        self.board = Board()
        self.board.add(self.queen)

    def test_get_possible_moves(self):
        # All moves available
        qmoves = self.queen.get_possible_moves(self.board)
        qout = [(3, 3), (3, 2), (3, 1), (3, 0), (4, 3), (5, 2), (6, 1), (7, 0), (4, 4), (5, 4),
                (6, 4), (7, 4), (4, 5), (5, 6), (6, 7), (3, 5), (3, 6), (3, 7), (2, 5), (1, 6),
                (0, 7), (2, 4), (1, 4), (0, 4), (2, 3), (1, 2), (0, 1)]
        self.assertEqual(qmoves, qout)
        # When this piece is on a corner
        self.board.move(self.queen, (0, 0))
        qmoves = self.queen.get_possible_moves(self.board)
        qout = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (1, 1), (2, 2), (3, 3),
                (4, 4), (5, 5), (6, 6), (7, 7), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                (0, 7)]
        self.assertEqual(qmoves, qout)
        self.board.move(self.queen, (3, 4))
        # Capture
        queen2 = Queen("black", (3, 3))
        self.board.add(queen2)
        qmoves = self.queen.get_possible_moves(self.board)
        qout = [(3, 3), (4, 3), (5, 2), (6, 1), (7, 0), (4, 4), (5, 4),
                (6, 4), (7, 4), (4, 5), (5, 6), (6, 7), (3, 5), (3, 6), (3, 7), (2, 5), (1, 6),
                (0, 7), (2, 4), (1, 4), (0, 4), (2, 3), (1, 2), (0, 1)]
        self.assertEqual(qmoves, qout)
        self.board.remove(queen2)
        # Ally piece blocking the way
        queen3 = Queen("white", (5, 2))
        self.board.add(queen3)
        qmoves = self.queen.get_possible_moves(self.board)
        qout = [(3, 3), (3, 2), (3, 1), (3, 0), (4, 3), (4, 4), (5, 4),
                (6, 4), (7, 4), (4, 5), (5, 6), (6, 7), (3, 5), (3, 6), (3, 7), (2, 5), (1, 6),
                (0, 7), (2, 4), (1, 4), (0, 4), (2, 3), (1, 2), (0, 1)]
        self.assertEqual(qmoves, qout)


if __name__ == '__main__':
    unittest.main()
