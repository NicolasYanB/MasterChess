import tkinter as tk
import os


class LoadGameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        width, height = 450, 600
        master.geometry(f"{width}x{height}")
        master.resizable(False, False)
        master.title("Load Game")
        self.master = master
        home = os.path.expanduser('~')
        self.game_dir = f"{home}/.MasterChess"
        self.pack(expand=True, fill=tk.BOTH)
        self.set_components()

    def set_components(self):
        self.set_listbox()

    def set_listbox(self):
        listbox_frame = tk.Frame(self, width=240, height=590)
        listbox_frame.pack_propagate(False)
        listbox_frame.pack(pady=5, padx=5, side=tk.LEFT)
        listbox = tk.Listbox(listbox_frame, width=28)
        listbox.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        self.add_listbox_elements(listbox)
        listbox.bind("<<ListboxSelect>>", self.on_select)

    def add_listbox_elements(self, listbox):
        game_files = os.listdir(self.game_dir)
        for i in range(len(game_files)):
            game_file = game_files[i]
            listbox.insert(i, game_file)

    def on_select(self, event):
        self.set_miniboard(event.widget)

    def set_miniboard(self, listbox):
        selected_index = listbox.curselection()[0]
        file = listbox.get(selected_index)
        path = f"{self.game_dir}/{file}"
        preview = BoardPreview(self, path)
        preview.show_preview(285, 250)


class BoardPreview(tk.Canvas):
    def __init__(self, master, file):
        self.width = self.height = 104
        super().__init__(master, width=self.width, height=self.height)
        self.square_size = self.width // 8
        light_square = "#eeeed2"
        dark_square = "#769656"
        self.colors = [light_square, dark_square]
        self.images = []
        self.file = file

    def show_preview(self, x, y):
        self.draw_board()
        self.draw_pieces()
        self.place(x=x, y=y)

    def draw_board(self):
        color = 0
        for y in range(0, self.height, self.square_size):
            for x in range(0, self.width, self.square_size):
                x0, y0, x1, y1 = x, y, x + self.square_size, y + self.square_size
                coords = x0, y0, x1, y1
                self.create_rectangle(coords, fill=self.colors[color])
                color = abs(color - 1)
            self.colors.reverse()

    def draw_pieces(self):
        pieces = self.get_pieces()
        for piece in pieces:
            color = piece[0]
            type = piece[1]
            column, line = piece[2:]
            image_path = f"images/mini-pieces/{color}/{type}.png"
            x, y = column * self.square_size, line * self.square_size
            image = tk.PhotoImage(file=image_path)
            self.create_image(x, y, image=image, anchor=tk.NW)
            self.images.append(image)

    def get_pieces(self):
        pieces = []
        board_state = 0
        with open(self.file, 'r') as game_file:
            content = game_file.read()
            board_state = eval(content)[2:]
        for piece in board_state:
            p = piece.split()
            color = p[0]
            type = p[1]
            column, line = int(p[2]), int(p[3])
            pieces.append([color, type, column, line])
        return pieces


if __name__ == '__main__':
    root = tk.Tk()
    load_game_window = LoadGameWindow(root)
    load_game_window.mainloop()
