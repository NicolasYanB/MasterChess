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
        width = height = 104
        miniboard = tk.Canvas(self, width=width, height=height+1)
        miniboard.place(x=285, y=250)

        square_size = width//8
        light_square = "#eeeed2"
        dark_square = "#769656"
        colors = [light_square, dark_square]
        color = 0
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                x0, y0, x1, y1 = x, y, x + square_size, y + square_size
                coords = x0, y0, x1, y1
                miniboard.create_rectangle(coords, fill=colors[color])
                color = abs(color - 1)
            colors.reverse()

        selected_index = listbox.curselection()[0]
        file = listbox.get(selected_index)
        pieces = self.get_pieces(file)
        print(pieces)

    def get_pieces(self, file):
        pieces = []
        path = f"{self.game_dir}/{file}"
        board_state = 0
        with open(path, 'r') as game_file:
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
