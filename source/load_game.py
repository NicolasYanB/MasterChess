import tkinter as tk
import os

from source import MainMenu, GameGui
from source import realpath


class LoadGameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        width, height = 450, 450
        master.geometry(f"{width}x{height}")
        master.resizable(False, False)
        master.title("Load Game")
        icon = tk.PhotoImage(file=f"{realpath}/images/icon.png")
        master.iconphoto(False, icon)
        self.master = master
        home_dir = os.path.expanduser('~')
        self.game_dir = f"{home_dir}/.MasterChess"
        self.listbox_frame = ListboxFrame(self)
        self.pack(expand=True, fill=tk.BOTH)
        self.set_components()

    def set_components(self):
        self.set_listbox()
        self.set_back_button()

    def set_listbox(self):
        self.listbox_frame.pack(pady=20, padx=5, side=tk.LEFT, anchor=tk.S)
        game_files = os.listdir(self.game_dir)
        self.listbox_frame.add_elements(game_files)
        self.listbox_frame.set_on_select_event(self.listbox_on_select)

    def set_back_button(self):
        image_path = f"{realpath}/images/back.png"
        self.btn_image = tk.PhotoImage(file=image_path)
        back_btn = tk.Button(self, image=self.btn_image, command=self.back_to_main_menu)
        back_btn.place(x=5, y=0)

    def listbox_on_select(self, event):
        self.remove_current_preview()
        listbox = event.widget.master
        self.show_board_preview(listbox)
        self.show_captured_pieces(listbox)
        self.set_turn_label(listbox)
        self.set_buttons()

    def show_board_preview(self, listbox):
        filename = listbox.get_selected_element()
        if filename is None:
            return
        path = f"{self.game_dir}/{filename}"
        preview = BoardPreview(self, path)
        preview.show_preview(x=285, y=175)

    def show_captured_pieces(self, listbox):
        filename = listbox.get_selected_element()
        if filename is None:
            return
        path = f"{self.game_dir}/{filename}"
        white_pieces = CapturedPiecesField(self, "white", path)
        black_pieces = CapturedPiecesField(self, "black", path)
        white_pieces.place(x=285, y=140)
        black_pieces.place(x=285, y=290)

    def set_turn_label(self, listbox):
        filename = listbox.get_selected_element()
        if filename is None:
            return
        path = f"{self.game_dir}/{filename}"
        turn = 0
        with open(path, 'r') as game_file:
            content = eval(game_file.read())
            turn = content[-3]
        text = f"Turn player: {turn}"
        lbl_turn = tk.Label(self, text=text)
        lbl_turn.place(x=270, y=100)

    def set_buttons(self):
        load_btn = tk.Button(self, text="Load", command=self.load_game)
        delete_btn = tk.Button(self, text="Delete", command=self.delete_file)
        load_btn.place(x=260, y=340)
        delete_btn.place(x=350, y=340)

    def delete_file(self):
        listbox = self.listbox_frame.listbox
        selected_element = self.listbox_frame.get_selected_element()
        if selected_element is None:
            return
        path = f"{self.game_dir}/{selected_element}"
        os.remove(path)
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        self.remove_current_preview()

    def load_game(self):
        selected_element = self.listbox_frame.get_selected_element()
        if selected_element is None:
            return
        path = f"{self.game_dir}/{selected_element}"
        game = 0
        with open(path, 'r') as game_file:
            content = game_file.read()
            game = eval(content)
        self.master.destroy()
        new_root = tk.Tk()
        game_gui = GameGui(new_root, loaded_game=game)
        game_gui.mainloop()

    def remove_current_preview(self):
        children = self.winfo_children()
        for child in children:
            if child._name == "!listboxframe" or child._name == "!button":
                continue
            child.destroy()

    def back_to_main_menu(self):
        self.master.destroy()
        new_root = tk.Tk()
        main_menu = MainMenu(new_root)
        main_menu.mainloop()


class BoardPreview(tk.Canvas):
    def __init__(self, master, file):
        self.width = self.height = 104
        super().__init__(master, width=self.width, height=self.height)
        self.square_size = self.width // 8
        self.images = []
        self.file = file

    def show_preview(self, x, y):
        self.draw_board()
        self.draw_pieces()
        self.place(x=x, y=y)

    def draw_board(self):
        light_square = "#eeeed2"
        dark_square = "#769656"
        colors = [light_square, dark_square]
        color = 0
        for y in range(0, self.height, self.square_size):
            for x in range(0, self.width, self.square_size):
                x0, y0, x1, y1 = x, y, x + self.square_size, y + self.square_size
                coords = x0, y0, x1, y1
                self.create_rectangle(coords, fill=colors[color])
                color = abs(color - 1)
            colors.reverse()

    def draw_pieces(self):
        pieces = self.get_pieces()
        for piece in pieces:
            color = piece[0]
            piece_type = piece[1]
            column, line = piece[2:]
            image_path = f"{realpath}/images/mini-pieces/{color}/{piece_type}.png"
            x, y = column * self.square_size, line * self.square_size
            image = tk.PhotoImage(file=image_path)
            self.create_image(x, y, image=image, anchor=tk.NW)
            self.images.append(image)

    def get_pieces(self):
        pieces = []
        board_state = 0
        with open(self.file, 'r') as game_file:
            content = eval(game_file.read())
            board_state = content[:-4]
        for piece in board_state:
            piece_info = piece.split()
            color = piece_info[0]
            piece_type = piece_info[1]
            column, line = int(piece_info[2]), int(piece_info[3])
            pieces.append([color, piece_type, column, line])
        return pieces


class ListboxFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=240, height=570)
        self.pack_propagate(False)  # tell the frame not let its children control its size
        self.listbox = tk.Listbox(self, width=28)
        self.listbox.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

    def add_elements(self, elm_list):
        for i in range(len(elm_list)):
            elm = elm_list[i]
            self.listbox.insert(i, elm)

    def get_selected_element(self):
        try:
            selected_index = self.listbox.curselection()[0]
        except IndexError:
            return
        element = self.listbox.get(selected_index)
        return element

    def set_on_select_event(self, function):
        self.listbox.bind("<<ListboxSelect>>", function)


class CapturedPiecesField(tk.Canvas):
    def __init__(self, master, color, file):
        super().__init__(master, width=104, height=26)
        self.color = color
        self.path = file
        self.show_captured_pieces()

    def show_captured_pieces(self):
        pieces = self.sort_pieces(self.get_pieces())
        self.draw_pieces(pieces)

    def get_pieces(self):
        captured_pieces = 0
        with open(self.path, 'r') as game_file:
            content = eval(game_file.read())
            captured_pieces = content[-1]
        return captured_pieces[self.color]

    def sort_pieces(self, pieces):
        # Each piece have a value according to its type
        # Lower its value, lower its position in the sorted list
        #          0        1         2        3        4
        order = ["pawn", "knight", "bishop", "rook", "queen"]
        initial_index = 0
        while initial_index < len(pieces) - 1:
            lower_piece_value = order.index(pieces[initial_index])
            lower_piece_index = initial_index
            for i in range(initial_index+1, len(pieces)):
                piece_value = order.index(pieces[i])
                if piece_value < lower_piece_value:
                    lower_piece_value = piece_value
                    lower_piece_index = i
            piece = pieces.pop(lower_piece_index)
            pieces.insert(initial_index, piece)
            initial_index += 1
        return pieces

    def draw_pieces(self, pieces):
        self.images = []
        column = line = 0
        piece_size = 13
        for piece in pieces:
            img_path = f"{realpath}/images/mini-pieces/{self.color}/{piece}.png"
            image = tk.PhotoImage(file=img_path)
            x, y = column * piece_size, line * piece_size
            self.create_image(x, y, image=image, anchor=tk.NW)
            self.images.append(image)
            if column == 7:
                column = 0
                line += 1
            else:
                column += 1
