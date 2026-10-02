import time

class GameState:
    MAX_HINTS = 3

    # difficulty name -> time limit in seconds (None = no limit)
    DIFFICULTY_LIMITS = {"Easy": None, "Medium": 300, "Hard": 180}

    def __init__(self, time_limit=None):
        self._time_limit = time_limit
        self._start_time = time.monotonic()
        self._end_time = None
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

    def reset_moves(self):
        """Clear the move counter (used by Solve)."""
        self._moves = 0

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
        self.stop_timer()

    def unlock_input(self):
        self._input_locked = False

    @property
    def elapsed(self):
        """Whole seconds played (freezes once the round ends)."""
        end = self._end_time if self._end_time is not None else time.monotonic()
        return int(end - self._start_time)

    @property
    def time_limit(self):
        return self._time_limit

    @property
    def time_left(self):
        if self._time_limit is None:
            return None
        return max(0, self._time_limit - self.elapsed)

    @property
    def is_time_up(self):
        return self._time_limit is not None and self.elapsed >= self._time_limit

    def stop_timer(self):
        if self._end_time is None:
            self._end_time = time.monotonic()
    # ------------------------------------------------------------------
    # Reset (new image loaded, or Solve pressed)
    # ------------------------------------------------------------------

    def reset(self):
        self._moves = 0
        self._hints_used = 0
        self._selected_tile = None
        self._input_locked = False
        self._active_hint = None
        self._start_time = time.monotonic()
        self._end_time = None