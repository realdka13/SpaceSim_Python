import numpy as np

class TrailManager:
    def __init__(self, max_length=1000):
        #Max Length
        self.max_length = max_length

        #Body Dictionary
        self.trails = {}

    def add_body(self, body_id, initial_pos):
        #Add body to dictionary
        self.trails[body_id] = [np.array(initial_pos, dtype=float)]

    def update(self, body_id, new_pos):
        #Add next position to trail
        self.trails[body_id].append(np.array(new_pos, dtype=float))

        #Remove positions beyond max length
        self.trails[body_id] = self.trails[body_id][-self.max_length:]

    def get_trail(self, body_id):
        #Return Trail Data
        return self.trails[body_id]

    def set_max_length(self, length):
        #Change Max Length
        self.max_length = max(1, int(length))

        #Update Current trail data with new max length
        for key in self.trails:
            self.trails[key] = self.trails[key][-self.max_length:]

    def get_max_length(self):
        #Return Max Length
        return self.max_length
    
    def clear(self, body_id=None):
        #Clear Trails
        if body_id is None:
            for key in self.trails:
                self.trails[key] = []
        else:
            if body_id in self.trails:
                self.trails[body_id] = []