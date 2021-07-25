import unittest
from source import Piece


class TestPiece(unittest.TestCase):
    def setUp(self):
        self.piece1 = Piece("pawn", "white", (0, 0))
        self.piece2 = Piece("knight", "black", (1, 0))

    def test_is_possible(self):
        print("test_is_possible")
        self.assertTrue(self.piece1._is_possible((2, 0)))
        for x in (8, 0, -1):
            for y in (8, 0, -1):
                self.assertFalse(self.piece1._is_possible((x, y)))
        self.assertTrue(self.piece2._is_possible((3, 0)))
        for x in (8, 0, -1):
            for y in (8, 0, -1):
                self.assertFalse(self.piece2._is_possible((x, y))) if x != y and x != 0 else 0
        self.assertFalse(self.piece2._is_possible((1, 0)))


if __name__ == '__main__':
    unittest.main()
