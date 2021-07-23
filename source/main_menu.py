import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.width = 350
        self.height = 300
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Master Chess")
        self.master = master


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


main()
