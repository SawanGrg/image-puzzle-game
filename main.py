"""
Entry point for the Image Puzzle Game.

This file should stay almost empty on purpose — its only job is to
create the Tk root window, hand it to the App class, and start the
event loop. All real logic lives in ui/gui.py, puzzle/, and
transformations/.
"""

import tkinter as tk
from ui.gui import GUI


def main():
    root = tk.Tk()
    root.title("Image Puzzle Game")

    app = GUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()