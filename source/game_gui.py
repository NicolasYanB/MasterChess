import tkinter as tk
from source import Game, InvalidMoveException
from source import Queen, Rook, Bishop, Knight
from datetime import datetime
import os


class GameGui(tk.Frame):
    def __init__(self, master, saved_game=None):
        super().__init__(master)
        self.width = self.height = 712
        self.squares = []
        self.stop_game = False
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.game = Game()
        if saved_game is None:
            self.game.load_new_game_board()
        else:
            self.game.load_saved_game_board(saved_game)
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
        if self.stop_game:
            return
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        square_coords = square_x, square_y, square_x + self.square_size, square_y + self.square_size
        enclosed_objects = self.canvas.find_enclosed(*square_coords)
        for obj in enclosed_objects:
            if "move" in self.canvas.gettags(obj):
                self.move_event(event)
                break
        else:
            self.unselect()

    def piece_event(self, event):
        if self.stop_game:
            return
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
        if self.stop_game:
            return
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = int(square_x/self.square_size), int(square_y/self.square_size)
        move = column, line
        try:
            self.game.move_selected_piece(move)
        except InvalidMoveException:
            self.unselect()
            return
        moved_piece = self.game.selected_piece
        self.unselect()
        self.canvas.delete("piece")
        self.draw_pieces()
        self.canvas.delete("check")
        if self.was_promoted(moved_piece):
            promotion_window = PromotionWindow(self, moved_piece)
            promotion_window.mainloop()
        else:
            self.finish_move()

    def finish_move(self):
        game_status = self.game.post_movement_actions()
        king_in_check = self.game.get_king_in_check()
        self.highlight_king_in_check(king_in_check)
        if game_status != 0:
            self.end_game(game_status)

    def end_game(self, game_status):
        self.stop_game = True
        end_game_window = 0
        if game_status == 1:
            winner = "white" if self.game.turn == "black" else "white"
            end_game_window = CheckmateWindow(self, winner)
        else:
            end_game_window = DrawWindow(self, game_status)
        end_game_window.mainloop()

    def was_promoted(self, piece):
        if piece.type == "pawn":
            line = piece.position[1]
            if line == 0 or line == 7:
                return True
        return False

    def promote(self, promoted_piece, new_piece):
        self.game.promote(promoted_piece, new_piece)
        self.canvas.delete("piece")
        self.draw_pieces()
        self.finish_move()

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

    def on_closing(self):
        children = self.master.winfo_children()
        if len(children) > 1:
            child = children[1]
            if child._w == ".!promotionwindow":
                return
            self.master.destroy()
            return
        save_game_dialog = SaveGameWindow(self)
        save_game_dialog.mainloop()


class PromotionWindow(tk.Toplevel):
    def __init__(self, master, pawn):
        self.width = self.height = 178
        super().__init__(width=self.width, height=self.height)
        self.master = master
        self.master.stop_game = True
        self.square_side = self.width//2
        self.color = pawn.color
        self.pawn = pawn
        self.title("Promotion")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.set_components()

    def on_closing(self):
        pass

    def set_components(self):
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        light_square = "#eeeed2"
        dark_square = "#769656"
        colors = [light_square, dark_square]
        color = 0
        for y in range(2):
            for x in range(2):
                x1, y1 = self.square_side * x, self.square_side * y
                x2, y2 = x1 + self.square_side, y1 + self.square_side
                coords = x1, y1, x2, y2
                self.canvas.create_rectangle(coords, fill=colors[color], tags="square")
                color = abs(color - 1)
            colors.reverse()

    def draw_pieces(self):
        self.pieces = []
        queen_image = f"images/pieces/{self.color}/queen.png"
        rook_image = f"images/pieces/{self.color}/rook.png"
        bishop_image = f"images/pieces/{self.color}/bishop.png"
        knight_image = f"images/pieces/{self.color}/knight.png"
        images = {"queen": queen_image, "rook": rook_image,
                  "bishop": bishop_image, "knight": knight_image}
        margin = 2
        c = 0
        for y in range(2):
            for x in range(2):
                x0, y0 = self.square_side * x + margin, self.square_side * y + margin
                piece = list(images.keys())[c]
                image = tk.PhotoImage(file=images[piece])
                self.pieces.append(image)
                self.canvas.create_image(x0, y0, image=image, anchor=tk.NW, tags=f"piece {piece}")
                c += 1
        self.canvas.tag_bind("piece", "<Button-1>", self.click_event)

    def click_event(self, event):
        pieces = ["queen", "rook", "bishop", "knight"]
        clicked_object = event.widget.find_withtag("current")
        tags = self.canvas.gettags(clicked_object)
        for piece in pieces:
            if piece in tags:
                self.promote_to(piece)

    def promote_to(self, type):
        pieces = {"queen": Queen, "rook": Rook,
                  "bishop": Bishop, "knight": Knight}
        promoted_piece = pieces[type](self.color, self.pawn.position)
        self.master.promote(self.pawn, promoted_piece)
        self.master.stop_game = False
        self.destroy()


class EndGameWindow(tk.Toplevel):
    def __init__(self, master, width=300, height=100):
        super().__init__(width=width, height=height)
        self.master = master
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_all)

    def set_buttons(self, x):
        new_game_btn = tk.Button(self, text="New Game", command=self.start_new_game)
        main_menu_btn = tk.Button(self, text="Main Menu", command=self.return_to_main_menu)
        close_btn = tk.Button(self, text="Exit", command=self.close_all)
        delta = 110
        new_game_btn.place(x=x, y=50)
        main_menu_btn.place(x=x+delta, y=50)
        close_btn.place(x=x+delta*2, y=50)

    def start_new_game(self):
        self.master.master.destroy()
        new_root = tk.Tk()
        new_game_gui = GameGui(new_root)
        new_game_gui.mainloop()

    def return_to_main_menu(self):
        from source import MainMenu
        self.master.master.destroy()
        new_root = tk.Tk()
        main_menu = MainMenu(new_root)
        main_menu.mainloop()

    def close_all(self):
        self.master.master.destroy()


class CheckmateWindow(EndGameWindow):
    def __init__(self, master, winner):
        super().__init__(master)
        self.winner = winner
        self.title("Checkmate")
        self.set_components()

    def set_components(self):
        self.set_label()
        self.set_buttons(10)

    def set_label(self):
        text = f"{self.winner} wins"
        label = tk.Label(self, text=text, font="sans-serif 15 bold")
        label.place(x=90, y=10)


class DrawWindow(EndGameWindow):
    def __init__(self, master, end_game):
        super().__init__(master, width=350)
        self.end_game = end_game
        self.title("Draw")
        self.set_components()

    def set_components(self):
        self.set_label()
        self.set_buttons(40)

    def set_label(self):
        draw_type = ''
        x = 0
        if self.end_game == 2:
            draw_type = "stalemate"
            x = 65
        if self.end_game == 3:
            draw_type = "threefold repetition"
            x = 10
        if self.end_game == 4:
            draw_type = "fifty move rule"
            x = 40
        if self.end_game == 5:
            draw_type = "insufficient material"
            x = 10
        text = f"Draw by {draw_type}"
        label = tk.Label(self, text=text, font="sans-serif 15 bold")
        label.place(x=x, y=10)


class SaveGameWindow(tk.Toplevel):
    def __init__(self, master):
        width = 300
        height = 160
        super().__init__(width=width, height=height)
        master.stop_game = True
        self.title("Save Game")
        self.resizable(False, False)
        self.master = master
        self.set_components()
        self.bind("<Return>", lambda event: self.yes_btn_event())
        self.bind("<Escape>", lambda event: self.destroy())

    def set_components(self):
        save_game_lbl = tk.Label(self, text="Save the Game?", font="sans-serif 13 bold")
        save_game_lbl.place(x=75, y=20)
        self.set_entry()
        self.set_buttons()

    def set_entry(self):
        default_filename = datetime.now().strftime(r"%Y-%m-%d %H:%M")
        self.game_file_entry = tk.Entry(self, width=34)
        self.game_file_entry.insert(0, default_filename)
        self.game_file_entry.place(x=10, y=55)

    def set_buttons(self):
        yes_btn = tk.Button(self, text="YES", command=self.yes_btn_event)
        no_btn = tk.Button(self, text="NO", command=self.no_btn_event)
        cancel_btn = tk.Button(self, text="Cancel", command=self.destroy)
        yes_btn.place(x=40, y=100)
        no_btn.place(x=110, y=100)
        cancel_btn.place(x=180, y=100)

    def yes_btn_event(self):
        game_state = self.master.game.get_game_data()
        filename = self.game_file_entry.get()
        home = os.path.expanduser('~')
        path = f"{home}/.MasterChess/{filename}"
        with open(path, 'w') as game_file:
            game_file.write(game_state)
        self.master.master.destroy()

    def no_btn_event(self):
        self.master.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    game_gui = GameGui(root)
    game_gui.mainloop()
