import tkinter as tk
from PIL import Image, ImageTk


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width, self.height = 350, 300
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()
        self.master = master
        self.set_background()
        self.set_buttons()

    def set_background(self):
        img_path = "images/background.png"
        img = Image.open(img_path)
        resized_img = img.resize((self.width, self.height), Image.ANTIALIAS)
        background = ImageTk.PhotoImage(resized_img)
        self.canvas.background = background
        self.canvas.create_image(0, 0, anchor=tk.NW, image=background)

    def set_buttons(self):
        btn_new_game = tk.Button(text="New Game")
        btn_load_game = tk.Button(text="Load Game")
        self.canvas.create_window(60, 220, anchor=tk.NW, window=btn_new_game)
        self.canvas.create_window(200, 220, anchor=tk.NW, window=btn_load_game)


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


main()
