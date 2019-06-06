import pytest
import numpy as np
import matplotlib.pyplot as plt
from submarines_3d import *


def test_submarine_creation():
    assert Submarine((0, 0, 0), 0, None, False)


def test_destroyer_creation():
    assert Destroyer((0, 0, 1), 0, None, False)


def test_jet_creation():
    assert Jet((0, 0, 2), 0, None, False)


def test_general_creation():
    assert General((0, 0, 0), 0, None, False)
    assert General((1, 1, 1), 1, None, True)


def test_dunder_str_of_gamepiece():
    piece = Destroyer((0, 0, 1), 3, False)
    assert piece.__str__() == "Destroyer3"


def test_gamepiece_creation_flip():
    assert Jet((0, 0, 2), 0, None, True)


def test_coordinates_not_tuple():
    with pytest.raises(AssertionError):
        myship = Destroyer("001", 0, None, False)


def test_coordinates_missing():
    with pytest.raises(AssertionError):
        myship = Destroyer((0, 0), 0, None, False)


def test_too_many_coordinates():
    with pytest.raises(AssertionError):
        myship = Destroyer((0, 0, 1, 0), 0, None, False)


def test_flip_orientation():
    myjet = Jet((0, 0, 2), 0, None, True)
    truth_jet = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]]).T
    mysub = Submarine((0, 0, 0), 0, None, True)
    truth_sub = np.ones((3, 1), dtype=int)

    assert np.array_equal(myjet.shape, truth_jet)
    assert np.array_equal(mysub.shape, truth_sub)


def test_z_incompatible_with_gamepiece():
    with pytest.raises(AssertionError):
        myjet = Jet((0, 0, 0), 0, None, False)


def test_board_too_small_for_piece_type():
    board_size = (3, 3)
    number_of_pieces = {AvailablePieces.Jet: 1}
    with pytest.raises(AssertionError) as e:
        myboard = Board(board_size, number_of_pieces)
    assert "Board size is too small to accommodate" in str(e.value)


def test_too_many_pieces_to_fit_in_board():
    board_size = (5, 5)
    number_of_pieces = {AvailablePieces.Destroyer: 7}
    with pytest.raises(AssertionError) as e:
        myboard = Board(board_size, number_of_pieces)
    assert "Too many pieces of type" in str(e.value)


def test_board_creation():
    board_size = (10, 10)
    board_size_2 = (8, 8)
    number_of_pieces = {AvailablePieces.General: 1, AvailablePieces.Submarine: 4, AvailablePieces.Destroyer: 3,
                        AvailablePieces.Jet: 2}
    number_of_pieces_2 = {AvailablePieces.Destroyer: 4}
    assert Board(board_size, number_of_pieces)
    assert Board(board_size_2, number_of_pieces_2)


def test_board_strike_invalid_input():
    board_size = (5, 5)
    number_of_pieces = {AvailablePieces.Destroyer: 2}
    brd = Board(board_size, number_of_pieces)
    inputs = ["5,5,1", ("0,0,3"), "0,1", ("0,1,"), "0,4,-1", "h,s,f", "", "0,1,2,2"]
    for inp in inputs:
        assert not brd.test_coords_valid(inp)


def test_sturdy_gamepiece_damaged_not_destroyed():
    dst = Destroyer((0, 0, 1), 0, "board", False)
    assert not dst.destroyed
    dst.pixels[0].hit()
    assert dst.pixels[0].damaged
    assert not dst.pixels[1].damaged
    assert not dst.destroyed


def test_sturdy_gamepiece_destroyed():
    dst = Destroyer((0, 0, 1), 0, "board", False)
    assert not dst.destroyed
    for pxl in dst.pixels:
        pxl.hit()
    for pxl in dst.pixels:
        assert pxl.damaged
    assert dst.destroyed


def test_unsturdy_gamepiece_destroyed():
    sub = Submarine((0, 0, 0), 0, "board", False)
    assert not sub.destroyed
    sub.pixels[0].hit()
    for pxl in sub.pixels:
        assert pxl.damaged
    assert sub.destroyed


def test_multiple_generals():
    board_size = (10, 10)
    number_of_pieces = {AvailablePieces.General: 2}
    with pytest.raises(AssertionError):
        board = Board(board_size, number_of_pieces)


def test_general_game_over():
    pass


def test_game_over():
    board_size = (1, 1)
    number_of_pieces = {AvailablePieces.General: 1}
    brd = Board(board_size, number_of_pieces)
    for z in range(3):
        brd.strike(0, 0, z)
    for piece in brd.pieces:
        assert piece.destroyed
        for pxl in piece.pixels:
            assert pxl.damaged
