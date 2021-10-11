import tkinter as tk
from PIL import Image, ImageTk
import os


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width, self.height = 350, 300
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.pack()
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.master = master
        self.set_background()
        self.create_game_directory()
        self.set_buttons()

    def set_background(self):
        img_path = "images/background.png"
        img = Image.open(img_path)
        resized_img = img.resize((self.width, self.height), Image.ANTIALIAS)
        background = ImageTk.PhotoImage(resized_img)
        self.canvas.background = background
        self.canvas.create_image(0, 0, anchor=tk.NW, image=background)

    def create_game_directory(self):
        home = os.path.expanduser('~')
        path = f"{home}/.MasterChess"
        if not os.path.exists(path):
            os.mkdir(path)

    def set_buttons(self):
        btn_new_game = tk.Button(self, text="New Game", command=self.start_new_game)
        btn_load_game = tk.Button(self, text="Load Game")
        self.canvas.create_window(60, 220, anchor=tk.NW, window=btn_new_game)
        self.canvas.create_window(200, 220, anchor=tk.NW, window=btn_load_game)

    def start_new_game(self):
        from source import GameGui
        self.master.destroy()
        new_root = tk.Tk()
        game_gui = GameGui(new_root)
        game_gui.mainloop()


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


if __name__ == '__main__':
    main()
