import tkinter as tk
from PIL import Image, ImageTk


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width = 350
        self.height = 300
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.canvas.pack()
        self.master = master
        self.set_background()

    def set_background(self):
        img_path = "images/background.png"
        img = Image.open(img_path)
        resized_img = img.resize((self.width, self.height), Image.ANTIALIAS)
        background = ImageTk.PhotoImage(resized_img)
        self.canvas.background = background
        self.canvas.create_image(0, 0, anchor=tk.NW, image=background)


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


main()
