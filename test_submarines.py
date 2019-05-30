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
    truth = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]]).T
    assert np.array_equal(myjet.shape, truth)


def test_z_incompatible_with_gamepiece():
    with pytest.raises(AssertionError):
        myjet = Jet((0, 0, 0), 0, None, False)


def test_top_left_coordinate_not_in_board():
    pass


def test_game_piece_out_of_bounds():
    pass


def test_game_piece_overlap():
    pass


def test_board_creation():
    assert Board(5, 5)


def test_board_invalid_input():
    pass


def test_board_nonpositive_index():
    pass


def test_board_dunder_str():
    pass
