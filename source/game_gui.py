from datetime import datetime
import tkinter as tk
import os

from source import Queen, Rook, Bishop, Knight
from source import Game, InvalidMoveException
from source import realpath


class GameGui(tk.Frame):
    """
    Game graphical interface

    Reads the user input and display the changes on the game

    Args:
        master (tkinter.Tk): parent widget
        loaded_game (List[object]): list of pieces of information about the game

    Attributes:
        width (int): width of the window
        height (int): height of the window
        square_side (int): size of the side of the square
        squares (List[int]): IDs of all squares of the board
        images (List[tkinter.PhotoImage]): list to keep a reference to all the images used
            so the garbage collector don't erase them.
        paused (bool): true if the game was suspended
        canvas (tkinter.Canvas): widget that draws the board and the pieces
        game (game.Game): object responsible for validating and executing player actions
        master (tkinter.Tk): parent widget
    """

    def __init__(self, master, loaded_game=None):
        super().__init__(master)
        self.width = self.height = 712
        self.squares = []
        self.images = []
        self.paused = False
        self.square_side = self.width//8
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        icon = tk.PhotoImage(file=f"{realpath}/images/icon.png")
        master.iconphoto(False, icon)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pack(expand=True, fill=tk.BOTH)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.game = Game()
        if loaded_game:
            self.game.load_saved_game_board(loaded_game)
        else:
            self.game.init_new_game_board()
        self.draw_board()
        self.draw_pieces()
        self.master = master

    def draw_board(self):
        """Draws all the squares that compound the board"""
        light_square = "#eeeed2"
        dark_square = "#769656"
        colors = [light_square, dark_square]
        color = 0
        for y in range(0, self.height, self.square_side):
            for x in range(0, self.width, self.square_side):
                x0, y0, x1, y1 = x, y, x + self.square_side, y + self.square_side
                coords = x0, y0, x1, y1
                square = self.canvas.create_rectangle(coords, fill=colors[color], tags="square")
                color = abs(color - 1)  # Change the value from 0 to 1 and vice versa
                self.squares.append(square)
            colors.reverse()
        self.canvas.tag_bind("square", "<Button-1>", self.square_click_event)

    def draw_pieces(self):
        """Draw the pieces on their respective positions at self.game.board"""
        pieces = self.game.board.get_all_pieces()
        for piece in pieces:
            column, line = piece.position
            margin = 2  # Distance between the square border and the piece image border
            x, y = column * self.square_side + margin, line * self.square_side + margin
            image = tk.PhotoImage(file=realpath + '/' + piece.image)
            self.canvas.create_image(x, y, image=image, anchor=tk.NW, tags="piece")
            self.images.append(image)
        self.canvas.tag_bind("piece", "<Button-1>", self.piece_click_event)
        self.highlight_king_in_check()  # In a loaded game, check if the king is in check

    def square_click_event(self, event):
        """
        Method trigged when the user clicks on a square

        If there's a circle inside the square, move the selected piece to that square.
        If not, unselect the piece and erase all the moves highlights.

        Args:
            event (tkinter.Event): object that contains information about the event
        """
        if self.paused:
            return
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        square_coords = square_x, square_y, square_x + self.square_side, square_y + self.square_side
        enclosed_objects = self.canvas.find_enclosed(*square_coords)
        for obj in enclosed_objects:
            if "move" in self.canvas.gettags(obj):
                self.move_event(event)
                break
        else:
            self.unselect()

    def piece_click_event(self, event):
        """
        Method trigged when the user clicks on a piece

        Highlight the piece as well as all movements it can make

        If the piece clicked is an opponent piece, check if there's a piece selected,
        call move_event to try to capture that piece if there is.

        Args:
            event (tkinter.Event): object that contains information about the event
        """
        if self.paused:
            return
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = int(square_x/self.square_side), int(square_y/self.square_side)
        clicked_piece = self.game.board.get(column, line)
        if clicked_piece.color != self.game.turn:
            if self.game.selected_piece is not None:
                self.move_event(event)
            return
        self.unselect()
        self.game.select_piece(column, line)
        self.highlight_square(square_x, square_y)

    def move_event(self, event):
        """
        Moves the selected piece to the clicked square

        args:
            event (tkinter.Event): object that contains information about the event
        """
        if self.paused:
            return
        x, y = event.x, event.y
        square_x, square_y = self.find_square(x, y)
        column, line = int(square_x/self.square_side), int(square_y/self.square_side)
        move = column, line
        try:
            self.game.move_selected_piece(move)
        except InvalidMoveException:
            self.unselect()
            return
        moved_piece = self.game.selected_piece
        self.canvas.delete("piece")
        self.draw_pieces()
        self.canvas.delete("check")
        self.unselect()
        if self.was_promoted(moved_piece):
            promotion_window = PromotionWindow(self, moved_piece)
            promotion_window.mainloop()
        else:
            self.finish_move()

    def finish_move(self):
        """Highlight the king if it is in check and check if the game ended."""
        game_status = self.game.post_movement_actions()
        self.highlight_king_in_check()
        if game_status != 0:
            self.end_game(game_status)

    def end_game(self, game_status):
        """
        Finish the game and open a dialog displaying how the game ended

        args:
            game_status (int): The value represents how the game ended. 1 represents a checkmate,
                values up to 5 stand for a draw.
        """
        self.paused = True
        end_game_window = 0
        if game_status == 1:
            # The turn change before this method is called, so the winner is the opposite player
            winner = "white" if self.game.turn == "black" else "white"
            end_game_window = CheckmateWindow(self, winner)
        else:
            end_game_window = DrawWindow(self, game_status)
        end_game_window.mainloop()

    def was_promoted(self, piece):
        """
        Checks if the piece reached the promotion if it's a pawn

        args:
            piece (piece.Piece): piece that was or wasn't promoted

        returns:
            bool: True if the piece reached the promotion.
                False if wasn't promoted or wasn't a pawn
        """
        if piece.type == "pawn":
            line = piece.position[1]
            if line == 0 or line == 7:
                return True
        return False

    def promote(self, promoted_piece, new_piece):
        """
        Replaces the old piece for the new piece

        args:
            promoted_piece (piece.Piece): old piece that was promoted
            new_piece (piece.Piece): piece that will replace the old piece
        """
        self.game.promote(promoted_piece, new_piece)
        self.canvas.delete("piece")
        self.draw_pieces()
        self.finish_move()

    def find_square(self, x, y):
        """
        Finds on which square is the point (x, y)

        args:
            x (int): horizontal position of the point
            y (int): vertical position of the point

        returns:
            coordinate of the left top corner of the square as a tuple, for example: (0, 89)
        """
        for square in self.squares:
            x0, y0, x1, y1 = self.canvas.coords(square)
            if x0 <= x <= x1 and y0 <= y <= y1:
                return x0, y0

    def highlight_square(self, x, y):
        """
        Highlight a square in a given position

        Args:
            x (int): horizontal position of the square in pixels
            y (int): vertical position of the square in pixels
        """
        border = 3  # Value to make the sides fits inside the square
        x0, y0 = x + border, y + border
        x1, y1 = x + self.square_side - border, y + self.square_side - border
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#f5cb5c", tags="selected", width=5)
        self.highlight_valid_moves()

    def highlight_valid_moves(self):
        """
        Highlights every square to which the selected piece can move to

        Creates a circle if the square is empty and contours squares of capturable pieces.
        """
        valid_moves = self.game.get_selected_piece_moves()
        for move in valid_moves:
            column, line = move
            x, y = column * self.square_side, line * self.square_side
            x0, y0, x1, y1 = x, y, x + self.square_side, y + self.square_side
            if not self.game.board.is_empty(column, line):
                # Highlight a piece that can be captured
                border = 3
                x0, y0 = x0 + border, y0 + border
                x1, y1 = x1 - border, y1 - border
                coords = x0, y0, x1, y1
                self.canvas.create_rectangle(coords, outline="#fca311", tags="move", width=5)
                continue
            margin = 28  # margin to center the circle in the square
            x0, y0, x1, y1 = x0 + margin, y0 + margin, x1 - margin, y1 - margin
            self.canvas.create_oval(x0, y0, x1, y1, fill="#f5cb5c", outline="#f5cb5c", tags="move")
        self.canvas.tag_bind("move", "<Button-1>", self.move_event)

    def highlight_king_in_check(self):
        """Creates a red contour in the king square if it is in check"""
        king = self.game.get_king_in_check()
        if king == 0:
            return
        column, line = king.position
        x, y = column * self.square_side, line * self.square_side
        border = 3
        x0, y0 = x + border, y + border
        x1, y1 = x + self.square_side - border, y + self.square_side - border
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="check", width=5)

    def unselect(self):
        """
        Unselect the selected piece and remove all highlights on squares.
        """
        self.game.unselect()
        self.canvas.delete("selected")
        self.canvas.delete("move")

    def on_closing(self):
        """
        Handles the protocol of closing the window

        If the promotion window is open, the user can't close the game window.

        If there's any dialog box open, except by the promotion window, the windows can
        be closed normally.

        If no other dialog is open, the save game window opens to the user.
        """
        children = self.master.winfo_children()
        if len(children) > 1:
            child = children[1]
            if child._w == ".!promotionwindow":
                # Can't close the game if promotion window is open
                return
            self.master.destroy()
            return
        save_game_dialog = SaveGameWindow(self)
        save_game_dialog.mainloop()


class PromotionWindow(tk.Toplevel):
    """
    Dialog box that opens when a pawn is promoted.

    The user promote the pawn to one of the four options: rook, bishop, knight, and queen

    A 2x2 grid appears with a piece option on each square for the player to choose

    Args:
        master (tkinter.Frame): parent widget
        pawn (piece.Piece): promoted pawn

    Attributes:
        width (int): width of the window
        height (int): height of the window
        master (tkinter.Frame): parent widget
        square_side (int): side of the squares
        color (str): color of the promoted pawn
        pawn (piece.Pawn): promoted pawn
        canvas (tkinter.Canvas): the widget that draws the grid and the pieces
        pieces (List[tkinter.PhotoImage]): List to keep a reference to all the images used,
            so the garbage collector doesn't erase them.
    """
    def __init__(self, master, pawn):
        self.width = self.height = 178
        super().__init__(width=self.width, height=self.height)
        self.master = master
        self.master.paused = True
        self.square_side = self.width//2
        self.color = pawn.color
        self.pawn = pawn
        self.pieces = []
        icon = tk.PhotoImage(file="images/icon.png")
        self.iconphoto(False, icon)
        self.title("Promotion")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.set_components()

    def on_closing(self):
        # This window can't be closed
        pass

    def set_components(self):
        """Draws all the components on the window"""
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        """Draws the 2x2 grid that shows all the options to the player"""
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
        """Draws one piece in each square for the player to choose"""
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
        """
        Triggers when the player chooses the piece clicking on it

        Args:
            event (tkinter.Event): object that contains information about the event
        """
        pieces = ["queen", "rook", "bishop", "knight"]
        clicked_object = event.widget.find_withtag("current")
        tags = self.canvas.gettags(clicked_object)
        for piece in pieces:
            if piece in tags:
                self.promote_to(piece)

    def promote_to(self, piece_type):
        """
        Replace the old piece with the new piece, close the window, and the game proceeds

        Args:
            piece_type (str): type of the new piece
        """
        pieces = {"queen": Queen, "rook": Rook,
                  "bishop": Bishop, "knight": Knight}
        promoted_piece = pieces[piece_type](self.color, self.pawn.position)
        self.master.promote(self.pawn, promoted_piece)
        self.master.paused = False
        self.destroy()


class EndGameWindow(tk.Toplevel):
    """
    Parent class of all windows that pops up when the game ends

    Args:
        master (tkinter.Frame): parent widget
        width (int): width of the window. Defaults to 300
        height (int): height of the window. Defaults to 100
    """
    def __init__(self, master, width=300, height=100):
        super().__init__(width=width, height=height)
        self.master = master
        self.resizable(False, False)
        icon = tk.PhotoImage(file="images/icon.png")
        self.iconphoto(False, icon)
        self.protocol("WM_DELETE_WINDOW", self.close_all)

    def set_buttons(self, x):
        """
        Puts the buttons on the window

        Args:
            x (int): horizontal position of the first button in pixels
        """
        new_game_btn = tk.Button(self, text="New Game", command=self.start_new_game)
        main_menu_btn = tk.Button(self, text="Main Menu", command=self.return_to_main_menu)
        close_btn = tk.Button(self, text="Exit", command=self.close_all)
        delta = 110  # Distance between each button
        new_game_btn.place(x=x, y=50)
        main_menu_btn.place(x=x+delta, y=50)
        close_btn.place(x=x+delta*2, y=50)

    def start_new_game(self):
        """Destroys current game window and opens a new one"""
        self.master.master.destroy()
        new_root = tk.Tk()
        new_game_gui = GameGui(new_root)
        new_game_gui.mainloop()

    def return_to_main_menu(self):
        """Destroys current game window and opens the main menu"""
        from source import MainMenu
        self.master.master.destroy()
        new_root = tk.Tk()
        main_menu = MainMenu(new_root)
        main_menu.mainloop()

    def close_all(self):
        """Close the game"""
        self.master.master.destroy()


class CheckmateWindow(EndGameWindow):
    """
    Window that pops up when a checkmate occurs

    Display which player won the game

    Args:
        master (tkinter.Frame): parent widget
        winner (str): color of the winning player
    """
    def __init__(self, master, winner):
        super().__init__(master)
        self.winner = winner
        self.title("Checkmate")
        self.set_components()

    def set_components(self):
        self.set_label()
        self.set_buttons(10)

    def set_label(self):
        """Defines the text displayed on the window"""
        text = f"{self.winner} wins"
        label = tk.Label(self, text=text, font="sans-serif 15 bold")
        label.place(x=90, y=10)


class DrawWindow(EndGameWindow):
    """
    Window that pops up when the game ends in a draw

    Display the cause of the draw

    Args:
        master (tkinter.Frame): parent widget
        end_game (int): the value that represents how the game ended. Values above 2
            represent a draw
    """
    def __init__(self, master, end_game):
        super().__init__(master, width=350)
        self.end_game = end_game
        self.title("Draw")
        self.set_components()

    def set_components(self):
        self.set_label()
        self.set_buttons(40)

    def set_label(self):
        """Defines the text displayed on the window"""
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
    """
    Window that pops up when the player tries to close the game

    Give the option to save the game in a text file

    Args:
        master (tkinter.Frame): parent widget
    """
    def __init__(self, master):
        width = 300
        height = 160
        super().__init__(width=width, height=height)
        master.paused = True
        self.title("Save Game")
        self.resizable(False, False)
        self.master = master
        self.set_components()
        self.create_game_directory()
        self.bind("<Return>", lambda event: self.yes_btn_event())
        self.bind("<Escape>", lambda event: self.no_btn_event())

    def create_game_directory(self):
        """Creates the directory that keeps the the saved games files, if it doesn't exists"""
        home = os.path.expanduser('~')
        path = f"{home}/.MasterChess"
        if not os.path.exists(path):
            os.mkdir(path)

    def set_components(self):
        save_game_lbl = tk.Label(self, text="Save Game Before Closing?", font="sans-serif 13 bold")
        save_game_lbl.place(x=15, y=20)
        self.set_entry()
        self.set_buttons()

    def set_entry(self):
        """Sets the text entry, where the users can name the file as they wants"""
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
        """Saves the game on a file inside the hidden directory and close the game"""
        game_state = self.master.game.get_game_data()
        filename = self.game_file_entry.get()
        home = os.path.expanduser('~')
        path = f"{home}/.MasterChess/{filename}"
        with open(path, 'w') as game_file:
            game_file.write(game_state)
        self.master.master.destroy()

    def no_btn_event(self):
        "Close the game without saving it"
        self.master.master.destroy()
