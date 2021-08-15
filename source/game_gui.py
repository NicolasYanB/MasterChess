import tkinter as tk
from source import Game, TurnError


class GameGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width, self.height = 712, 712
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()
        self.game = Game()
        self.draw_board()
        self.draw_pieces()
        self.master = master

    def draw_board(self):
        self.square_size = self.width//8
        light_square = "#eeeed2"
        dark_square = "#769656"
        colors = [light_square, dark_square]
        color = 0
        for y in range(0, self.height, self.square_size):
            for x in range(0, self.width, self.square_size):
                x0, y0, x1, y1 = x, y, x + self.square_size, y + self.square_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[color])
                color = abs(color - 1)
            colors.reverse()

    def draw_pieces(self):
        self.game.load_board()
        self.images = []
        pieces = self.game.board.get_all_pieces()
        for piece in pieces:
            column, line = piece.position
            x, y = column * self.square_size, line * self.square_size
            image = tk.PhotoImage(file=piece.image)
            self.canvas.create_image(x, y, image=image, anchor=tk.NW, tags="piece")
            self.images.append(image)
        self.canvas.tag_bind("piece", "<Button-1>", self.piece_event)

    def piece_event(self, event):
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = square_x//self.square_size, square_y//self.square_size
        # --- Temporary code ---
        try:
            self.game.select_piece(column, line)
        except TurnError:
            self.game.unselect() if self.game.selected_piece is not None else 0
            return
        # Test
        piece = self.game.selected_piece
        print(piece.type, piece.color, piece.position)

    def find_square(self, x, y):
        for posy in range(0, self.height, self.square_size):
            for posx in range(0, self.width, self.square_size):
                x0, y0, x1, y1 = posx, posy, posx + self.square_size, posy + self.square_size
                if x0 < x < x1 and y0 < y < y1:
                    return x0, y0


if __name__ == '__main__':
    root = tk.Tk()
    game_gui = GameGui(root)
    game_gui.mainloop()
