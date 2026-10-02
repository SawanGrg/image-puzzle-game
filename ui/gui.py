#Hit137 Software Now
#Assessment3 - Image Puzzle Game
#Riwaj Shrestha (403312)
#Sawan Gurung (407504)
#Jung-Chuan Chiang (406089)



"""Tkinter GUI: welcome, setup and game screens."""
import random
import sys

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

from .styles import Styles
from puzzle.board import Board
from puzzle.game_state import GameState


class GUI:
    """Builds the screens and translates user input into Board/GameState calls."""

    def __init__(self, root):
        self.root = root

        self.root.title("Image Puzzle Game")
        self.root.geometry("1000x760")
        self.root.configure(bg=Styles.BG)
        self.root.resizable(True, True)

        self.selected_image = None
        self.grid_size = 3
        self.difficulty = "Easy"
        self._timer_job = None


        self.board = None
        self.game_state = None


        self.original_photo = None
        self.puzzle_photo = None


        self.tile_buttons = []

        self.show_welcome_screen()

    def clear_window(self):
        self._cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()



    def show_welcome_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=Styles.BG)
        container.pack(expand=True, fill="both")

        content = tk.Frame(container, bg=Styles.BG)
        content.pack(expand=True)

        tk.Label(
            content,
            text="Image Puzzle Game",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        ).pack(pady=(0, 10))

        tk.Label(
            content,
            text="Restore the scrambled image by moving, rotating and flipping tiles.",
            font=Styles.SUBTITLE_FONT,
            bg=Styles.BG,
            fg=Styles.MUTED
        ).pack(pady=(0, 25))

        tk.Button(
            content,
            text="Start Game",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            bg=Styles.ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.show_setup_screen
        ).pack()

    

    def show_setup_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=Styles.BG)
        container.pack(expand=True, fill="both", padx=Styles.PAGE_PAD_X, pady=Styles.PAGE_PAD_Y)

        tk.Label(
            container,
            text="Game Setup",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        ).pack(pady=(20, 30))

        image_section = tk.Frame(
            container,
            bg=Styles.PANEL,
            highlightbackground=Styles.BORDER,
            highlightthickness=1
        )
        image_section.pack(fill="x", padx=100)

        tk.Label(
            image_section,
            text="Choose an Image",
            font=Styles.HEADING_FONT,
            bg=Styles.PANEL,
            fg=Styles.TEXT
        ).pack(pady=(20, 10))

        self.image_label = tk.Label(
            image_section,
            text="No image selected",
            font=Styles.LABEL_FONT,
            bg=Styles.PANEL,
            fg=Styles.MUTED
        )
        self.image_label.pack(pady=(0, 15))
        if self.selected_image:
            self.image_label.config(text=self.selected_image, fg=Styles.SUCCESS)

        tk.Button(
            image_section,
            text="Browse Image",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.select_image
        ).pack(pady=(0, 20))

        grid_section = tk.Frame(container, bg=Styles.BG)
        grid_section.pack(pady=30)

        tk.Label(
            grid_section,
            text="Select Grid Size",
            font=Styles.HEADING_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        ).pack(pady=(0, 10))

        self.grid_var = tk.IntVar(value=self.grid_size)

        options = tk.Frame(grid_section, bg=Styles.BG)
        options.pack()

        for size in (3, 4, 5):
            tk.Radiobutton(
                options,
                text=f"{size} × {size}",
                variable=self.grid_var,
                value=size,
                font=Styles.LABEL_FONT,
                bg=Styles.BG,
                fg=Styles.TEXT,
                activebackground=Styles.BG,
                selectcolor=Styles.PANEL
            ).pack(side="left", padx=15)

        difficulty_section = tk.Frame(container, bg=Styles.BG)
        difficulty_section.pack(pady=(0, 20))

        tk.Label(
            difficulty_section,
            text="Select Difficulty",
            font=Styles.HEADING_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        ).pack(pady=(0, 10))

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_text = {"Easy": "Easy (no time limit)",
                           "Medium": "Medium (5 min)",
                           "Hard": "Hard (3 min)"}
        for level in GameState.DIFFICULTY_LIMITS:
            tk.Radiobutton(
                difficulty_section,
                text=difficulty_text[level],
                variable=self.difficulty_var,
                value=level,
                font=Styles.LABEL_FONT,
                bg=Styles.BG,
                fg=Styles.TEXT,
                activebackground=Styles.BG,
                selectcolor=Styles.PANEL
            ).pack(side="left", padx=15)

        tk.Button(
            container,
            text="Start Puzzle",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            bg=Styles.ACCENT,
            fg="white",
            relief="flat",
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            container,
            text="Back",
            font=Styles.SMALL_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT,
            relief="flat",
            command=self.show_welcome_screen
        ).pack()

    def select_image(self):
        """Open a file dialog and validate the chosen image."""
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

        try:
            Board.read_image(file_path)
        except ValueError:
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
        """Create a fresh Board and GameState, then show the game screen."""
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

        self.difficulty = self.difficulty_var.get()
        self.game_state = GameState(GameState.DIFFICULTY_LIMITS[self.difficulty])

        self.show_game_screen()

    

    def show_game_screen(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=Styles.BG)
        main_frame.pack(fill="both", expand=True, padx=Styles.PAGE_PAD_X, pady=Styles.PAGE_PAD_Y)

        header = tk.Frame(main_frame, bg=Styles.BG)
        header.pack(fill="x", pady=(0, 20))

        tk.Label(
            header,
            text="Image Puzzle Game",
            font=Styles.TITLE_FONT,
            bg=Styles.BG,
            fg=Styles.TEXT
        ).pack(side="left")

        stats = tk.Frame(header, bg=Styles.BG)
        stats.pack(side="right")

        self.moves_label = tk.Label(
            stats, text="Moves: 0", font=Styles.LABEL_FONT,
            bg=Styles.BG, fg=Styles.TEXT
        )
        self.moves_label.pack(side="left", padx=10)

        self.tiles_left_label = tk.Label(
            stats, text="Tiles Incorrect: 0", font=Styles.LABEL_FONT,
            bg=Styles.BG, fg=Styles.TEXT
        )
        self.tiles_left_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(
            stats, text="Time: 00:00", font=Styles.LABEL_FONT,
            bg=Styles.BG, fg=Styles.TEXT
        )
        self.timer_label.pack(side="left", padx=10)

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
        
        right_button = "<Button-2>" if sys.platform == "darwin" else "<Button-3>"
        self.puzzle_canvas.bind(right_button, self.on_puzzle_right_click)
        self.puzzle_canvas.bind("<Shift-Button-1>", self.on_puzzle_shift_click)

        
        tile_tools = tk.Frame(main_frame, bg=Styles.BG)
        tile_tools.pack(fill="x", pady=(15, 0))

        tk.Label(
            tile_tools,
            text="Selected tile:",
            font=Styles.LABEL_FONT,
            bg=Styles.BG,
            fg=Styles.MUTED
        ).pack(side="left", padx=(5, 10))

        self.tile_buttons = []
        tool_specs = [
            ("⟲ Rotate Left", lambda: self.rotate_selected(-90)),
            ("⟳ Rotate Right", lambda: self.rotate_selected(90)),
            ("⇆ Flip Horizontal", lambda: self.flip_selected(horizontal=True)),
            ("⇅ Flip Vertical", lambda: self.flip_selected(vertical=True)),
        ]
        for text, command in tool_specs:
            btn = tk.Button(
                tile_tools,
                text=text,
                font=Styles.SMALL_FONT,
                width=16,
                state="disabled",
                command=command
            )
            btn.pack(side="left", padx=5)
            self.tile_buttons.append(btn)

        
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

        self.solve_button = tk.Button(
            controls,
            text="Solve",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.solve_puzzle
        )
        self.solve_button.pack(side="left", padx=5)


        tk.Button(
            controls,
            text="Load New Image",
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            command=self.show_setup_screen
        ).pack(side="right", padx=5)

        self.render()
        self._tick()

    

    def _cancel_timer(self):
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

    @staticmethod
    def _format_time(seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def _update_timer_label(self):
        state = self.game_state
        if state.time_left is None:
            self.timer_label.config(text=f"Time: {self._format_time(state.elapsed)}")
        else:
            self.timer_label.config(text=f"Time left: {self._format_time(state.time_left)}")

    def _tick(self):
        """Refresh the clock a few times per second until the round ends."""
        self._timer_job = None
        self._update_timer_label()

        if self.game_state.input_locked:
            return

        if self.game_state.is_time_up:
            self.game_state.lock_input()
            self.render()
            messagebox.showinfo(
                "Time's up!",
                "You ran out of time. Load a new image to try again.",
                parent=self.root,
            )
            return

        self._timer_job = self.root.after(250, self._tick)

    

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

    

    def render(self):
        grid_size = self.board.grid_size
        state = self.game_state


        self.original_canvas.delete("all")
        self.original_photo = self._cv2_to_photo(self.board.original_image)
        self.original_canvas.create_image(0, 0, anchor="nw", image=self.original_photo)

        
        self.puzzle_canvas.delete("all")
        self.puzzle_photo = self._cv2_to_photo(self.board.reassemble())
        self.puzzle_canvas.create_image(0, 0, anchor="nw", image=self.puzzle_photo)

        
        for i in range(1, grid_size):
            x = i * self.board.tile_width
            y = i * self.board.tile_height
            self.puzzle_canvas.create_line(x, 0, x, self.board.original_image.shape[0], fill="#cccccc")
            self.puzzle_canvas.create_line(0, y, self.board.original_image.shape[1], y, fill="#cccccc")

        
        for tile in self.board.tiles:
            if tile.is_correct():
                x0, y0, _, _ = self._cell_rect(tile.current_position)
                self.puzzle_canvas.create_text(
                    x0 + 12, y0 + 12,
                    text="✓",
                    fill="#2ecc71",
                    font=("Arial", 14, "bold")
                )

        
        selected = state.selected_tile
        if selected is not None:
            x0, y0, x1, y1 = self._cell_rect(selected.current_position)
            self.puzzle_canvas.create_rectangle(
                x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                outline="#3498db", width=3
            )

        
        tools_state = (
            "normal"
            if selected is not None and not state.input_locked
            else "disabled"
        )
        for btn in self.tile_buttons:
            btn.config(state=tools_state)

        
        hint_tile = state.active_hint
        if hint_tile is not None:
            px0, py0, px1, py1 = self._cell_rect(hint_tile.current_position)
            cx, cy = (px0 + px1) / 2, (py0 + py1) / 2
            self.puzzle_canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, outline="#2980ff", width=3)

            ox0, oy0, ox1, oy1 = self._cell_rect(hint_tile.correct_position)
            ocx, ocy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
            self.original_canvas.create_oval(ocx - 10, ocy - 10, ocx + 10, ocy + 10, outline="#2980ff", width=3)

        
        self.moves_label.config(text=f"Moves: {state.moves}")
        self.tiles_left_label.config(text=f"Tiles Incorrect: {self.board.incorrect_count()}")
        
        self._refresh_action_buttons()

        
        if self.board.is_solved() and not state.input_locked:
            state.lock_input()
            self._update_timer_label()
            self.render()  
            messagebox.showinfo(
                "Solved!",
                f"You restored the picture in {state.moves} moves "
                f"({self._format_time(state.elapsed)}). "
                "Load a new image to keep playing.",
                parent=self.root,
            )

    def _refresh_action_buttons(self):
        """Hint/Solve only work while the round is running (Hint also needs hints left)."""
        playing = not self.game_state.input_locked
        hint_ok = playing and self.game_state.has_hints_left()
        self.hint_button.config(state="normal" if hint_ok else "disabled")
        self.solve_button.config(state="normal" if playing else "disabled")



    def on_puzzle_click(self, event):
        """Left click: select, deselect, or swap with the selected tile."""
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return  

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
        """Right click: rotate the tile 90 degrees clockwise."""
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return

        tile.apply_rotation(90)
        self.game_state.register_move()
        self.render()

    def on_puzzle_shift_click(self, event):
        """Shift + left click: flip the tile horizontally."""
        if self.game_state.input_locked:
            return

        tile = self.board.get_tile_at(event.x, event.y)
        if tile is None:
            return

        tile.apply_flip(horizontal=True)
        self.game_state.register_move()
        self.render()


    def rotate_selected(self, degrees):
        if self.game_state.input_locked:
            return

        tile = self.game_state.selected_tile
        if tile is None:
            return

        tile.apply_rotation(degrees)
        self.game_state.register_move()
        self.render()

    def flip_selected(self, horizontal=False, vertical=False):
        if self.game_state.input_locked:
            return

        tile = self.game_state.selected_tile
        if tile is None:
            return

        tile.apply_flip(horizontal=horizontal, vertical=vertical)
        self.game_state.register_move()
        self.render()

    def show_hint(self):
        """Mark one incorrect tile (and its home position) with a blue circle."""
        if self.game_state.input_locked or not self.game_state.has_hints_left():
            return

        incorrect_tiles = [t for t in self.board.tiles if not t.is_correct()]
        if not incorrect_tiles:
            return

        tile = random.choice(incorrect_tiles)
        self.game_state.use_hint(tile)
        self.render()

    def solve_puzzle(self):
        """Undo all transformations, clear moves, and lock input."""
        if self.game_state.input_locked or self.board.is_solved():
            return

        self.board.solve()
        self.game_state.reset_moves()
        self.game_state.clear_selection()
        self.game_state.clear_hint()
        self.game_state.lock_input()
        self.render()

        messagebox.showinfo(
            "Solved!",
            "Puzzle has been automatically restored.",
            parent=self.root,
        )