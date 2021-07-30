import unittest
from source import Pawn


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn1 = Pawn("white", (1, 7))
        self.pawn2 = Pawn("black",  (1, 0))

    def test_get_possible_moves(self):
        # When all moves are possible
        p1moves = self.pawn1.get_possible_moves()
        p2moves = self.pawn2.get_possible_moves()
        self.assertEqual(p1moves, [(2, 6), (0, 6), (1, 6), (1, 5)])
        self.assertEqual(p2moves, [(2, 1), (0, 1), (1, 1), (1, 2)])
        # When no move is possible
        self.pawn1.move_to((0,  0))
        self.pawn2.move_to((7, 7))
        p1moves = self.pawn1.get_possible_moves()
        p2moves = self.pawn2.get_possible_moves()
        self.assertEqual(p1moves, [])
        self.assertEqual(p2moves, [])
        # When the piece was already moved
        self.pawn1.move_to((1, 7))
        self.pawn2.move_to((1, 0))
        self.pawn1.moved = True
        self.pawn2.moved = True
        p1moves = self.pawn1.get_possible_moves()
        p2moves = self.pawn2.get_possible_moves()
        self.assertEqual(p1moves, [(2, 6), (0, 6), (1, 6)])
        self.assertEqual(p2moves, [(2, 1), (0, 1), (1, 1)])


if __name__ == '__main__':
    unittest.main()
