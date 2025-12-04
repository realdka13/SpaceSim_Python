import numpy as np

class TrailManager:
    def __init__(self, max_length=1000):
        self.max_length = max_length
        self.trails = {}  # stores trails keyed by body id

    def add_body(self, body_id, initial_pos):
        """Initialize trail for a new body"""
        self.trails[body_id] = [np.array(initial_pos, dtype=float)]

    def update(self, body_id, new_pos):
        """Add new position to trail and keep length within max_length"""
        self.trails[body_id].append(np.array(new_pos, dtype=float))
        self.trails[body_id] = self.trails[body_id][-self.max_length:]

    def get_trail(self, body_id):
        """Return a list of positions for plotting"""
        return self.trails[body_id]

    def set_max_length(self, length):
        self.max_length = max(1, int(length))
        for key in self.trails:
            self.trails[key] = self.trails[key][-self.max_length:]

    def get_max_length(self):
        """Return the current max trail length"""
        return self.max_length
    
    def clear(self, body_id=None):
        """
        Clear trails.
        If body_id is None, clears all trails.
        Otherwise, clears only the specified body's trail.
        """
        if body_id is None:
            for key in self.trails:
                self.trails[key] = []
        else:
            if body_id in self.trails:
                self.trails[body_id] = []