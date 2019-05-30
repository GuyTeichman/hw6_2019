import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple as tpl


class GamePiece:
    """A parent class from which all game pieces inherit. Includes an __init__, changing the orientation of the piece,
    what happens when the piece gets hit, what happens when the piece is destroyed. """

    def __init__(self, top_left_coord, idx, flip=False):
        self.tl = top_left_coord  # tuple of row and column
        self.idx = idx
        self.flip = flip
        if self.flip:
            self.change_orientation()

    def __str__(self):
        return f"{type(self).__name__}{self.idx}"

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
    """A game piece that can only exist in z layer 0, with a shape of [1 1 1],
    which is not sturdy (destroyed on first hit). """
    shape = np.array([1, 1, 1])
    is_sturdy = False
    z = 0
    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = False
    #     self.z = 0


class Destroyer(GamePiece):
    """A game piece that can only exist in z layer 1, with a shape of [1 1 1c1],
which is sturdy (requires multiple hits to be destroyed). """
    shape = np.array([1, 1, 1, 1])
    is_sturdy = True
    z = 1

    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = True
    #     self.z = 1


class Jet(GamePiece):
    """A game piece that can only exist in z layer 2, which is not sturdy (destroyed on first hit),
     and the following shape:
     [[0 1 0]
      [1 1 1]
      [0 1 0]
      [0 1 0]]"""
    shape = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])
    is_sturdy = False
    z = 2
    #
    # def __init__(self, top_left_coord, idx, flip):
    #     super().__init__(top_left_coord, idx, flip)
    #     self.is_sturdy = False
    #     self.z = 2


class General(GamePiece):
    """A game piece that can  exist in any z layer , with a shape of [1]. Immediate game over when it gets hit. """
    shape = np.array([1])
    is_sturdy = False

    def __init__(self, top_left_coord, idx, flip):
        super().__init__(top_left_coord, idx, flip)
        self.z = self.tl[2]

    def kill(self):
        pass  # trigger game over


class Board:
    available_pieces = [Submarine, Destroyer, Jet, General]

    def __init__(self, rows, columns):
        self.board = np.zeros((rows, columns))

    def __str__(self):
        pass
