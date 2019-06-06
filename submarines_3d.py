import numpy as np
from enum import Enum


class GamePiece:
    """A game_piece class from which all game pieces inherit. Includes an __init__, changing the orientation of the piece,
    what happens when the piece gets hit, what happens when the piece is destroyed. """
    destroyed = False
    unique = False  # by default pieces are not one-of-a-kind

    def __init__(self, top_left_coord: tuple, idx: int, board, flip: bool = False):
        assert isinstance(top_left_coord, tuple)
        assert len(top_left_coord) == 3
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
        """if flip == True, this function is called and transposes the game piece. """
        self.shape = self.shape.T

    def hit(self):
        """This function triggers when a game piece is reported to be hit (normally triggered by a child Pixel object).
        If the game piece is sturdy (like Destroyer) it tests to see whether it has any undamaged pixels left, and only
        if it does then it will trigger its own death. If it is not sturdy, it will change the status of all of its
        Pixels to be 'damaged', and will then automatically trigger its own death. """
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
        """This function triggers when the game piece is destroyed. It changes the piece's status to 'destroyed', and
        prints to the player. """
        assert not self.destroyed
        self.destroyed = True
        print("Signal.KILL")
        pass  # kill the game piece


class Pixel:
    """A single 'pixel' of a GamePiece object. These instances are initiated automatically when a game piece is created,
    and are then placed in the game board."""
    damaged = False

    def __init__(self, game_piece: GamePiece, loc: tuple):
        self.game_piece = game_piece
        self.loc = loc

    def __repr__(self):
        if self.damaged:
            return "X"
        return f"{type(self.game_piece).__name__}{self.game_piece.idx}"

    def __str__(self):
        return f"Pixel of game piece {type(self.game_piece).__name__}{self.game_piece.idx} in coordinates {self.loc}"

    def is_damaged(self):
        """returns the 'damaged' status of the pixel (whether is was hit already or not)"""
        return self.damaged

    def hit(self):
        """Triggers when a Pixel gets hit. Changes its 'damaged' status,
        and calls its parent gamepiece's 'hit' function. """
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
        """This function triggers when the General dies. It triggers the death of all other game pieces on the board."""
        for piece in self.board.pieces:
            piece.destroyed = True


class Board:
    """An instance of a game board. Has a player ID (normally 1 or 2), size (rows and columns, with the 3rd dimension
    automatically set to 3); has a 'board' property which is a numpy matrix containing Pixel objects of game pieces;
    has a 'pieces' property which contains all of the game pieces present on the board; and 'num_pieces' which
    specifies how many instances of each game piece should be on the board. The board attempts to automatically place
    all of the requested pieces on the board. If it fails due to a board size which is too small, or number of pieces
    which is too big, it will raise an error message. """

    def __init__(self, size: tuple, number_of_pieces: dict, player_id: int = 0):
        assert isinstance(player_id, int)
        self.player_id = player_id
        self.rows, self.columns = size
        self.board = np.zeros((self.rows, self.columns, 3), dtype=np.object)
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
        return f"Deep: \n{self.board[:, :, 0]} \nSea-level: \n{self.board[:, :, 1]} \nAir: \n{self.board[:, :, 2]}"

    def gen_coord(self, piece_type: GamePiece, z: int, flip: bool):
        """A function used to generate all possible 'top-left coordinates' for a given piece with the given board size
        in a random order. If it finds a suitable coordinate it returns it, and the Board instance may continue to
        place pieces. If no suitable coordinate is found, an error is raised. """
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
        assert max_x >= 0 and max_y >= 0, f"Board size is too small to accommodate piece {piece_type}"
        while len(used) < ((max_x + 1) * (max_y + 1)):
            x = np.random.randint(0, max_x + 1)
            y = np.random.randint(0, max_y + 1)
            if (x, y) in used:
                pass
            valid_placement = True
            for i in range(piece_rows):
                for j in range(piece_cols):
                    if flip:
                        idx = piece_type.shape[j, i]
                    else:
                        idx = piece_type.shape[i, j]
                    if idx == 1:
                        if self.board[i + x, j + y, z] != 0:
                            valid_placement = False
                            break
            if valid_placement:
                return x, y
            used.add((x, y))
        raise AssertionError(f"Too many pieces of type {piece_type} for specified board size. "
                             "Pieces cannot be placed without overlap or going out-of-bound.")

    def strike(self, x: int, y: int, z: int):
        """This function takes a coordinate input, and checks whether this coordinate is a 'hit' (targets an undamaged
        Pixel), or a 'miss'. If a hit, it checks whether the game is over using the 'check_game_over()' function. """
        if self.board[x, y, z] == 0 or (isinstance(self.board[x, y, z], Pixel) and self.board[x, y, z].is_damaged()):
            print("Signal.MISS")
            game_over = False
        else:
            self.board[x, y, z].hit()
            game_over = self.check_game_over()
        return game_over

    def test_coords_valid(self, coords_str: str):
        """This function receives an input string from a player, and tests whether it is a valid coordinate input:
        it must be composed of 3 integers exactly, which are non-negative, and do not exceed the board's boundaries. """
        try:
            x, y, z = eval(coords_str)
            assert isinstance(x, int) and isinstance(y, int) and isinstance(z, int)
            assert x >= 0 and y >= 0 and z >= 0
            assert x < self.rows and y < self.columns and z < 3
            coords_accepted = True
        except:
            coords_accepted = False
        return coords_accepted

    def check_game_over(self):
        """This function checks whether all pieces on the board are destroyed. If so, it returns True."""
        for piece in self.pieces:
            if not piece.destroyed:
                return False
        print("Signal.END")
        return True


def start():
    """This function triggers the beginning of the game. """
    boards = [Board(board_size, number_of_game_pieces, 1), Board(board_size, number_of_game_pieces, 2)]
    gameover = False
    quitgame = False
    i = 1
    while not gameover:
        coords_accepted = False
        while not coords_accepted:
            inp = input(
                f"Player {boards[(i + 1) % 2].player_id}, what is the coordinate you're targeting (row,column,layer)?")
            if inp == "show":
                print(boards[(i + 1) % 2])
                continue
            elif inp == "quit":
                quitgame = True
                break
            elif boards[i].test_coords_valid(inp):
                coords_accepted = True
            else:
                print("Invalid coordinates. ")
        if quitgame:
            print("Quitting game")
            break
        x, y, z = eval(inp)
    gameover = boards[i].strike(x, y, z)
    if gameover:
        print(f"Game over, player #{boards[(i + 1) % 2].player_id} won!")
    i = (i + 1) % 2


class AvailablePieces(Enum):
    """An enumerator containing all of the game pieces available in the game. Any new pieces added to the game should
    be added here as well. """
    Submarine = Submarine
    Destroyer = Destroyer
    Jet = Jet
    General = General


board_size = (6, 6)
number_of_game_pieces = {AvailablePieces.Submarine: 2, AvailablePieces.Destroyer: 2,
                         AvailablePieces.Jet: 1, AvailablePieces.General: 1}
