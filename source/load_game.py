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
        listbox_frame = ListboxFrame(self)
        listbox_frame.pack(pady=5, padx=5, side=tk.LEFT)
        listbox_frame.add_elements(os.listdir(self.game_dir))
        listbox_frame.set_on_select_event(self.on_select)

    def on_select(self, event):
        self.set_miniboard(event.widget.master)

    def set_miniboard(self, listbox):
        file = listbox.get_selected_element()
        if file is None:
            return
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


class ListboxFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=240, height=590)
        self.pack_propagate(False)
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


if __name__ == '__main__':
    root = tk.Tk()
    load_game_window = LoadGameWindow(root)
    load_game_window.mainloop()
