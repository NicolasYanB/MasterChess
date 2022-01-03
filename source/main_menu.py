import tkinter as tk
import os

from PIL import Image, ImageTk

realpath = __file__.split('/')
dir_index = realpath.index("MasterChess")
realpath = '/'.join(realpath[:dir_index+1])  # Path to the script directory 'MasterChess'


class MainMenu(tk.Frame):
    """
    First window to appear to the user.
    Gives two options: Start a new game or resume an unfinished game
    """

    def __init__(self, master):
        super().__init__(master)
        self.width, self.height = 350, 300
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        icon = tk.PhotoImage(file=f"{realpath}/images/icon.png")
        master.iconphoto(False, icon)
        self.pack()
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.master = master
        self.set_background_img()
        self.create_game_directory()
        self.set_buttons()

    def set_background_img(self):
        img_path = f"{realpath}/images/background.png"
        img = Image.open(img_path)
        resized_img = img.resize((self.width, self.height), Image.ANTIALIAS)
        background = ImageTk.PhotoImage(resized_img)
        self.canvas.background = background  # reference
        self.canvas.create_image(0, 0, anchor=tk.NW, image=background)

    def create_game_directory(self):
        """
        Creates the directory that the saved games will be stored
        """
        home = os.path.expanduser('~')
        path = f"{home}/.MasterChess"
        if not os.path.exists(path):
            os.mkdir(path)

    def set_buttons(self):
        btn_new_game = tk.Button(self, text="New Game", command=self.start_new_game)
        btn_load_game = tk.Button(self, text="Load Game", command=self.open_load_game_window)
        self.canvas.create_window(60, 220, anchor=tk.NW, window=btn_new_game)
        self.canvas.create_window(200, 220, anchor=tk.NW, window=btn_load_game)

    def start_new_game(self):
        from source import GameGui
        self.master.destroy()  # Destroy old root
        new_root = tk.Tk()
        game_gui = GameGui(new_root)
        game_gui.mainloop()

    def open_load_game_window(self):
        from source import LoadGameWindow
        self.master.destroy()
        new_root = tk.Tk()
        load_game_window = LoadGameWindow(new_root)
        load_game_window.mainloop()


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


if __name__ == '__main__':
    main()
