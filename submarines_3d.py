import numpy as np
import matplotlib.pyplot as plt


class GamePiece:
    shape = np.array([])

    def __init__(self, top_left_coord, idx, flip=False):
        self.tl = top_left_coord  # tuple of row and column
        self.idx = idx
        self.flip = flip
        if self.flip:
            self.change_orientation()

    def change_orientation(self):
        self.shape = self.shape.T

    def hit(self):
        if self.is_sturdy:
            pass  # take damage
        else:
            self.kill()

    def kill(self):
        print("Signal.KILL")
        pass  # kill the game piece


class Submarine(GamePiece):
    shape = np.array([1, 1, 1])
    is_sturdy = False
    z = 0
    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = False
    #     self.z = 0


class Destroyer(GamePiece):
    shape = np.array([1, 1, 1, 1])
    is_sturdy = True
    z = 1

    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = True
    #     self.z = 1


class Jet(GamePiece):
    shape = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])
    is_sturdy = False
    z = 2
    #
    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = False
    #     self.z = 2


class General(GamePiece):
    shape = np.array([1])
    is_sturdy = False

    def __init__(self, top_left_coord, idx, flip):
        super().__init__(top_left_coord, idx, flip)
        self.z = self.tl[2]

    def kill(self):
        pass  # trigger game over
