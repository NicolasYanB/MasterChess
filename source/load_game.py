import tkinter as tk


class LoadGameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        width, height = 450, 600
        master.geometry(f"{width}x{height}")
        master.resizable(False, False)
        master.title("Load Game")
        self.master = master


if __name__ == '__main__':
    root = tk.Tk()
    load_game_window = LoadGameWindow(root)
    load_game_window.mainloop()
