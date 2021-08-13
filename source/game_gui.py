import tkinter as tk
from source import Game


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
        pieces = [piece for piece in self.game.board]
        for piece in pieces:
            column, line = piece.position
            x, y = column * self.square_size, line * self.square_size
            image = tk.PhotoImage(file=piece.image)
            self.canvas.create_image(x, y, image=image, anchor=tk.NW)
            self.images.append(image)


if __name__ == '__main__':
    root = tk.Tk()
    game_gui = GameGui(root)
    game_gui.mainloop()
