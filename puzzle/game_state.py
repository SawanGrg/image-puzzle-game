class GameState:
    MAX_HINTS = 3

    def __init__(self):
        self._moves = 0
        self._hints_used = 0
        self._selected_tile = None
        self._input_locked = False
        self._active_hint = None  # tile currently showing a blue hint circle

    # ------------------------------------------------------------------
    # Moves
    # ------------------------------------------------------------------

    @property
    def moves(self):
        return self._moves

    def register_move(self):
        """Call this once for every swap, rotate, or flip the player makes."""
        self._moves += 1
        # spec: hint circle disappears after the NEXT move, so clear it here
        self.clear_hint()

    # ------------------------------------------------------------------
    # Tile selection (for the left-click select -> select -> swap flow)
    # ------------------------------------------------------------------

    @property
    def selected_tile(self):
        return self._selected_tile

    def select(self, tile):
        self._selected_tile = tile

    def clear_selection(self):
        self._selected_tile = None

    def is_selected(self, tile):
        return self._selected_tile is tile

    # ------------------------------------------------------------------
    # Hints
    # ------------------------------------------------------------------

    @property
    def hints_used(self):
        return self._hints_used

    @property
    def hints_remaining(self):
        return self.MAX_HINTS - self._hints_used

    def has_hints_left(self):
        return self._hints_used < self.MAX_HINTS

    def use_hint(self, tile):
        """
        Call this when the Hint button is pressed and a tile has been
        chosen to reveal. Returns False if no hints are left (caller
        should already have disabled the button by this point, but this
        is a safety check).
        """
        if not self.has_hints_left():
            return False

        self._hints_used += 1
        self._active_hint = tile
        return True

    @property
    def active_hint(self):
        """The tile currently marked with a blue hint circle, or None."""
        return self._active_hint

    def clear_hint(self):
        self._active_hint = None

    # ------------------------------------------------------------------
    # Completion / lock
    # ------------------------------------------------------------------

    @property
    def input_locked(self):
        return self._input_locked

    def lock_input(self):
        self._input_locked = True

    def unlock_input(self):
        self._input_locked = False

    # ------------------------------------------------------------------
    # Reset (new image loaded, or Solve pressed)
    # ------------------------------------------------------------------

    def reset(self):
        self._moves = 0
        self._hints_used = 0
        self._selected_tile = None
        self._input_locked = False
        self._active_hint = None