import unittest
from source import Pawn, Knight, Rook, Bishop, Queen, King, Board


class TestBoard(unittest.TestCase):
    def test_add(self):
        print("test_add")
        board = Board()
        white_pawn = Pawn("white", (0, 0))
        black_pawn = Pawn("black", (0, 0))
        board.add(white_pawn)
        self.assertRaises(IndexError, board.add, black_pawn)

    def test_get(self):
        print("test_get")
        board = Board()
        white_knight = Knight("black", (1, 0))
        black_knight = Knight("white", (2, 0))
        board.add(white_knight)
        board.add(black_knight)
        self.assertEqual(board.get(1, 0), white_knight)
        self.assertEqual(board.get(2, 0), black_knight)

    def test_is_empty(self):
        print("test_is_empty")
        board = Board()
        white_rook = Rook("white", (3, 0))
        board.add(white_rook)
        self.assertFalse(board.is_empty(3, 0))
        self.assertTrue(board.is_empty(0, 0))

    def test_get_all_of(self):
        print("test_get_all_of")
        board = Board()
        wpawn = Pawn("white", (0, 0))
        bpawn = Pawn("black", (1, 0))
        wknight = Knight("white", (2, 0))
        bknight = Knight("black", (3, 0))
        wrook = Rook("white", (4, 0))
        brook = Rook("black", (5, 0))
        wbishop = Bishop("white", (6, 0))
        bbishop = Bishop("black", (7, 0))
        wqueen = Queen("white", (0, 1))
        bqueen = Queen("black", (1, 1))
        wking = King("white", (2, 1))
        bking = King("black", (3, 1))
        pieces = [wpawn, bpawn, wknight, bknight, wrook, brook, wbishop, bbishop, wqueen,
                  bqueen, wking, bking]
        for piece in pieces:
            board.add(piece)
        self.assertEqual(board.get_all_of("white"), [wpawn, wknight, wrook, wbishop, wqueen,
                                                     wking])
        self.assertEqual(board.get_all_of("black"), [bpawn, bknight, brook, bbishop, bqueen,
                                                     bking])

    def test_get_all(self):
        print("test_get_all")
        board = Board()
        wpawn0 = Pawn("white", (0, 0))
        wpawn1 = Pawn("white", (1, 0))
        bpawn0 = Pawn("black", (2, 0))
        bpawn1 = Pawn("black", (3, 0))
        pieces = [wpawn0, wpawn1, bpawn0, bpawn1]
        for piece in pieces:
            board.add(piece)
        self.assertEqual(board.get_all("pawn", "white"), [wpawn0, wpawn1])
        self.assertEqual(board.get_all("pawn", "black"), [bpawn0, bpawn1])
        self.assertEqual(board.get_all("pawn"), [wpawn0, wpawn1, bpawn0, bpawn1])

    def test_remove(self):
        board = Board()
        wpawn = Pawn("white", (0, 0))
        board.add(wpawn)
        board.remove(0, 0)
        board.add(wpawn)
        board.remove(wpawn)
        self.assertEqual(board.get_all("pawn"), [])
        self.assertRaises(IndexError, board.remove, 1, 1)
        self.assertRaises(ValueError, board.remove, wpawn)

    def test_move(self):
        board = Board()
        wpawn = Pawn("white", (0, 0))
        board.add(wpawn)
        board.move(wpawn, (1, 0))
        self.assertEqual(wpawn.position, (1, 0))


if __name__ == '__main__':
    unittest.main()
