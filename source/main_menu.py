import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master


def main():
    root = tk.Tk()
    main_menu = MainMenu(root)
    main_menu.mainloop()


main()
