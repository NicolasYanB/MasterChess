import tkinter as tk


class LoadGameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        width, height = 450, 600
        master.geometry(f"{width}x{height}")
        master.resizable(False, False)
        master.title("Load Game")
        self.master = master
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


if __name__ == '__main__':
    root = tk.Tk()
    load_game_window = LoadGameWindow(root)
    load_game_window.mainloop()
