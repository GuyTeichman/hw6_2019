import numpy as np
import matplotlib.pyplot as plt


class GamePiece:
    def __init__(self, top_left_coord, idx, flip=False):
        self.tl = top_left_coord  # tuple of row and column
        self.idx = idx
        self.flip = flip
        return None

    def hit(self):
        if self.is_sturdy:
            pass  # take damage
        else:
            self.kill()

    def kill(self):
        pass  # kill the game piece


class Submarine(GamePiece):
    def __init__(self, top_left_coord, idx, flip):
        super().__init__(top_left_coord, idx, flip)
        self.is_sturdy = False
        self.z = 0


class Destroyer(GamePiece):
    def __init__(self, top_left_coord, idx, flip):
        super().__init__(top_left_coord, idx, flip)
        self.is_sturdy = True
        self.z = 1


class Jet(GamePiece):
    def __init__(self, top_left_coord, idx, flip):
        super().__init__(top_left_coord, idx, flip)
        self.is_sturdy = False
        self.z = 2
