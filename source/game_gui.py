import tkinter as tk
from source import Game, InvalidMoveException


class GameGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width, self.height = 712, 712
        self.squares = []
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()
        self.game = Game()
        self.game.load_board()
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
                coords = x0, y0, x1, y1
                square = self.canvas.create_rectangle(coords, fill=colors[color], tags="square")
                color = abs(color - 1)
                self.squares.append(square)
            colors.reverse()
        self.canvas.tag_bind("square", "<Button-1>", self.square_event)

    def draw_pieces(self):
        self.images = []
        pieces = self.game.board.get_all_pieces()
        for piece in pieces:
            column, line = piece.position
            margin = 2  # Value to make the piece fits perfectly inside the square
            x, y = column * self.square_size + margin, line * self.square_size + margin
            image = tk.PhotoImage(file=piece.image)
            self.canvas.create_image(x, y, image=image, anchor=tk.NW, tags="piece")
            self.images.append(image)
        self.canvas.tag_bind("piece", "<Button-1>", self.piece_event)

    def square_event(self, event):
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        square_coords = square_x, square_y, square_x + self.square_size, square_y + self.square_size
        enclosed_objects = self.canvas.find_enclosed(*square_coords)
        for obj in enclosed_objects:
            if "move" in self.canvas.gettags(obj):
                self.move_event(event)
                break
        self.unselect()

    def piece_event(self, event):
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = int(square_x/self.square_size), int(square_y/self.square_size)
        clicked_piece = self.game.board.get(column, line)
        if clicked_piece.color != self.game.turn:
            if self.game.selected_piece is not None:
                self.move_event(event)
            return
        self.unselect()
        self.game.select_piece(column, line)
        self.highlight_piece(square_x, square_y)

    def move_event(self, event):
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = int(square_x/self.square_size), int(square_y/self.square_size)
        move = column, line
        try:
            self.game.move_selected_piece(move)
        except InvalidMoveException:
            self.unselect()
            return
        self.unselect()
        self.canvas.delete("piece")
        self.draw_pieces()
        king_in_check = self.game.get_king_in_check()
        self.highlight_king_in_check(king_in_check)

    def find_square(self, x, y):
        for square in self.squares:
            x0, y0, x1, y1 = self.canvas.coords(square)
            if x0 <= x <= x1 and y0 <= y <= y1:
                return x0, y0

    def highlight_piece(self, x, y):
        border = 3  # Value to make the border fits inside the square
        x0, y0 = x + border, y + border
        x1, y1 = x + self.square_size - border, y + self.square_size - border
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#f5cb5c", tags="selected", width=5)
        self.highlight_valid_moves()

    def highlight_valid_moves(self):
        valid_moves = self.game.get_selected_piece_moves()
        for move in valid_moves:
            column, line = move
            x, y = column * self.square_size, line * self.square_size
            x0, y0, x1, y1 = x, y, x + self.square_size, y + self.square_size
            if not self.game.board.is_empty(column, line):
                border = 3
                x0, y0 = x0 + border, y0 + border
                x1, y1 = x1 - border, y1 - border
                coords = x0, y0, x1, y1
                self.canvas.create_rectangle(coords, outline="#fca311", tags="move", width=5)
                continue
            margin = 28  # margin between the square and the circle
            x0, y0, x1, y1 = x0 + margin, y0 + margin, x1 - margin, y1 - margin
            self.canvas.create_oval(x0, y0, x1, y1, fill="#f5cb5c", outline="#f5cb5c", tags="move")
        self.canvas.tag_bind("move", "<Button-1>", self.move_event)

    def highlight_king_in_check(self, king):
        if king == 0:
            self.canvas.delete("check")
            return
        column, line = king.position
        x, y = column * self.square_size, line * self.square_size
        border = 3
        x0, y0 = x + border, y + border
        x1, y1 = x + self.square_size - border, y + self.square_size - border
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="check", width=5)

    def unselect(self):
        self.game.unselect()
        self.canvas.delete("selected")
        self.canvas.delete("move")


if __name__ == '__main__':
    root = tk.Tk()
    game_gui = GameGui(root)
    game_gui.mainloop()
