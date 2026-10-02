import tkinter as tk
from ui.gui import GUI


def main():
    root = tk.Tk()
    root.title("Image Puzzle Game")

    app = GUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()