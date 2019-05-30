import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple as tpl


class GamePiece:
    """A game_piece class from which all game pieces inherit. Includes an __init__, changing the orientation of the piece,
    what happens when the piece gets hit, what happens when the piece is destroyed. """
    destroyed = False

    def __init__(self, top_left_coord, idx, board, flip=False):
        assert isinstance(top_left_coord, tuple)
        assert len(top_left_coord) == 3
        if len(np.shape(self.shape)) == 1:
            self.shape.shape =  (1, np.shape(self.shape)[0])
        try:
            assert top_left_coord[2] == self.z
        except AttributeError:
            self.z = top_left_coord[2]

        self.tl = top_left_coord  # tuple of row and column
        self.idx = idx
        self.board = board
        self.flip = flip
        if self.flip:
            self.change_orientation()

        self.pixels = []
        try:
            rows, cols = np.shape(self.shape)
        except ValueError:
            rows = np.shape(self.shape)[0]
            cols = 1
        for row in range(rows):
            for col in range(cols):
                if self.shape[row, col] == 1:
                    self.pixels.append(Pixel(self, (row + self.tl[0], col + self.tl[1], self.tl[2])))

    def __str__(self):
        return f"{type(self).__name__}{self.idx}"

    def change_orientation(self):
        self.shape = self.shape.T

    def hit(self):
        if self.is_sturdy:
            print("Signal.HIT")
            for pxl in self.pixels:
                if not pxl.damaged:  # if one of the pixels is not yet damaged, stop the code
                    return None
        else:
            for pxl in self.pixels:
                pxl.damaged = True

        self.kill()

    def kill(self):
        assert not self.destroyed
        self.destroyed = True
        print("Signal.KILL")
        pass  # kill the game piece


class Pixel:
    damaged = False

    def __init__(self, game_piece, loc):
        self.game_piece = game_piece
        self.loc = loc

    def is_damaged(self):
        return self.damaged

    def hit(self):
        assert not self.damaged
        self.damaged = True
        self.game_piece.hit()


class Submarine(GamePiece):
    """A game piece that can only exist in z layer 0, with a shape of [1 1 1],
    which is not sturdy (destroyed on first hit). """
    shape = np.array([1, 1, 1])
    is_sturdy = False
    z = 0


class Destroyer(GamePiece):
    """A game piece that can only exist in z layer 1, with a shape of [1 1 1c1],
which is sturdy (requires multiple hits to be destroyed). """
    shape = np.array([1, 1, 1, 1])
    is_sturdy = True
    z = 1


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


class General(GamePiece):
    """A game piece that can  exist in any z layer , with a shape of [1]. Immediate game over when it gets hit. """
    shape = np.array([1])
    is_sturdy = False

    def __init__(self, top_left_coord, idx, board, flip):
        super().__init__(top_left_coord, idx, board, flip)
        self.z = self.tl[2]

    def kill(self):
        pass  # trigger game over


class Board:
    available_pieces = [Submarine, Destroyer, Jet, General]

    def __init__(self, rows, columns):
        self.board = np.zeros((rows, columns, 3))

    def __str__(self):
        pass
