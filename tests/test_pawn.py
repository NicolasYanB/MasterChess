import unittest
from source import Pawn, Board


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn = Pawn("white", (1, 7))
        self.board = Board()
        self.board.add(self.pawn)

    def test_get_possible_moves(self):
        # All moves available
        self.board.add(Pawn("black", (0, 6)))
        self.board.add(Pawn("black", (2, 6)))
        self.assertEqual(self.pawn.get_possible_moves(self.board), [(1, 6), (1, 5), (2, 6), (0, 6)])
        self.board.remove(0, 6)
        self.board.remove(2, 6)
        # Pieces blocking all possible moves
        self.board.add(Pawn("white", (0, 6)))
        self.board.add(Pawn("white", (2, 6)))
        self.board.add(Pawn("black", (1, 6)))
        self.assertEqual(self.pawn.get_possible_moves(self.board), [])
        self.board.remove(0, 6)
        self.board.remove(2, 6)
        self.board.remove(1, 6)
        # Pawn on the opposite corner
        self.board.move(self.pawn, (0, 0))
        self.assertEqual(self.pawn.get_possible_moves(self.board), [])
        # Pawn after first move
        self.board.move(self.pawn, (4, 4))
        self.assertEqual(self.pawn.get_possible_moves(self.board), [(4, 3)])


if __name__ == '__main__':
    unittest.main()
