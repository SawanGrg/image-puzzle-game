import random

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

from .styles import Styles
from puzzle.board import Board
from puzzle.game_state import GameState


class GUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Image Puzzle Game")
        self.root.geometry("1000x700")
        self.root.configure(bg=Styles.BG)
        self.root.resizable(True, True)

        self.selected_image = None
        self.grid_size = 3

        # created once "Start Puzzle" is pressed
        self.board = None
        self.game_state = None

        # must keep references or Tkinter garbage-collects the images
        self.original_photo = None
        self.puzzle_photo = None

        self.show_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # Screen 1: welcome
    # ------------------------------------------------------------------

    def show_welcome_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=Styles.BG)
        container.pack(expand=True, fill="both")

        content = tk.Frame(container, bg=Styles.BG)
        content.pack(expand=True)

        title = tk.Label(
            content,
            text="Image Puzzle Game",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        title.pack(pady=(0, 10))

        subtitle = tk.Label(
            content,
            text="Restore the scrambled image by moving, rotating and flipping tiles.",
            font=Styles.SUBTITLE_FONT,
            bg=Styles.BG,
            fg=Styles.MUTED
        )
        subtitle.pack(pady=(0, 25))

        start_button = tk.Button(
            content,
            text="Start Game",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            bg=Styles.ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.show_setup_screen
        )
        start_button.pack()

    # ------------------------------------------------------------------
    # Screen 2: setup (image + grid size)
    # ------------------------------------------------------------------

    def show_setup_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=Styles.BG)
        container.pack(expand=True, fill="both", padx=Styles.PAGE_PAD_X, pady=Styles.PAGE_PAD_Y)

        title = tk.Label(
            container,
            text="Game Setup",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        title.pack(pady=(20, 30))

        image_section = tk.Frame(
            container,
            bg=Styles.PANEL,
            highlightbackground=Styles.BORDER,
            highlightthickness=1
        )
        image_section.pack(fill="x", padx=100)

        image_title = tk.Label(
            image_section,
            text="Choose an Image",
            font=Styles.HEADING_FONT,
            bg=Styles.PANEL,
            fg=Styles.TEXT
        )
        image_title.pack(pady=(20, 10))

        self.image_label = tk.Label(
            image_section,
            text="No image selected",
            font=Styles.LABEL_FONT,
            bg=Styles.PANEL,
            fg=Styles.MUTED
        )
        self.image_label.pack(pady=(0, 15))

        browse_button = tk.Button(
            image_section,
            text="Browse Image",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.select_image
        )
        browse_button.pack(pady=(0, 20))

        grid_section = tk.Frame(container, bg=Styles.BG)
        grid_section.pack(pady=30)

        grid_title = tk.Label(
            grid_section,
            text="Select Grid Size",
            font=Styles.HEADING_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        grid_title.pack(pady=(0, 10))

        self.grid_var = tk.IntVar(value=3)

        options = tk.Frame(grid_section, bg=Styles.BG)
        options.pack()

        for size in (3, 4, 5):
            radio = tk.Radiobutton(
                options,
                text=f"{size} × {size}",
                variable=self.grid_var,
                value=size,
                font=Styles.LABEL_FONT,
                bg=Styles.BG,
                fg=Styles.TEXT,
                activebackground=Styles.BG,
                selectcolor=Styles.PANEL
            )
            radio.pack(side="left", padx=15)

        start_button = tk.Button(
            container,
            text="Start Puzzle",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            bg=Styles.ACCENT,
            fg="white",
            relief="flat",
            command=self.start_game
        )
        start_button.pack(pady=10)

        back_button = tk.Button(
            container,
            text="Back",
            font=Styles.SMALL_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT,
            relief="flat",
            command=self.show_welcome_screen
        )
        back_button.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("Bitmap Files", "*.bmp")
            ]
        )

        if not file_path:
            return

        image = cv2.imread(file_path)

        if image is None:
            messagebox.showerror(
                "Invalid Image",
                "The selected file could not be loaded as an image."
            )
            return

        self.selected_image = file_path

        self.image_label.config(
            text=file_path,
            fg=Styles.SUCCESS
        )

    def start_game(self):
        if not self.selected_image:
            messagebox.showwarning(
                "No Image",
                "Please select an image first."
            )
            return

        self.grid_size = self.grid_var.get()

        try:
            self.board = Board(self.grid_size)
            self.board.load_image(self.selected_image)
            self.board.scramble()
        except ValueError as e:
            messagebox.showerror("Could not load image", str(e))
            return

        self.game_state = GameState()

        self.show_game_screen()

    # ------------------------------------------------------------------
    # Screen 3: the actual puzzle
    # ------------------------------------------------------------------

    def show_game_screen(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=Styles.BG)
        main_frame.pack(fill="both", expand=True, padx=Styles.PAGE_PAD_X, pady=Styles.PAGE_PAD_Y)

        header = tk.Frame(main_frame, bg=Styles.BG)
        header.pack(fill="x", pady=(0, 20))

        title = tk.Label(
            header,
            text="Image Puzzle Game",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        title.pack(side="left")

        stats = tk.Frame(header, bg=Styles.BG)
        stats.pack(side="right")

        self.moves_label = tk.Label(
            stats,
            text="Moves: 0",
            font=Styles.LABEL_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        self.moves_label.pack(side="left", padx=10)

        self.tiles_left_label = tk.Label(
            stats,
            text="Tiles Incorrect: 0",
            font=Styles.LABEL_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        )
        self.tiles_left_label.pack(side="left", padx=10)

        boards = tk.Frame(main_frame, bg=Styles.BG)
        boards.pack(expand=True, fill="both")

        original_section = tk.Frame(
            boards,
            bg=Styles.PANEL,
            highlightbackground=Styles.BORDER,
            highlightthickness=1
        )
        original_section.pack(side="left", expand=True, fill="both", padx=(0, 10))

        tk.Label(
            original_section,
            text="Original Image",
            font=Styles.HEADING_FONT,
            bg=Styles.PANEL,
            fg=Styles.TEXT
        ).pack(pady=15)

        img_h, img_w = self.board.original_image.shape[:2]

        self.original_canvas = tk.Canvas(
            original_section,
            bg=Styles.PANEL,
            width=img_w,
            height=img_h,
            highlightthickness=0
        )
        self.original_canvas.pack(padx=20, pady=20)

        puzzle_section = tk.Frame(
            boards,
            bg=Styles.PANEL,
            highlightbackground=Styles.BORDER,
            highlightthickness=1
        )
        puzzle_section.pack(side="right", expand=True, fill="both", padx=(10, 0))

        tk.Label(
            puzzle_section,
            text="Puzzle",
            font=Styles.HEADING_FONT,
            bg=Styles.PANEL,
            fg=Styles.TEXT
        ).pack(pady=15)

        self.puzzle_canvas = tk.Canvas(
            puzzle_section,
            bg="white",
            width=img_w,
            height=img_h,
            highlightbackground=Styles.BORDER,
            highlightthickness=1
        )
        self.puzzle_canvas.pack(padx=40, pady=20)

        self.puzzle_canvas.bind("<Button-1>", self.on_puzzle_click)
        self.puzzle_canvas.bind("<Button-3>", self.on_puzzle_right_click)
        self.puzzle_canvas.bind("<Shift-Button-1>", self.on_puzzle_shift_click)

        controls = tk.Frame(main_frame, bg=Styles.BG)
        controls.pack(fill="x", pady=(20, 0))

        self.hint_button = tk.Button(
            controls,
            text="Hint",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.show_hint
        )
        self.hint_button.pack(side="left", padx=5)

        solve_button = tk.Button(
            controls,
            text="Solve",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.solve_puzzle
        )
        solve_button.pack(side="left", padx=5)

        load_button = tk.Button(
            controls,
            text="Load New Image",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.show_setup_screen
        )
        load_button.pack(side="right", padx=5)

        self.render()

    # ------------------------------------------------------------------
    # Coordinate <-> tile helpers
    # ------------------------------------------------------------------

    def _cell_rect(self, position):
        """Pixel rectangle (x0, y0, x1, y1) for a grid position index."""
        row = position // self.board.grid_size
        col = position % self.board.grid_size
        x0 = col * self.board.tile_width
        y0 = row * self.board.tile_height
        x1 = x0 + self.board.tile_width
        y1 = y0 + self.board.tile_height
        return x0, y0, x1, y1

    def _cv2_to_photo(self, cv_image):
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)
        return ImageTk.PhotoImage(pil_image)

    # ------------------------------------------------------------------
    # Rendering — the single place that redraws everything from state
    # ------------------------------------------------------------------

    def render(self):
        grid_size = self.board.grid_size

        # --- original image (left, static reference) ---
        self.original_canvas.delete("all")
        self.original_photo = self._cv2_to_photo(self.board.original_image)
        self.original_canvas.create_image(0, 0, anchor="nw", image=self.original_photo)

        # --- transformed image (right, interactive) ---
        self.puzzle_canvas.delete("all")
        self.puzzle_photo = self._cv2_to_photo(self.board.reassemble())
        self.puzzle_canvas.create_image(0, 0, anchor="nw", image=self.puzzle_photo)

        # faint grid lines over the puzzle canvas
        for i in range(1, grid_size):
            x = i * self.board.tile_width
            y = i * self.board.tile_height
            self.puzzle_canvas.create_line(x, 0, x, self.board.original_image.shape[0], fill="#cccccc")
            self.puzzle_canvas.create_line(0, y, self.board.original_image.shape[1], y, fill="#cccccc")

        # green ticks on correct tiles
        for tile in self.board.tiles:
            if tile.is_correct():
                x0, y0, _, _ = self._cell_rect(tile.current_position)
                self.puzzle_canvas.create_text(
                    x0 + 12, y0 + 12,
                    text="✓",
                    fill="#2ecc71",
                    font=("Arial", 14, "bold")
                )

        # highlight the currently selected tile
        selected = self.game_state.selected_tile
        if selected is not None:
            x0, y0, x1, y1 = self._cell_rect(selected.current_position)
            self.puzzle_canvas.create_rectangle(
                x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                outline="#3498db", width=3
            )

        # active hint: blue circle on puzzle canvas AND on original canvas
        hint_tile = self.game_state.active_hint
        if hint_tile is not None:
            px0, py0, px1, py1 = self._cell_rect(hint_tile.current_position)
            cx, cy = (px0 + px1) / 2, (py0 + py1) / 2
            self.puzzle_canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, outline="#2980ff", width=3)

            ox0, oy0, ox1, oy1 = self._cell_rect(hint_tile.correct_position)
            ocx, ocy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
            self.original_canvas.create_oval(ocx - 10, ocy - 10, ocx + 10, ocy + 10, outline="#2980ff", width=3)

        # counters
        self.moves_label.config(text=f"Moves: {self.game_state.moves}")
        self.tiles_left_label.config(text=f"Tiles Incorrect: {self.board.incorrect_count()}")

        # hint button state
        if self.game_state.has_hints_left():
            self.hint_button.config(state="normal")
        else:
            self.hint_button.config(state="disabled")

        # completion check
        if self.board.is_solved() and not self.game_state.input_locked:
            self.game_state.lock_input()
            messagebox.showinfo("Solved!", "You restored the picture! Load a new image to keep playing.")

    # ------------------------------------------------------------------
    # Click handling
    # ------------------------------------------------------------------

    def on_puzzle_click(self, event):
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return  # click landed outside the image

        selected = self.game_state.selected_tile

        if selected is None:
            self.game_state.select(tile)
        elif self.game_state.is_selected(tile):
            self.game_state.clear_selection()
        else:
            self.board.swap(selected, tile)
            self.game_state.clear_selection()
            self.game_state.register_move()

        self.render()

    def on_puzzle_right_click(self, event):
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return

        tile.apply_rotation(90)
        self.game_state.register_move()
        self.render()

    def on_puzzle_shift_click(self, event):
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return

        tile.apply_flip(horizontal=True)
        self.game_state.register_move()
        self.render()

    # ------------------------------------------------------------------
    # Hint / Solve
    # ------------------------------------------------------------------

    def show_hint(self):
        if self.game_state.input_locked or not self.game_state.has_hints_left():
            return

        incorrect_tiles = [t for t in self.board.tiles if not t.is_correct()]
        if not incorrect_tiles:
            return

        tile = random.choice(incorrect_tiles)
        self.game_state.use_hint(tile)
        self.render()

    def solve_puzzle(self):
        self.board.solve()
        self.game_state.reset()
        self.render()
