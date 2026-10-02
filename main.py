#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)


import tkinter as tk
from ui.gui import GUI


def main():
    root = tk.Tk()
    root.title("Image Puzzle Game")

    app = GUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()