import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple as tpl
from enum import Enum


class GamePiece:
    """A game_piece class from which all game pieces inherit. Includes an __init__, changing the orientation of the piece,
    what happens when the piece gets hit, what happens when the piece is destroyed. """
    destroyed = False
    unique = False  # by default pieces are not one-of-a-kind

    def __init__(self, top_left_coord: tuple, idx: int, board, flip: bool = False):
        assert isinstance(top_left_coord, tuple)
        assert len(top_left_coord) == 3
        if len(np.shape(self.shape)) == 1:
            self.shape.shape = (1, np.shape(self.shape)[0])
        try:
            assert top_left_coord[2] == self.z, "piece placed in invalid layer"
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

    def __init__(self, game_piece: GamePiece, loc: tuple):
        self.game_piece = game_piece
        self.loc = loc

    def __str__(self):
        return f"{type(self.game_piece).__name__}{self.game_piece.idx}"

    def __repr__(self):
        return f"Pixel of game piece {type(self.game_piece).__name__}{self.game_piece.idx} in coordinates {self.loc}"

    def is_damaged(self):
        return self.damaged

    def hit(self):
        assert not self.damaged
        self.damaged = True
        self.game_piece.hit()


class Submarine(GamePiece):
    """A game piece that can only exist in z layer 0, with a shape of [1 1 1],
    which is not sturdy (destroyed on first hit). """
    shape = np.array([[1, 1, 1]])
    is_sturdy = False
    z = 0


class Destroyer(GamePiece):
    """A game piece that can only exist in z layer 1, with a shape of [1 1 1c1],
which is sturdy (requires multiple hits to be destroyed). """
    shape = np.array([[1, 1, 1, 1]])
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
    unique = True  # A general is a one-of-a-kind piece by definition
    shape = np.array([[1]])
    is_sturdy = False

    def __init__(self, top_left_coord: tuple, idx: int, board, flip: bool):
        super().__init__(top_left_coord, idx, board, flip)
        self.z = self.tl[2]

    def kill(self):
        pass  # trigger game over


class Board:
    def __init__(self, size: tuple, number_of_pieces: dict):
        self.rows, self.columns = size
        self.board = np.zeros((self.rows, self.columns, 3),dtype=np.object)
        self.num_pieces = number_of_pieces
        self.pieces = []
        for piece in self.num_pieces:
            assert (not piece.value.unique) or (piece.value.unique and self.num_pieces[piece] <= 1), \
                f"Cannot have more than one of the unique piece {piece.name}!"
            assert isinstance(self.num_pieces[piece], int) and self.num_pieces[piece] > 0, \
                f"Invalid number of the game piece {piece.name}!"
            # piece_shape = piece.value.shape.

            for i in range(self.num_pieces[piece]):  # generate every instance of the piece required
                flip = np.random.choice([True, False])
                try:
                    z = piece.value.z
                except AttributeError:
                    z = np.random.randint(0, 3)
                try:
                    row, col = self.gen_coord(piece.value, z, flip)
                except AssertionError as e:
                    row, col = self.gen_coord(piece.value, z, not flip)
                self.pieces.append(piece.value((row, col, z), i, self, flip))
                for pxl in self.pieces[-1].pixels:
                    self.board[pxl.loc[0], pxl.loc[1], pxl.loc[2]] = pxl

    def __str__(self):
        return self.board.__str__()

    def gen_coord(self, piece_type: GamePiece, z: int, flip: bool):
        used = set()
        try:
            piece_rows, piece_cols = np.shape(piece_type.shape)
        except ValueError:
            piece_cols = np.shape(piece_type.shape)[0]
            piece_rows = 1
        if flip:
            piece_rows, piece_cols = piece_cols, piece_rows
        max_x = self.rows - piece_rows
        max_y = self.columns - piece_cols
        assert max_x >= 0 and max_y >= 0, f"Board size is too small to accomodate piece {piece_type}"
        while len(used) < ((max_x + 1) * (max_y + 1)):
            x = np.random.randint(0, max_x + 1)
            y = np.random.randint(0, max_y + 1)
            if (x, y) in used:
                pass
            valid_placement = True
            for i in range(piece_rows):
                for j in range(piece_cols):
                    if flip:
                        idx = piece_type.shape[j,i]
                    else:
                        idx = piece_type.shape[i,j]
                    if idx == 1:
                        if self.board[i + x, j + y, z] != 0:
                            valid_placement = False
                            break
            if valid_placement:
                return x, y
            used.add((x, y))
        raise AssertionError(f"Too many pieces of type {piece_type} for specified board size. "
                        "Pieces cannot be placed without overlap or going out-of-bound.")


class AvailablePieces(Enum):
    Submarine = Submarine
    Destroyer = Destroyer
    Jet = Jet
    General = General


board_size = (10, 10)
number_of_pieces = {AvailablePieces.Submarine: 4, AvailablePieces.Destroyer: 4,
                    AvailablePieces.Jet: 3, AvailablePieces.General: 1}

# def start():
board1 = Board(board_size,number_of_pieces)
